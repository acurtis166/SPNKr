"""Test the spnkr.parsers.refdata module."""

import pytest

from spnkr.parsers.refdata import SubTier

SUBTIER_VALUES = [
    (SubTier.ONE, 1),
    (SubTier.TWO, 2),
    (SubTier.THREE, 3),
    (SubTier.FOUR, 4),
    (SubTier.FIVE, 5),
    (SubTier.SIX, 6),
]


@pytest.mark.parametrize("subtier, value", SUBTIER_VALUES)
def test_subtier_from_int(subtier: SubTier, value: int):
    """Test the from_int method of the SubTier class."""
    assert SubTier.from_int(value) == subtier


@pytest.mark.parametrize("subtier, value", SUBTIER_VALUES)
def test_subtier_to_int(subtier: SubTier, value: int):
    """Test the as_int method of the SubTier class."""
    assert subtier.to_int() == value
