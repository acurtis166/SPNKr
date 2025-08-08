"""Test the spnkr.extras module."""

import pytest

from spnkr import extras
from spnkr.models.refdata import SubTier, Tier

CSR_TIERS = [
    (0, Tier.BRONZE, SubTier.I),
    (299, Tier.BRONZE, SubTier.VI),
    (300, Tier.SILVER, SubTier.I),
    (599, Tier.SILVER, SubTier.VI),
    (600, Tier.GOLD, SubTier.I),
    (899, Tier.GOLD, SubTier.VI),
    (900, Tier.PLATINUM, SubTier.I),
    (1199, Tier.PLATINUM, SubTier.VI),
    (1200, Tier.DIAMOND, SubTier.I),
    (1499, Tier.DIAMOND, SubTier.VI),
    (1500, Tier.ONYX, SubTier.I),
    (3000, Tier.ONYX, SubTier.I),
]


@pytest.mark.parametrize("csr,tier,sub_tier", CSR_TIERS)
def test_rank_init(csr: float, tier: Tier, sub_tier: SubTier):
    """Test that the correct tier and sub-tier are returned."""
    result = extras.CompetitiveSkillRank(csr)
    assert result.tier == tier
    assert result.sub_tier == sub_tier


def test_rank_str_low():
    """Test the __str__ method of the Rank class."""
    ranking = extras.CompetitiveSkillRank(25)
    assert str(ranking) == "Bronze I"


def test_rank_str_high():
    """Test the __str__ method of the Rank class."""
    ranking = extras.CompetitiveSkillRank(1475)
    assert str(ranking) == "Diamond VI"


def test_rank_str_onyx():
    """Test the __str__ method of the Rank class when the tier is Onyx."""
    ranking = extras.CompetitiveSkillRank(1550)
    assert str(ranking) == "Onyx"
