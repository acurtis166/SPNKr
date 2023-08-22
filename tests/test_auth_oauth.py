"""Test the spnkr.auth.oauth module."""

import json
from pathlib import Path
from typing import Any

import pytest

from spnkr.auth import oauth

RESPONSES = Path("tests/responses")


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


def test_generate_authorization_url():
    """Test that the authorization URL is generated."""
    azure_app = oauth.AzureApp("client_id", "client_secret", "redirect_uri")
    expected = (
        "https://login.live.com/oauth20_authorize.srf?"
        "client_id=client_id&"
        "response_type=code&"
        "approval_prompt=auto&"
        "scope=Xboxlive.signin+Xboxlive.offline_access&"
        "redirect_uri=redirect_uri"
    )
    assert oauth.generate_authorization_url(azure_app) == expected


def test_request_oauth_token():
    ...


def test_refresh_oauth_token():
    ...


def test_oauth_token_request():
    ...
