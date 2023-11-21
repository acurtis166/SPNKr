"""Get gamertags for a list of Xbox User IDs (XUIDs)."""

import argparse
import asyncio
import os

import dotenv
from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens
from spnkr.client import HaloInfiniteClient
from spnkr.parsers.pydantic import User

dotenv.load_dotenv()

CLIENT_ID = os.environ["SPNKR_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPNKR_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPNKR_REDIRECT_URI"]
REFRESH_TOKEN = os.environ["SPNKR_REFRESH_TOKEN"]


async def main(xuids: list[str]) -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    async with ClientSession() as session:
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)
        spartan = player.spartan_token.token
        clearance = player.clearance_token.token
        client = HaloInfiniteClient(session, spartan, clearance)
        response = await client.get_users(xuids)
        data = await response.json()
        users = [User(**user) for user in data]
        for user in users:
            print(user.gamertag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("xuids", nargs="+")
    args = parser.parse_args()
    asyncio.run(main(args.xuids))
