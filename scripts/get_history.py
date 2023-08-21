"""Get your full match history from the Halo Infinite API."""

import argparse
import asyncio
import os
from pathlib import Path
from typing import Any, AsyncIterator

import dotenv
import pandas as pd
from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens
from spnkr.client import HaloInfiniteClient
from spnkr.parsers.flat_dict import parse_match_history
from spnkr.xuid import XUID

dotenv.load_dotenv()

REFRESH_TOKEN = os.environ["SPNKR_REFRESH_TOKEN"]
CLIENT_ID = os.environ["SPNKR_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPNKR_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPNKR_REDIRECT_URI"]


async def iter_matches(
    client: HaloInfiniteClient, xuid: XUID
) -> AsyncIterator[dict[str, Any]]:
    """Request and yield match history results from the Halo Infinite API."""
    count = 25
    start = 0
    while count == 25:
        print(start)
        response = await client.get_match_history(xuid, start, count)
        history = parse_match_history(await response.json())
        for match in history:
            yield match
        count = len(history)
        start += count


async def main(out_path: Path) -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    # Get the most recent match in the output file, if it exists.
    # This prevents us from requesting matches we already have.
    old_df = most_recent = None
    if out_path.exists():
        assert out_path.suffix == ".csv"
        old_df = pd.read_csv(out_path)
        old_df["start_time"] = pd.to_datetime(old_df["start_time"])
        most_recent = old_df["start_time"].max()

    async with ClientSession() as session:
        # Refresh the player's tokens.
        player = await refresh_player_tokens(session, REFRESH_TOKEN, app)
        client = HaloInfiniteClient(
            session=session,
            spartan_token=player.spartan_token.token,
            clearance_token=player.clearance_token.token,
        )

        # Request the player's match history.
        matches = []
        async for match in iter_matches(client, player.xuid):
            if most_recent is not None and match["start_time"] <= most_recent:
                # We've reached the most recent match in the output file.
                break
            matches.append(match)

    new_df = pd.DataFrame(matches)
    if old_df is not None:
        # Combine the old and new datasets.
        new_df = pd.concat([old_df, new_df])
    new_df.to_csv(out_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out_path", type=Path, help="Output file path")
    args = parser.parse_args()

    asyncio.run(main(args.out_path))
