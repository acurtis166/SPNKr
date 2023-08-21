"""Perform the initial authentication flow to obtain an OAuth2 refresh token."""

import asyncio
import os

import dotenv

from spnkr.auth import AzureApp, authenticate_player

dotenv.load_dotenv()

CLIENT_ID = os.environ["SPNKR_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPNKR_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPNKR_REDIRECT_URI"]


async def main() -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    refresh_token = await authenticate_player(app)
    print(f"Your refresh token is:\n{refresh_token}")


if __name__ == "__main__":
    asyncio.run(main())
