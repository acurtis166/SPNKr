import asyncio
import os

import dotenv
import pytest
import pytest_asyncio
from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens
from spnkr.client import HaloInfiniteClient


@pytest_asyncio.fixture(scope="session")
async def authenticated_player():
    dotenv.load_dotenv()
    refresh_token = os.environ["SPNKR_REFRESH_TOKEN"]
    client_id = os.environ["SPNKR_CLIENT_ID"]
    client_secret = os.environ["SPNKR_CLIENT_SECRET"]
    redirect_uri = os.environ["SPNKR_REDIRECT_URI"]
    app = AzureApp(client_id, client_secret, redirect_uri)
    async with ClientSession() as session:
        return await refresh_player_tokens(session, app, refresh_token)


@pytest_asyncio.fixture(scope="session")
async def client(authenticated_player):
    """Return a client."""
    async with ClientSession() as session:
        yield HaloInfiniteClient(
            session=session,
            spartan_token=authenticated_player.spartan_token.token,
            clearance_token=authenticated_player.clearance_token.token,
        )


@pytest.fixture(scope="session")
def event_loop():
    """Redefine the event loop to be session-scoped."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
