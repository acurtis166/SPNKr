"""Configuration for pytest."""

import json
from typing import Any
from unittest.mock import AsyncMock

import pytest


class MockResponse:
    def __init__(self, data) -> None:
        self._data = data

    def raise_for_status(self) -> None:
        pass

    async def read(self) -> bytes:
        return self._data

    async def json(self) -> Any:
        return json.loads(self._data)


class MockSession:
    def __init__(self) -> None:
        self.headers = {}
        self.get = AsyncMock()
        self.get.return_value = MockResponse({})

    def set_response(self, file_name: str) -> None:
        """Set the response for the next GET request."""
        with open(f"tests/responses/{file_name}", "rb") as f:
            self.get.return_value = MockResponse(f.read())


@pytest.fixture
def session():
    return MockSession()


@pytest.fixture
def response():
    return MockResponse(b"{}")
