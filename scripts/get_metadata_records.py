"""Save metadata from the Halo Infinite API to CSV files."""

import argparse
import asyncio
import os
from pathlib import Path
from typing import Callable, Coroutine

import dotenv
import pandas as pd
from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens
from spnkr.client import HaloInfiniteClient
from spnkr.parsers.records import AssetRecord, parse_asset, parse_medal_metadata

dotenv.load_dotenv()

REFRESH_TOKEN = os.environ["SPNKR_REFRESH_TOKEN"]
CLIENT_ID = os.environ["SPNKR_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPNKR_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPNKR_REDIRECT_URI"]


async def get_asset(
    getter: Callable[[str, str], Coroutine], asset_id: str, version_id: str
) -> AssetRecord:
    data = await getter(asset_id, version_id)
    return parse_asset(data)


async def main(match_history_path: Path, out_path: Path) -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    # Get the map, mode, playlist, and map-mode pair IDs from the match history.
    history = pd.read_csv(match_history_path)
    map_ids = (
        history[["map_variant_asset_id", "map_variant_version_id"]]
        .drop_duplicates()
        .itertuples(index=False)
    )
    mode_ids = (
        history[["game_variant_asset_id", "game_variant_version_id"]]
        .drop_duplicates()
        .itertuples(index=False)
    )
    playlist_ids = (
        history[["playlist_asset_id", "playlist_version_id"]]
        .drop_duplicates()
        .dropna()
        .itertuples(index=False)
    )
    map_mode_ids = (
        history[["map_mode_pair_asset_id", "map_mode_pair_version_id"]]
        .drop_duplicates()
        .dropna()
        .itertuples(index=False)
    )

    maps = []
    modes = []
    playlists = []
    map_modes = []

    async with ClientSession() as session:
        # Refresh the player's tokens.
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)
        client = HaloInfiniteClient(
            session=session,
            spartan_token=player.spartan_token.token,
            clearance_token=player.clearance_token.token,
        )

        # Get the assets and medals.
        maps = await asyncio.gather(
            get_asset(client.discovery_ugc.get_map, aid, vid)
            for aid, vid in map_ids
        )
        modes = await asyncio.gather(
            get_asset(client.discovery_ugc.get_ugc_game_variant, aid, vid)
            for aid, vid in mode_ids
        )
        playlists = await asyncio.gather(
            get_asset(client.discovery_ugc.get_playlist, aid, vid)
            for aid, vid in playlist_ids
        )
        map_modes = await asyncio.gather(
            get_asset(client.discovery_ugc.get_map_mode_pair, aid, vid)
            for aid, vid in map_mode_ids
        )
        medal_data = await client.gamecms_hacs.get_medal_metadata()
        medals = parse_medal_metadata(medal_data)

    # Write the assets and medals to CSV files.
    write_args = {
        "maps": maps,
        "modes": modes,
        "playlists": playlists,
        "map_modes": map_modes,
        "medals": medals,
    }
    for name, data in write_args.items():
        df = pd.DataFrame(data)
        df.to_csv(out_path / f"{name}.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("i", type=Path, help="Match history CSV file")
    parser.add_argument("o", type=Path, help="Output directory")
    args = parser.parse_args()

    asyncio.run(main(args.i, args.o))
