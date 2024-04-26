"""Test the spnkr.auth.oauth module."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession

from spnkr.auth import app, oauth
from spnkr.errors import OAuth2Error

RESPONSES = Path("tests/responses")


class MockResponse:
    def __init__(self, json_data: Any, ok: bool = True):
        self.json_data = json_data
        self.ok = ok

    async def json(self) -> Any:
        return self.json_data


class MockSession:
    def __init__(self, response: Any):
        self.response = response

    async def get(self, *args, **kwargs) -> Any:
        return self.response

    async def post(self, *args, **kwargs) -> Any:
        return self.response


@pytest.fixture
def azure_app():
    return app.AzureApp("client_id", "client_secret", "redirect_uri")


def load_response(name: str) -> Any:
    with open(RESPONSES / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def test_oauth2_token_access_token():
    """Test that the access token value is returned."""
    response = load_response("oauth2")
    oauth_token = oauth.OAuth2Token(response)
    assert oauth_token.access_token == "abcdefg"


def test_oauth2_token_refresh_token():
    """Test that the refresh token value is returned."""
    response = load_response("oauth2")
    oauth_token = oauth.OAuth2Token(response)
    assert oauth_token.refresh_token == "hijklmnop"


def test_generate_authorization_url(azure_app):
    """Test that the authorization URL is generated."""
    expected = (
        "https://login.live.com/oauth20_authorize.srf?"
        "client_id=client_id&"
        "response_type=code&"
        "approval_prompt=auto&"
        "scope=Xboxlive.signin+Xboxlive.offline_access&"
        "redirect_uri=redirect_uri"
    )
    assert oauth.generate_authorization_url(azure_app) == expected


@pytest.mark.asyncio
async def test_request_oauth_token(azure_app, monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr(oauth, "_oauth2_token_request", mock)
    expected_data = {
        "grant_type": "authorization_code",
        "code": "auth_code",
        "scope": "Xboxlive.signin Xboxlive.offline_access",
        "redirect_uri": "redirect_uri",
    }
    async with ClientSession() as session:
        await oauth.request_oauth_token(session, "auth_code", azure_app)

    mock.assert_called_with(session, expected_data, azure_app)


@pytest.mark.asyncio
async def test_refresh_oauth_token(azure_app, monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr(oauth, "_oauth2_token_request", mock)
    expected_data = {
        "grant_type": "refresh_token",
        "scope": "Xboxlive.signin Xboxlive.offline_access",
        "refresh_token": "rt",
    }
    async with ClientSession() as session:
        await oauth.refresh_oauth_token(session, "rt", azure_app)

    mock.assert_called_with(session, expected_data, azure_app)


@pytest.mark.asyncio
async def test_oauth_token_request(azure_app):
    response = load_response("oauth2")
    session = MockSession(MockResponse(response))
    token = await oauth._oauth2_token_request(session, {}, azure_app)  # type: ignore
    assert token.access_token == "abcdefg"


@pytest.mark.asyncio
async def test_oauth_token_error(azure_app):
    session = MockSession(MockResponse({"error": "invalid_grant"}, ok=False))
    with pytest.raises(OAuth2Error):
        await oauth._oauth2_token_request(session, {}, azure_app)  # type: ignore
