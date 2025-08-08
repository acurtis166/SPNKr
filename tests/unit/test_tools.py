"""Test the spnkr.tools module."""

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


@pytest.mark.parametrize("csr,tier,sub_tier", CSR_TIERS)
def test_rank_init(csr: float, tier: Tier, sub_tier: SubTier):
    """Test that the correct tier and sub-tier are returned."""
    result = tools.CompetitiveSkillRank(csr)
    assert result.tier == tier
    assert result.sub_tier == sub_tier


def test_rank_str_low():
    """Test the __str__ method of the Rank class."""
    ranking = tools.CompetitiveSkillRank(25)
    assert str(ranking) == "Bronze I"


def test_rank_str_high():
    """Test the __str__ method of the Rank class."""
    ranking = tools.CompetitiveSkillRank(1475)
    assert str(ranking) == "Diamond VI"


def test_rank_str_onyx():
    """Test the __str__ method of the Rank class when the tier is Onyx."""
    ranking = tools.CompetitiveSkillRank(1550)
    assert str(ranking) == "Onyx"
