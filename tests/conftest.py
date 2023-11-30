"""Configuration for pytest."""

from unittest.mock import AsyncMock

import pytest


class MockSession:
    def __init__(self) -> None:
        self.headers = {}
        self.get = AsyncMock()


@pytest.fixture
def session():
    return MockSession()
