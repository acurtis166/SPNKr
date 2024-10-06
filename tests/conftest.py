import asyncio

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Redefine the event loop to be session-scoped."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
