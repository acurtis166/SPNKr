"""Search all assets in Halo Infinite and save to CSV."""

import asyncio
import os

import dotenv
import pandas as pd
from aiohttp import ClientSession

from spnkr import AzureApp, HaloInfiniteClient, refresh_player_tokens

dotenv.load_dotenv()

REFRESH_TOKEN = os.environ["SPNKR_REFRESH_TOKEN"]
CLIENT_ID = os.environ["SPNKR_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPNKR_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPNKR_REDIRECT_URI"]


async def main() -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    async with ClientSession() as session:
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)
        client = HaloInfiniteClient(
            session=session,
            spartan_token=player.spartan_token.token,
            clearance_token=player.clearance_token.token,
        )
        start = 0
        result_count = 101
        records = []
        while result_count == 101:
            print(f"Getting assets {start} to {start + 101}")
            resp = await client.discovery_ugc.search_assets(start, count=101)
            page = await resp.parse()
            for asset in page.results:
                record = (
                    str(asset.asset_id),
                    str(asset.asset_version_id),
                    asset.asset_kind.name.lower(),
                    asset.name,
                    asset.description,
                    asset.plays_all_time,
                    asset.average_rating,
                )
                records.append(record)
            result_count = page.result_count
            start += page.result_count

        columns = [
            "asset_id",
            "version_id",
            "asset_kind",
            "name",
            "description",
            "plays_all_time",
            "average_rating",
        ]
        pd.DataFrame(records, columns=columns).to_csv("assets.csv", index=False)


if __name__ == "__main__":
    asyncio.run(main())
