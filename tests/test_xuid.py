"""Test the spnkr.xuid module."""

import pytest

from spnkr.xuid import unwrap_xuid, wrap_xuid

WRAPPABLE = [
    ("1234567890", "xuid(1234567890)"),
    ("xuid(1234567890)", "xuid(1234567890)"),
    (1234567890, "xuid(1234567890)"),
]
UNWRAPPABLE = [
    ("1234567890", 1234567890),
    ("xuid(1234567890)", 1234567890),
    (1234567890, 1234567890),
]
INVALID = ["1234y567890", "(123)", "xuid(1234567890x)", "bid(1234567890)"]


@pytest.mark.parametrize("value, expected", WRAPPABLE)
def test_wrap_xuid(value: str | int, expected: str):
    """Test that the XUID is wrapped."""
    assert wrap_xuid(value) == expected


@pytest.mark.parametrize("value, expected", UNWRAPPABLE)
def test_unwrap_xuid(value: str | int, expected: int):
    """Test that the XUID is unwrapped."""
    assert unwrap_xuid(value) == expected


@pytest.mark.parametrize("value", INVALID)
def test_unwrap_xuid_invalid(value: str | int):
    """Test that invalid XUIDs raise an error."""
    with pytest.raises(ValueError):
        unwrap_xuid(value)
