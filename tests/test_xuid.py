"""Test the spnkr.xuid module."""

import pytest

from spnkr.errors import InvalidXuidError
from spnkr.xuid import unwrap_xuid, wrap_xuid

WRAPPABLE = [
    ("1234567890123456", "xuid(1234567890123456)"),
    ("xuid(1234567890123456)", "xuid(1234567890123456)"),
    (1234567890123456, "xuid(1234567890123456)"),
]
UNWRAPPABLE = [
    ("1234567890123456", 1234567890123456),
    ("xuid(1234567890123456)", 1234567890123456),
    (1234567890123456, 1234567890123456),
]
INVALID = [
    123456789012345,
    "123456789012345",
    12345678901234567,
    "12345678901234567",
    "1234y567890",
    "(123)",
    "xuid(1234567890x)",
    "bid(1234567890)",
    "",
    " ",
    "xuid()",
    "xuid(1234567890123456]",
]


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
    with pytest.raises(InvalidXuidError):
        unwrap_xuid(value)
