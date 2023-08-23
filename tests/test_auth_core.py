"""Test the spnkr.auth.core module."""

import asyncio

import pytest
from aiohttp import ClientSession

from spnkr.auth import app, core, halo, oauth, xbox


@pytest.fixture
def azure_app():
    return app.AzureApp("test_client_id", "test_client_secret")


@pytest.fixture
async def session():
    async with ClientSession() as session:
        yield session


def create_future(result):
    future = asyncio.Future()
    future.set_result(result)
    return future


class MockToken:
    def __init__(self, **kwargs):
        self.attrs = kwargs

    def __getattr__(self, name):
        return self.attrs[name]


@pytest.mark.asyncio
async def test_authenticate_player(session, azure_app, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: " test_code ")
    token = oauth.OAuth2Token({"refresh_token": "test_refresh_token"})
    future = create_future(token)
    monkeypatch.setattr(oauth, "request_oauth_token", lambda *args: future)
    refresh_token = await core.authenticate_player(session, azure_app)
    assert refresh_token == "test_refresh_token"


def test_get_authorization_code(azure_app, monkeypatch):
    """Test that the user-inputted code is returned."""
    monkeypatch.setattr("builtins.input", lambda _: " test_code ")
    assert core._get_authorization_code(azure_app) == "test_code"


@pytest.mark.asyncio
async def test_refresh_player_tokens(session, azure_app, monkeypatch):
    monkeypatch.setattr(
        oauth,
        "refresh_oauth_token",
        lambda *a: create_future(MockToken(access_token="test1")),
    )
    monkeypatch.setattr(
        xbox,
        "request_user_token",
        lambda *a: create_future(MockToken(token="test2")),
    )
    monkeypatch.setattr(
        xbox,
        "request_xsts_token",
        lambda *a: create_future(
            MockToken(
                token="test3",
                xuid="xuid(123)",
                gamertag="MrChief",
                authorization_header_value="X 123;ABC",
            )
        ),
    )
    monkeypatch.setattr(
        halo,
        "request_spartan_token",
        lambda *a: create_future(MockToken(token="test4")),
    )
    monkeypatch.setattr(
        halo,
        "request_clearance_token",
        lambda *a: create_future(MockToken(token="test5")),
    )
    player = await core.refresh_player_tokens(session, "rt", azure_app)
    assert player.player_id == "xuid(123)"
    assert player.gamertag == "MrChief"
    assert player.spartan_token.token == "test4"
    assert player.clearance_token.token == "test5"
    assert player.xbl_authorization_header_value == "X 123;ABC"
