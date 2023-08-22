"""Test the spnkr.auth.xbox module."""

import json
from pathlib import Path
from typing import Any

import pytest

from spnkr.auth import xbox

RESPONSES = Path("tests/responses")


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


def test_request_user_token():
    ...


def test_request_xsts_token():
    ...
