"""Test the spnkr.auth.halo module."""

import datetime as dt
import json
from pathlib import Path
from typing import Any

import pytest

from spnkr.auth import halo

RESPONSES = Path("tests/responses")


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


def test_request_spartan_token():
    ...


def test_request_clearance_token():
    ...
