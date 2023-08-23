"""Enumerated data types used by the Halo Infinite API."""

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

    # TODO try creating custom games with different bot difficulties to confirm
    RECRUIT = 0
    MARINE = 1
    ODST = 2
    SPARTAN = 3


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
    INFECTION = 22
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
