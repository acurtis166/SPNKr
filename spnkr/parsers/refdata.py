"""Enumerated data types used by the Halo Infinite API."""

import math
from enum import IntEnum, StrEnum


class AssetKind(IntEnum):
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
    # TODO these are guesses
    NA = 0
    RECRUIT = 1
    MARINE = 2
    ODST = 3
    SPARTAN = 4


class GameVariantCategory(IntEnum):
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
    ESCORT = 23
    GUN_GAME = 24
    GRIFFBALL = 25
    TEST_ENGINE = 32
    LAND_GRAB = 39


class LifecycleMode(IntEnum):
    CUSTOM = 1
    MATCHMADE = 3


class Outcome(IntEnum):
    TIE = 1
    WIN = 2
    LOSS = 3
    DID_NOT_FINISH = 4


class PlayerType(IntEnum):
    HUMAN = 1
    BOT = 2


class PlaylistExperience(IntEnum):
    ARENA = 2
    BIG_TEAM_BATTLE = 3
    PVE = 4
    FEATURED = 5


class SkillResultCode(IntEnum):
    SUCCESS = 0


class SubTier(IntEnum):
    MISSING = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6


class Team(IntEnum):
    # TODO: Check if these are correct and add missing ones
    EAGLE = 0
    COBRA = 1


class Tier(StrEnum):
    MISSING = ""
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    DIAMOND = "Diamond"
    ONYX = "Onyx"


def get_tier_from_csr(csr: float) -> tuple[Tier, SubTier]:
    """Get the tier and sub-tier from a CSR value."""
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
        tier = Tier.ONYX
        remainder = 0  # Onyx doesn't have sub-tiers
    sub_tier = SubTier((remainder // 50) + 1)
    return tier, sub_tier
