"""Test the spnkr.auth.xbox module."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest

from spnkr.auth import xbox

RESPONSES = Path("tests/data/responses")


class MockResponse:
    def __init__(self, json_data: Any):
        self.json_data = json_data

    async def json(self) -> Any:
        return self.json_data


class MockSession:
    def __init__(self, response: Any):
        self.post = AsyncMock(return_value=response)


def load_response(name: str) -> Any:
    with open(RESPONSES / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def test_xau_response_token():
    """Test that the user token value is returned."""
    response = load_response("xbox_user")
    user_token = xbox.XAUResponse(response)
    assert user_token.token == "abcdefg"


def test_xsts_response_token():
    """Test that the xsts token is returned."""
    response = load_response("xsts")
    xsts_token = xbox.XSTSResponse(response)
    assert xsts_token.token == "123456789"


def test_xsts_response_xui():
    """Test that the xbox user info is returned."""
    response = load_response("xsts")
    xsts_token = xbox.XSTSResponse(response)
    assert len(xsts_token.xui) == 7


def test_xsts_response_xuid():
    """Test that the xsts player id is returned."""
    response = load_response("xsts")
    xsts_token = xbox.XSTSResponse(response)
    assert xsts_token.xuid == "xuid(2669321029139235)"


def test_xsts_response_userhash():
    """Test that the xsts user hash is returned."""
    response = load_response("xsts")
    xsts_token = xbox.XSTSResponse(response)
    assert xsts_token.userhash == "abcdefg"


def test_xsts_response_gamertag():
    """Test that the xsts gamertag is returned."""
    response = load_response("xsts")
    xsts_token = xbox.XSTSResponse(response)
    assert xsts_token.gamertag == "e"


def test_xsts_response_authorization_header_value():
    """Test that the xsts gamertag is returned."""
    response = load_response("xsts")
    xsts_token = xbox.XSTSResponse(response)
    assert xsts_token.authorization_header_value == "XBL3.0 x=abcdefg;123456789"


@pytest.mark.asyncio
async def test_request_user_token():
    response = load_response("xbox_user")
    session = MockSession(MockResponse(response))
    token = await xbox.request_user_token(session, "test")  # type: ignore
    assert token.token == "abcdefg"


@pytest.mark.asyncio
async def test_request_user_token_called_with():
    session = MockSession(MockResponse({}))
    await xbox.request_user_token(session, "test")  # type: ignore
    session.post.assert_called_with(
        "https://user.auth.xboxlive.com/user/authenticate",
        json={
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": "d=test",
            },
        },
        headers={"x-xbl-contract-version": "1"},
    )


@pytest.mark.asyncio
async def test_request_xsts_token():
    response = load_response("xsts")
    session = MockSession(MockResponse(response))
    token = await xbox.request_xsts_token(session, "test", "party")  # type: ignore
    assert token.token == "123456789"


@pytest.mark.asyncio
async def test_request_xsts_token_called_with():
    session = MockSession(MockResponse({}))
    await xbox.request_xsts_token(session, "test", "party")  # type: ignore
    session.post.assert_called_with(
        "https://xsts.auth.xboxlive.com/xsts/authorize",
        json={
            "RelyingParty": "party",
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": ["test"],
                "SandboxId": "RETAIL",
            },
        },
        headers={"x-xbl-contract-version": "1"},
    )
