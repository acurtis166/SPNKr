"""Download skill results from the Halo Infinite API using a CSV of match stats."""

import argparse
import asyncio
import json
import os
from pathlib import Path

import aiofiles
import dotenv
import pandas as pd
from aiohttp import ClientResponseError, ClientSession

from spnkr import AzureApp, HaloInfiniteClient, refresh_player_tokens

dotenv.load_dotenv()

REFRESH_TOKEN = os.environ["SPNKR_REFRESH_TOKEN"]
CLIENT_ID = os.environ["SPNKR_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPNKR_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPNKR_REDIRECT_URI"]


async def make_request(
    client: HaloInfiniteClient,
    match_id: str,
    xuids: list[str],
    out_path: Path,
) -> tuple[str, int, str | None]:
    """Make a request to the Halo Infinite API and save the response."""
    try:
        data = await client.skill.get_match_skill(match_id, xuids)
    except ClientResponseError as e:
        return match_id, e.status, e.message
    file_name = f"{match_id}.json"
    async with aiofiles.open(out_path / file_name, "w") as f:
        await f.write(json.dumps(data))
    return match_id, 200, None


async def main(player_stats_path: Path, out_dir: Path) -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    # Get match ids that already exist in the output directory.
    existing_matches = set(f.stem for f in out_dir.glob("*.json"))

    # Get match id/xuid pairs from the CSV.
    df = pd.read_csv(player_stats_path)
    df = df[~df["match_id"].isin(existing_matches)]  # Remove existing matches.
    match_iter = (
        df.groupby("match_id").aggregate({"player_id": list}).itertuples()
    )

    async with ClientSession() as session:
        # Refresh the player's tokens.
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)
        client = HaloInfiniteClient(
            session=session,
            spartan_token=player.spartan_token.token,
            clearance_token=player.clearance_token.token,
        )

        # Make requests for each match.
        jobs = [
            make_request(client, mid, xuids, out_dir)
            for mid, xuids in match_iter
        ]
        results = await asyncio.gather(*jobs)

    report = pd.DataFrame(results, columns=["match_id", "status", "reason"])
    out_path = player_stats_path.parent / "report.csv"
    report.to_csv(out_path, index=False)

    print(f"Processed {len(results)} matches.")
    print(f"Saved report to {out_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "i", type=Path, help="Path to input player stats CSV file."
    )
    parser.add_argument("o", type=Path, help="Path to output directory.")
    args = parser.parse_args()
    assert args.i.suffix == ".csv"
    assert args.o.is_dir()

    asyncio.run(main(args.i, args.o))
