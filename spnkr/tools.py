"""Tools for Halo Infinite data analysis."""

import math
from enum import IntEnum
from typing import NamedTuple

from .parsers.refdata import (
    BotDifficulty,
    GameVariantCategory,
    LifecycleMode,
    MedalDifficulty,
    MedalType,
    Outcome,
    PlayerType,
    PlaylistExperience,
    SubTier,
    Tier,
)
from .xuid import unwrap_xuid, wrap_xuid

__all__ = [
    "wrap_xuid",
    "unwrap_xuid",
    "BOT_DIFFICULTY_MAP",
    "GAME_CATEGORY_MAP",
    "LIFECYCLE_MAP",
    "MEDAL_DIFFICULTY_MAP",
    "MEDAL_TYPE_MAP",
    "OUTCOME_MAP",
    "PLAYER_TYPE_MAP",
    "PLAYLIST_EXPERIENCE_MAP",
    "get_rank_from_csr",
    "Rank",
]


def _intenum_to_mapping(enum: type[IntEnum]) -> dict[int, str]:
    """Create a dict of value to name for an `IntEnum`."""
    return {e.value: e.name for e in enum}


BOT_DIFFICULTY_MAP: dict[int, str] = _intenum_to_mapping(BotDifficulty)
"""Mapping of bot difficulty values to names."""
GAME_CATEGORY_MAP: dict[int, str] = _intenum_to_mapping(GameVariantCategory)
"""Mapping of game variant category values to names."""
LIFECYCLE_MAP: dict[int, str] = _intenum_to_mapping(LifecycleMode)
"""Mapping of lifecycle mode values to names."""
MEDAL_DIFFICULTY_MAP: dict[int, str] = _intenum_to_mapping(MedalDifficulty)
"""Mapping of medal difficulty values to names."""
MEDAL_TYPE_MAP: dict[int, str] = _intenum_to_mapping(MedalType)
"""Mapping of medal type values to names."""
OUTCOME_MAP: dict[int, str] = _intenum_to_mapping(Outcome)
"""Mapping of match outcome values to names."""
PLAYER_TYPE_MAP: dict[int, str] = _intenum_to_mapping(PlayerType)
"""Mapping of player type values to names."""
PLAYLIST_EXPERIENCE_MAP: dict[int, str] = _intenum_to_mapping(
    PlaylistExperience
)
"""Mapping of playlist experience values to names."""


class Rank(NamedTuple):
    """A CSR tier and sub-tier.

    Attributes:
        tier: CSR tier.
        sub_tier: CSR sub-tier.
    """

    tier: Tier
    sub_tier: SubTier

    def __str__(self) -> str:
        if self.tier is Tier.ONYX:
            return self.tier.value
        return f"{self.tier.value} {self.sub_tier.to_int()}"


def get_rank_from_csr(csr: int | float) -> Rank:
    """Get the tier and sub-tier from a CSR value.

    Args:
        csr: CSR value to convert.

    Returns:
        A ranking named tuple containing `tier` and `subtier`.
    """
    csr = math.floor(csr)
    quotient, remainder = divmod(csr, 300)
    if quotient == 0:
        tier = Tier.BRONZE
    elif quotient == 1:
        tier = Tier.SILVER
    elif quotient == 2:
        tier = Tier.GOLD
    elif quotient == 3:
        tier = Tier.PLATINUM
    elif quotient == 4:
        tier = Tier.DIAMOND
    else:
        return Rank(Tier.ONYX, SubTier.ONE)
    sub_tier = SubTier.from_int((remainder // 50) + 1)
    return Rank(tier, sub_tier)
