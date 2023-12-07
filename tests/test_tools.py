"""Test the spnkr.tools module."""

from enum import IntEnum

import pytest

from spnkr import tools
from spnkr.models.refdata import SubTier, Tier

CSR_TIERS = [
    (0, Tier.BRONZE, SubTier.ONE),
    (299, Tier.BRONZE, SubTier.SIX),
    (300, Tier.SILVER, SubTier.ONE),
    (599, Tier.SILVER, SubTier.SIX),
    (600, Tier.GOLD, SubTier.ONE),
    (899, Tier.GOLD, SubTier.SIX),
    (900, Tier.PLATINUM, SubTier.ONE),
    (1199, Tier.PLATINUM, SubTier.SIX),
    (1200, Tier.DIAMOND, SubTier.ONE),
    (1499, Tier.DIAMOND, SubTier.SIX),
    (1500, Tier.ONYX, SubTier.ONE),
    (3000, Tier.ONYX, SubTier.ONE),
]


def test_ranking_str():
    """Test the __str__ method of the Rank class."""
    ranking = tools.Rank(Tier.BRONZE, SubTier.ONE)
    assert str(ranking) == "Bronze 1"


def test_ranking_str_onyx():
    """Test the __str__ method of the Rank class when the tier is Onyx."""
    ranking = tools.Rank(Tier.ONYX, SubTier.ONE)
    assert str(ranking) == "Onyx"


@pytest.mark.parametrize("csr,tier,sub_tier", CSR_TIERS)
def test_get_rank_from_csr(csr: float, tier: Tier, sub_tier: SubTier):
    """Test that the correct tier and sub-tier are returned."""
    assert tools.get_rank_from_csr(csr) == (tier, sub_tier)


def test_intenum_to_mapping():
    """Test the _intenum_to_mapping function."""

    class TestEnum(IntEnum):
        A = 1
        B = 2
        C = 3

    assert tools._intenum_to_mapping(TestEnum) == {1: "A", 2: "B", 3: "C"}
