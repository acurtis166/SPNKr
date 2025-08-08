"""Test the spnkr.parsers.refdata module."""

import pytest

from spnkr.models.refdata import MedalNameId, PersonalScoreNameId, SubTier

SUBTIER_VALUES = [
    (SubTier.I, 1),
    (SubTier.II, 2),
    (SubTier.III, 3),
    (SubTier.IV, 4),
    (SubTier.V, 5),
    (SubTier.VI, 6),
]


@pytest.mark.parametrize("subtier, value", SUBTIER_VALUES)
def test_subtier_from_int(subtier: SubTier, value: int):
    """Test the from_int method of the SubTier class."""
    assert SubTier.from_int(value) == subtier


@pytest.mark.parametrize("subtier, value", SUBTIER_VALUES)
def test_subtier_to_int(subtier: SubTier, value: int):
    """Test the as_int method of the SubTier class."""
    assert subtier.to_int() == value


def test_medal_display_name():
    result = MedalNameId.ACE
    assert result.display_name == "Ace"


def test_personal_score_display_name():
    result = PersonalScoreNameId.EMP_ASSIST
    assert result.display_name == "EMP Assist"
