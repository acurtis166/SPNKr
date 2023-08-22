"""Test the spnkr.auth.core module."""

import pytest

from spnkr.auth import app, core


def test_authenticate_player():
    ...


def test_get_authorization_code(monkeypatch):
    """Test that the user-inputted code is returned."""
    azure_app = app.AzureApp("test_client_id", "test_client_secret")
    monkeypatch.setattr("builtins.input", lambda _: " test_code ")
    assert core._get_authorization_code(azure_app) == "test_code"


def test_refresh_player_tokens():
    ...
