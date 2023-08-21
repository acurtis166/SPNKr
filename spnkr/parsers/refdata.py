"""Enumerated data types used by the Halo Infinite API."""

import math
from enum import IntEnum, StrEnum


class AssetKind(IntEnum):
    """Types of assets used by Halo Infinite."""

    FILM = 1
    MAP = 2
    PLAYLIST = 3
    PREFAB = 4
    TEST_ASSET = 5
    UGC_GAME_VARIANT = 6
    MAP_MODE_PAIR = 7
    PROJECT = 8
    MANIFEST = 9
    ENGINE_GAME_VARIANT = 10


class BotDifficulty(IntEnum):
    """Bot difficulty levels."""

    # TODO these are guesses
    NOT_APPLICABLE = 0
    RECRUIT = 1
    MARINE = 2
    ODST = 3
    SPARTAN = 4


class GameVariantCategory(IntEnum):
    """Categories of multiplayer game modes."""

    SLAYER = 6
    ATTRITION = 7
    ELIMINATION = 8
    FIESTA = 9
    STRONGHOLDS = 11
    BASTION = 12
    TOTAL_CONTROL = 14
    CTF = 15
    ASSAULT = 16
    EXTRACTION = 17
    ODDBALL = 18
    STOCKPILE = 19
    JUGGERNAUT = 20
    GVC_22 = 22  # TODO: What is this?
    ESCORT = 23
    GUN_GAME = 24
    GRIFBALL = 25
    TEST_ENGINE = 32
    LAND_GRAB = 39


class LifecycleMode(IntEnum):
    """General categories of game modes."""

    CUSTOM = 1
    MATCHMADE = 3


class MedalDifficulty(IntEnum):
    """Difficulty of medals obtainable in matchmaking.

    Values line up to indices in the medal metadata response content.
    """

    NORMAL = 0
    HEROIC = 1
    LEGENDARY = 2
    MYTHIC = 3


class MedalType(IntEnum):
    """Types of medals obtainable in matchmaking.

    Values line up to indices in the medal metadata response content.
    """

    SPREE = 0
    MODE = 1
    MULTIKILL = 2
    PROFICIENCY = 3
    SKILL = 4
    STYLE = 5


class Outcome(IntEnum):
    """Match outcome options."""

    TIE = 1
    WIN = 2
    LOSS = 3
    DID_NOT_FINISH = 4


class PlayerType(IntEnum):
    """Types of players."""

    HUMAN = 1
    BOT = 2


class PlaylistExperience(IntEnum):
    """General categories of playlists."""

    ARENA = 2
    BIG_TEAM_BATTLE = 3
    PVE = 4
    FEATURED = 5


class SkillResultCode(IntEnum):
    """Result codes for skill requests."""

    SUCCESS = 0
    # TODO: Need to add the rest of these


class SubTier(IntEnum):
    """Sub-tiers of skill rankings."""

    NOT_APPLICABLE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6


class Tier(StrEnum):
    """Tiers of skill rankings."""

    NOT_APPLICABLE = ""
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    DIAMOND = "Diamond"
    ONYX = "Onyx"


def get_tier_from_csr(csr: float) -> tuple[Tier, SubTier]:
    """Get the tier and sub-tier from a CSR value.

    Args:
        csr: CSR value to convert.

    Returns:
        A tuple containing the tier and sub-tier.
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
        return Tier.ONYX, SubTier.NOT_APPLICABLE  # Onyx doesn't have sub-tiers
    sub_tier = SubTier((remainder // 50) + 1)
    return tier, sub_tier
