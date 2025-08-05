"""Enumerated data types used by the Halo Infinite API."""

import logging
from enum import Enum, IntEnum, StrEnum

logger = logging.getLogger(__name__)


class AssetHome(IntEnum):
    """Source of an asset."""

    UNKNOWN = 0
    STUDIO = 1
    PLAYER = 2


class AssetKind(IntEnum):
    """Types of assets used by Halo Infinite."""

    UNKNOWN = 0
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
    """Bot difficulty levels as encoded in stats responses."""

    UNKNOWN = -1
    MARINE = 1
    ODST = 2
    SPARTAN = 3
    RECRUIT = 4
    ADAPTIVE = 5


class CloneBehavior(IntEnum):
    """Permission levels for cloning assets."""

    DEFAULT = 0
    TEMPLATE = 1
    PROHIBITED = 2


class FilmChunkType(IntEnum):
    """Types of saved film chunks."""

    NONE = 0
    FILM_HEADER = 1
    REPLICATION_DATA = 2
    HIGHLIGHT_EVENTS = 3


class FilmStatus(IntEnum):
    """Status of a saved film."""

    UNKNOWN = 0
    COMPLETE = 1
    ONGOING = 2
    RECOVERED = 3


class GameplayInteraction(IntEnum):
    """Types of enemies interacted with in-game."""

    # Retrieved from JavaScript files in Waypoint network traffic.
    UNKNOWN = -1
    NONE = 0
    PVP = 1
    PVE = 2
    PVPVE = 3


class GameVariantCategory(IntEnum):
    """Game mode category enumeration."""

    UNKNOWN = -1
    NONE = 0
    CAMPAIGN = 1
    FORGE = 2
    ACADEMY = 3
    ACADEMY_TUTORIAL = 4
    ACADEMY_PRACTICE = 5
    MULTIPLAYER_SLAYER = 6
    MULTIPLAYER_ATTRITION = 7
    MULTIPLAYER_ELIMINATION = 8
    MULTIPLAYER_FIESTA = 9
    MULTIPLAYER_SWAT = 10
    MULTIPLAYER_STRONGHOLDS = 11
    MULTIPLAYER_BASTION = 12
    MULTIPLAYER_KING_OF_THE_HILL = 13
    MULTIPLAYER_TOTAL_CONTROL = 14
    MULTIPLAYER_CTF = 15
    MULTIPLAYER_ASSAULT = 16
    MULTIPLAYER_EXTRACTION = 17
    MULTIPLAYER_ODDBALL = 18
    MULTIPLAYER_STOCKPILE = 19
    MULTIPLAYER_JUGGERNAUT = 20
    MULTIPLAYER_REGICIDE = 21
    MULTIPLAYER_INFECTION = 22
    MULTIPLAYER_ESCORT = 23
    MULTIPLAYER_GUN_GAME = 24
    MULTIPLAYER_GRIFBALL = 25
    MULTIPLAYER_RACE = 26
    MULTIPLAYER_PROTOTYPE = 27
    TEST = 28
    TEST_ACADEMY = 29
    TEST_AUDIO = 30
    TEST_CAMPAIGN = 31
    TEST_ENGINE = 32
    TEST_FORGE = 33
    TEST_GRAPHICS = 34
    TEST_MULTIPLAYER = 35
    TEST_SANDBOX = 36
    ACADEMY_TRAINING = 37
    ACADEMY_WEAPON_DRILL = 38
    MULTIPLAYER_LAND_GRAB = 39
    MULTIPLAYER_MINIGAME = 41
    MULTIPLAYER_FIREFIGHT = 42


class InspectionResult(IntEnum):
    """Related to readiness of user-generated content?"""

    UNKNOWN = 0
    TOLERABLE = 5
    STUDIO_CONTENT = 50


class LifecycleMode(IntEnum):
    """General categories of game modes."""

    CUSTOM = 1
    MATCHMADE = 3
    LOCAL_AREA_NETWORK = 7


class MedalDifficulty(IntEnum):
    """Difficulty of medals obtainable in matchmaking."""

    # Values line up to indices in the medal metadata response content.
    NORMAL = 0
    HEROIC = 1
    LEGENDARY = 2
    MYTHIC = 3


class MedalType(IntEnum):
    """Types of medals obtainable in matchmaking."""

    # Values line up to indices in the medal metadata response content.
    SPREE = 0
    MODE = 1
    MULTIKILL = 2
    PROFICIENCY = 3
    SKILL = 4
    STYLE = 5


class Outcome(IntEnum):
    """Match outcome options."""

    UNKNOWN = -1
    NONE = 0
    TIE = 1
    WIN = 2
    LOSS = 3
    DID_NOT_FINISH = 4
    DID_NOT_START = 5


class PlayerType(IntEnum):
    """Types of players."""

    UNKNOWN = -1
    HUMAN = 1
    BOT = 2


class PlaylistBotDifficulty(IntEnum):
    """Bot difficulty options for matchmaking playlists."""

    AUTOMATIC = 0
    RECRUIT = 1
    MARINE = 2
    ODST = 3
    SPARTAN = 4


class PlaylistDeviceInput(IntEnum):
    """Device input options for matchmaking playlists."""

    UNKNOWN = 0
    CONTROLLER = 1
    MOUSE_KEYBOARD = 2


class PlaylistEntrySelectionStrategy(IntEnum):
    """Selection strategies for playlist entries."""

    WEIGHTED = 0
    NO_REPEAT = 1


class PlaylistExperience(IntEnum):
    """General categories of playlists."""

    UNKNOWN = -1
    NONE = 0
    UNTRACKED = 1
    ARENA = 2
    BIG_TEAM_BATTLE = 3
    PVE = 4
    FEATURED = 5
    FIREFIGHT = 6


class SkillResultCode(IntEnum):
    """Result codes for skill requests."""

    SUCCESS = 0
    NOT_FOUND = 1
    SERVICE_FAILURE = 2
    SERVICE_UNAVAILABLE = 3
    FORBIDDEN = 4


class SubTier(Enum):
    """Sub-tiers of skill rankings.

    The `value` attribute of the sub-tier items is the index of the sub-tier,
    starting at 0 for the 1st sub-tier and incrementing as sub-tier increases.
    The `to_int` method returns the true sub-tier value, e.g., "ONE" returns 1.
    """

    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5

    @classmethod
    def from_int(cls, value: int) -> "SubTier":
        """Return the sub-tier from an integer value."""
        return cls(value - 1)

    def to_int(self) -> int:
        """Return the integer value of the sub-tier. For example, "ONE" => 1."""
        return self.value + 1


class Tier(StrEnum):
    """Tiers of skill rankings."""

    UNRANKED = ""
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    DIAMOND = "Diamond"
    ONYX = "Onyx"
