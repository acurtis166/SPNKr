"""Enumerated data types used by the Halo Infinite API."""

from enum import IntEnum, StrEnum


class AssetKind(IntEnum):
    """Types of assets used by Halo Infinite."""

    FILM = 1
    """A film asset."""
    MAP = 2
    """A map asset."""
    PLAYLIST = 3
    """A matchmaking playlist asset."""
    PREFAB = 4
    """A prefabricated object asset."""
    TEST_ASSET = 5
    """A test asset."""
    UGC_GAME_VARIANT = 6
    """A user-generated content game mode asset."""
    MAP_MODE_PAIR = 7
    """A map and game mode pair asset."""
    PROJECT = 8
    """A project asset."""
    MANIFEST = 9
    """A manifest asset."""
    ENGINE_GAME_VARIANT = 10
    """An engine game mode asset."""


class BotDifficulty(IntEnum):
    """Bot difficulty levels."""

    RECRUIT = 4
    """Recruit bots. Lowest difficulty."""
    MARINE = 1
    """Marine bots. 2nd lowest difficulty."""
    ODST = 2
    """ODST bots. 2nd highest difficulty."""
    SPARTAN = 3
    """Spartan bots. Highest difficulty."""


class GameVariantCategory(IntEnum):
    """Categories of multiplayer game modes."""

    SLAYER = 6
    """Slayer game modes."""
    ATTRITION = 7
    """Attrition game modes."""
    ELIMINATION = 8
    """Elimination game modes."""
    FIESTA = 9
    """Fiesta game modes."""
    STRONGHOLDS = 11
    """Strongholds game modes."""
    BASTION = 12
    """Bastion game modes."""
    TOTAL_CONTROL = 14
    """Total Control game modes."""
    CTF = 15
    """Capture the Flag game modes."""
    ASSAULT = 16
    """Assault game modes."""
    EXTRACTION = 17
    """Extraction game modes."""
    ODDBALL = 18
    """Oddball game modes."""
    STOCKPILE = 19
    """Stockpile game modes."""
    JUGGERNAUT = 20
    """Juggernaut game modes."""
    INFECTION = 22
    """Infection game modes."""
    ESCORT = 23
    """Escort game modes."""
    GUN_GAME = 24
    """Gun Game game modes."""
    GRIFBALL = 25
    """Grifball game modes."""
    TEST_ENGINE = 32
    """Test Engine game modes."""
    LAND_GRAB = 39
    """Land Grab game modes."""


class LifecycleMode(IntEnum):
    """General categories of game modes."""

    CUSTOM = 1
    """Custom games."""
    MATCHMADE = 3
    """Matchmade games."""


class MedalDifficulty(IntEnum):
    """Difficulty of medals obtainable in matchmaking."""

    # Values line up to indices in the medal metadata response content.
    NORMAL = 0
    """Normal difficulty medals. Easiest to obtain."""
    HEROIC = 1
    """Heroic difficulty medals. 2nd easiest to obtain."""
    LEGENDARY = 2
    """Legendary difficulty medals. 2nd hardest to obtain."""
    MYTHIC = 3
    """Mythic difficulty medals. Hardest to obtain."""


class MedalType(IntEnum):
    """Types of medals obtainable in matchmaking."""

    # Values line up to indices in the medal metadata response content.
    SPREE = 0
    """General or weapon-specific killing sprees."""
    MODE = 1
    """Game mode-specific medals."""
    MULTIKILL = 2
    """Kill multiple enemies in quick succession."""
    PROFICIENCY = 3
    """Medals related to player proficiency."""
    SKILL = 4
    """Medals awarded for skillful play."""
    STYLE = 5
    """Medals awarded for stylish play."""


class Outcome(IntEnum):
    """Match outcome options."""

    TIE = 1
    """Match ended in a tie."""
    WIN = 2
    """Match was won."""
    LOSS = 3
    """Match was lost."""
    DID_NOT_FINISH = 4
    """Match was not finished."""


class PlayerType(IntEnum):
    """Types of players."""

    HUMAN = 1
    """Human players."""
    BOT = 2
    """AI players."""


class PlaylistExperience(IntEnum):
    """General categories of playlists."""

    ARENA = 2
    """Arena playlists. Typically 4v4."""
    BIG_TEAM_BATTLE = 3
    """Big team battle playlists. Typically 12v12."""
    PVE = 4
    """Player vs. environment playlists."""
    FEATURED = 5
    """Featured playlists. Rotates frequently."""


class SkillResultCode(IntEnum):
    """Result codes for skill requests."""

    SUCCESS = 0
    """Skill request was successful."""


class SubTier(IntEnum):
    """Sub-tiers of skill rankings."""

    NOT_APPLICABLE = 0
    """Not applicable."""
    ONE = 1
    """1st sub-tier."""
    TWO = 2
    """2nd sub-tier."""
    THREE = 3
    """3rd sub-tier."""
    FOUR = 4
    """4th sub-tier."""
    FIVE = 5
    """5th sub-tier."""
    SIX = 6
    """6th sub-tier. Highest sub-tier before advancing to the next tier."""


class Tier(StrEnum):
    """Tiers of skill rankings."""

    NOT_APPLICABLE = ""
    """Not applicable."""
    BRONZE = "Bronze"
    """Bronze tier. Lowest tier."""
    SILVER = "Silver"
    """Silver tier."""
    GOLD = "Gold"
    """Gold tier."""
    PLATINUM = "Platinum"
    """Platinum tier."""
    DIAMOND = "Diamond"
    """Diamond tier."""
    ONYX = "Onyx"
    """Onyx tier. Highest tier."""
