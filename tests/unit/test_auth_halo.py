"""Test the spnkr.auth.halo module."""

import datetime as dt
import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest

from spnkr.auth import halo

RESPONSES = Path("tests/data/responses")


class MockResponse:
    def __init__(self, json_data: Any):
        self.json_data = json_data

    async def json(self) -> Any:
        return self.json_data


class MockSession:
    def __init__(self, response: Any):
        self.get = AsyncMock(return_value=response)
        self.post = AsyncMock(return_value=response)


def load_response(name: str) -> Any:
    with open(RESPONSES / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def test_spartan_token_token():
    """Test that the spartan token is returned."""
    response = load_response("spartan")
    spartan_token = halo.SpartanToken(response)
    assert spartan_token.token == "abcdef"


def test_spartan_token_expires_at():
    """Test that the expiration datetime is returned."""
    response = load_response("spartan")
    spartan_token = halo.SpartanToken(response)
    expected = dt.datetime(2999, 1, 27, 5, 3, 47, tzinfo=dt.timezone.utc)
    assert spartan_token.expires_at == expected


def test_clearance_token_token():
    """Test that the clearance token is returned."""
    response = load_response("clearance")
    clearance_token = halo.ClearanceToken(response)
    assert clearance_token.token == "xyz"


@pytest.mark.asyncio
async def test_request_spartan_token():
    """Test that a spartan token is returned."""
    response = load_response("spartan")
    session = MockSession(MockResponse(response))
    token = await halo.request_spartan_token(session, "test")  # type: ignore
    assert token.token == "abcdef"


@pytest.mark.asyncio
async def test_request_spartan_token_called_with():
    session = MockSession(MockResponse({}))
    await halo.request_spartan_token(session, "test")  # type: ignore
    session.post.assert_called_with(
        "https://settings.svc.halowaypoint.com/spartan-token",
        json={
            "Audience": "urn:343:s3:services",
            "MinVersion": "4",
            "Proof": [
                {
                    "Token": "test",
                    "TokenType": "Xbox_XSTSv3",
                }
            ],
        },
        headers={"Accept": "application/json"},
    )


@pytest.mark.asyncio
async def test_request_clearance_token():
    """Test that a clearance token is returned."""
    response = load_response("clearance")
    session = MockSession(MockResponse(response))
    token = await halo.request_clearance_token(session, "test")  # type: ignore
    assert token.token == "xyz"


@pytest.mark.asyncio
async def test_request_clearance_token_called_with():
    session = MockSession(MockResponse({}))
    await halo.request_clearance_token(session, "test")  # type: ignore
    session.get.assert_called_with(
        "https://settings.svc.halowaypoint.com/oban/flight-configurations/titles/hi/audiences/RETAIL/active",
        headers={"x-343-authorization-spartan": "test"},
    )
