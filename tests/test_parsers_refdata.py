"""Test the spnkr.parsers.refdata module."""

import pytest

from spnkr.parsers.refdata import SubTier, Tier, get_tier_from_csr

TEST_DATA = [
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
    (1500, Tier.ONYX, SubTier.NOT_APPLICABLE),
    (3000, Tier.ONYX, SubTier.NOT_APPLICABLE),
]


@pytest.mark.parametrize("csr,tier,sub_tier", TEST_DATA)
def test_get_tier_from_csr(csr: float, tier: Tier, sub_tier: SubTier):
    """Test that the correct tier and sub-tier are returned."""
    assert get_tier_from_csr(csr) == (tier, sub_tier)
