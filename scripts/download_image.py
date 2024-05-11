"""Download an image from game CMS."""

import asyncio
import os

import dotenv
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
        resp = await client.gamecms_hacs.get_image(
            "career_rank/ProgressWidget/64_Corporal_Gold_III.png"
        )
        with open("test.png", "wb") as f:
            f.write(await resp.read())


if __name__ == "__main__":
    asyncio.run(main())
