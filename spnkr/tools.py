"""Tools for Halo Infinite data analysis."""

import math
from enum import IntEnum
from typing import NamedTuple

from spnkr.models.refdata import (
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
from spnkr.xuid import unwrap_xuid, wrap_xuid

__all__ = [
    "wrap_xuid",
    "unwrap_xuid",
    "BOT_DIFFICULTY_MAP",
    "BOT_MAP",
    "GAME_CATEGORY_MAP",
    "LIFECYCLE_MAP",
    "MEDAL_DIFFICULTY_MAP",
    "MEDAL_TYPE_MAP",
    "OUTCOME_MAP",
    "PLAYER_TYPE_MAP",
    "PLAYLIST_EXPERIENCE_MAP",
    "TEAM_MAP",
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
PLAYLIST_EXPERIENCE_MAP: dict[int, str] = _intenum_to_mapping(PlaylistExperience)
"""Mapping of playlist experience values to names."""
BOT_MAP: dict[str, str] = {
    "bid(1.0)": "343 Connmando",
    "bid(2.0)": "343 Beard",
    "bid(3.0)": "343 Aloysius",
    "bid(4.0)": "343 Lemondade",
    "bid(5.0)": "343 Cream Corn",
    "bid(6.0)": "343 Rhinosaurus",
    "bid(7.0)": "343 Oscar",
    "bid(8.0)": "343 Marmot",
    "bid(9.0)": "343 Chilies",
    "bid(10.0)": "343 Cliffton",
    "bid(11.0)": "343 Ensrude",
    "bid(12.0)": "343 Godfather",
    "bid(13.0)": "343 Ritzy",
    "bid(14.0)": "343 Darkstar",
    "bid(15.0)": "343 Ham Sammich",
    "bid(16.0)": "343 Meowlnir",
    "bid(17.0)": "343 PardonMy",
    "bid(18.0)": "343 Mak",
    "bid(19.0)": "343 Ellis",
    "bid(20.0)": "343 Robot Hoida",
    "bid(21.0)": "343 Bergerton",
    "bid(22.0)": "343 Tedosaur",
    "bid(23.0)": "343 Cosmo",
    "bid(24.0)": "343 Shady Seal",
    "bid(25.0)": "343 Mumblebee",
    "bid(26.0)": "343 Total Ten",
    "bid(27.0)": "343 Byrontron",
    "bid(28.0)": "343 Forge Lord",
    "bid(29.0)": "343 Mickey",
    "bid(30.0)": "343 Lacuna",
    "bid(31.0)": "343 Hundy",
    "bid(32.0)": "343 Nando",
    "bid(33.0)": "343 Free Money",
    "bid(34.0)": "343 BF Scrub",
    "bid(35.0)": "343 Zero",
    "bid(36.0)": "343 Wiggle Cat",
    "bid(37.0)": "343 Brew Dog",
    "bid(38.0)": "343 The Thumb",
    "bid(39.0)": "343 Flippant",
    "bid(40.0)": "343 Donos",
    "bid(41.0)": "343 O Freruner",
    "bid(42.0)": "343 Tanuki",
    "bid(43.0)": "343 SpaceCase",
    "bid(44.0)": "343 GrappleMans",
    "bid(45.0)": "343 BERRYHILL",
    "bid(46.0)": "343 TooMilks",
    "bid(47.0)": "343 KaleDucky",
    "bid(48.0)": "343 BoboGan",
    "bid(49.0)": "343 Chaco",
    "bid(50.0)": "343 Colson",
    "bid(51.0)": "343 Ben Desk",
    "bid(52.0)": "343 The Referee",
    "bid(53.0)": "343 Doomfruit",
    "bid(54.0)": "343 Stone",
    "bid(55.0)": "343 Hollis",
    "bid(56.0)": "343 Razzle",
    "bid(57.0)": "343 Dazzle",
    "bid(58.0)": "343 Bachici",
    "bid(59.0)": "343 Sandwolf",
    "bid(60.0)": "343 Kubly",
}
"""Mapping of bot IDs to names. For example, 'bid(1.0)' -> '343 Connmando'."""
TEAM_MAP: dict[int, str] = {
    0: "Eagle",
    1: "Cobra",
    2: "Hades",
    3: "Valkyrie",
    4: "Rampart",
    5: "Cutlass",
    6: "Valor",
    7: "Hazard",
    8: "Observer",
}
"""Mapping of team IDs to names. For example, 0 -> 'Eagle'."""


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
