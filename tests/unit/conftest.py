"""Configuration for pytest."""

from unittest.mock import AsyncMock

import pytest


class MockResponse:
    def __init__(self, data) -> None:
        self._data = data

    def raise_for_status(self) -> None:
        pass


class MockSession:
    def __init__(self) -> None:
        self.headers = {}
        self.get = AsyncMock()
        self.get.return_value = MockResponse({})
        self.request = AsyncMock()
        self.request.return_value = MockResponse({})


@pytest.fixture
def session():
    return MockSession()
