"""Download full match data from the Halo Infinite API using a CSV of history."""

import argparse
import asyncio
import json
import os
from pathlib import Path

import aiofiles
import dotenv
import pandas as pd
from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens
from spnkr.client import HaloInfiniteClient

dotenv.load_dotenv()

REFRESH_TOKEN = os.environ["SPNKR_REFRESH_TOKEN"]
CLIENT_ID = os.environ["SPNKR_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPNKR_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPNKR_REDIRECT_URI"]


async def make_request(
    client: HaloInfiniteClient, match_id: str, out_path: Path
) -> str:
    """Make a request to the Halo Infinite API and save the response."""
    data = await client.stats.get_match_stats(match_id)
    file_name = f"{match_id}.json"
    async with aiofiles.open(out_path / file_name, "w") as f:
        await f.write(json.dumps(data))
    return file_name


async def main(history_path: Path, out_dir: Path) -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    # Get match ids that already exist in the output directory.
    existing_matches = set(f.stem for f in out_dir.glob("*.json"))

    # Get NEW match ids from the CSV.
    history_df = pd.read_csv(history_path)
    match_ids = set(history_df["match_id"]) - existing_matches

    async with ClientSession() as session:
        # Refresh the player's tokens.
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)
        client = HaloInfiniteClient(
            session=session,
            spartan_token=player.spartan_token.token,
            clearance_token=player.clearance_token.token,
        )

        # Make requests for each match id.
        jobs = [make_request(client, mid, out_dir) for mid in match_ids]
        file_names = await asyncio.gather(*jobs)

    print(f"Downloaded {len(file_names)} matches.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("i", type=Path, help="Path to input history CSV file.")
    parser.add_argument("o", type=Path, help="Path to output directory.")
    args = parser.parse_args()
    assert args.i.suffix == ".csv"
    assert args.o.is_dir()

    asyncio.run(main(args.i, args.o))
