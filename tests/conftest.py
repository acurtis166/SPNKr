"""Configuration for pytest."""

from unittest.mock import AsyncMock

import pytest


class MockResponse:
    def raise_for_status(self) -> None:
        pass

    async def json(self) -> dict:
        return {}


class MockSession:
    def __init__(self) -> None:
        self.headers = {}
        self.get = AsyncMock()
        self.get.return_value = MockResponse()


@pytest.fixture
def session():
    return MockSession()
