"""Enumerated data types used by the Halo Infinite API."""

import logging
from enum import Enum, IntEnum, StrEnum

logger = logging.getLogger(__name__)


class AssetHome(IntEnum):
    """Source of an asset."""

    UNKNOWN = 0
    """Unknown asset source."""
    STUDIO = 1
    """Developer-sourced asset."""
    PLAYER = 2
    """Player-sourced asset."""


class AssetKind(IntEnum):
    """Types of assets used by Halo Infinite."""

    UNKNOWN = 0
    """Unknown asset type."""
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
    """Bot difficulty levels as encoded in stats responses."""

    UNKNOWN = -1
    """Unknown bot difficulty."""
    MARINE = 1
    """Marine bots. 2nd lowest difficulty."""
    ODST = 2
    """ODST bots. 2nd highest difficulty."""
    SPARTAN = 3
    """Spartan bots. Highest difficulty."""
    RECRUIT = 4
    """Recruit bots. Lowest difficulty."""
    ADAPTIVE = 5
    """Adaptive bots. Difficulty changes based on player performance."""


class CloneBehavior(IntEnum):
    """Permission levels for cloning assets."""

    DEFAULT = 0
    """Default clone behavior."""
    TEMPLATE = 1
    """Clone as a template."""
    PROHIBITED = 2
    """Cloning is prohibited."""


class FilmChunkType(IntEnum):
    """Types of saved film chunks."""

    NONE = 0
    """No film chunk type."""
    FILM_HEADER = 1
    """Film header chunk."""
    REPLICATION_DATA = 2
    """Replication data chunk."""
    HIGHLIGHT_EVENTS = 3
    """Highlight events chunk."""


class FilmStatus(IntEnum):
    """Status of a saved film."""

    UNKNOWN = 0
    """Unknown film status."""
    COMPLETE = 1
    """Film is complete."""
    ONGOING = 2
    """Film is ongoing."""
    RECOVERED = 3
    """Film was recovered."""


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
    """Unknown inspection result."""
    TOLERABLE = 5
    """Tolerable inspection result."""
    STUDIO_CONTENT = 50
    """Studio content inspection result."""


class LifecycleMode(IntEnum):
    """General categories of game modes."""

    CUSTOM = 1
    """Custom games."""
    MATCHMADE = 3
    """Matchmade games."""
    LOCAL_AREA_NETWORK = 7
    """Games played on LAN."""


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

    UNKNOWN = -1
    """Unknown match outcome."""
    NONE = 0
    """No match outcome."""
    TIE = 1
    """Match ended in a tie."""
    WIN = 2
    """Match was won."""
    LOSS = 3
    """Match was lost."""
    DID_NOT_FINISH = 4
    """Match was not finished."""
    DID_NOT_START = 5
    """Match was not started."""


class PlayerType(IntEnum):
    """Types of players."""

    UNKNOWN = -1
    """Unknown player type."""
    HUMAN = 1
    """Human players."""
    BOT = 2
    """AI players."""


class PlaylistBotDifficulty(IntEnum):
    """Bot difficulty options for matchmaking playlists."""

    AUTOMATIC = 0
    """Bot difficulty is automatically determined."""
    RECRUIT = 1
    """Recruit bot difficulty."""
    MARINE = 2
    """Marine bot difficulty."""
    ODST = 3
    """ODST bot difficulty."""
    SPARTAN = 4
    """Spartan bot difficulty."""


class PlaylistDeviceInput(IntEnum):
    """Device input options for matchmaking playlists."""

    UNKNOWN = 0
    """Unknown device input."""
    CONTROLLER = 1
    """Controller."""
    MOUSE_KEYBOARD = 2
    """Keyboard and mouse."""


class PlaylistEntrySelectionStrategy(IntEnum):
    """Selection strategies for playlist entries."""

    WEIGHTED = 0
    """Selection strategy that uses weighted probabilities."""
    NO_REPEAT = 1
    """Selection strategy that avoids repeating map mode pairs."""


class PlaylistExperience(IntEnum):
    """General categories of playlists."""

    UNKNOWN = -1
    """Unknown playlist experience."""
    NONE = 0
    """No playlist experience."""
    UNTRACKED = 1
    """Untracked playlist experience."""
    ARENA = 2
    """Arena playlists. Typically 4v4."""
    BIG_TEAM_BATTLE = 3
    """Big team battle playlists. Typically 12v12."""
    PVE = 4
    """Player vs. bots playlists."""
    FEATURED = 5
    """Featured playlists. Rotates frequently."""
    FIREFIGHT = 6
    """Firefight PvE playlist"""


class SkillResultCode(IntEnum):
    """Result codes for skill requests."""

    SUCCESS = 0
    """Skill request was successful."""
    NOT_FOUND = 1
    """Skill request failed as a requested resource was not found."""
    SERVICE_FAILURE = 2
    """Skill request failed due to a service failure."""
    SERVICE_UNAVAILABLE = 3
    """Skill request failed as the service is unavailable."""
    FORBIDDEN = 4
    """Skill request failed as the request was forbidden."""


class SubTier(Enum):
    """Sub-tiers of skill rankings.

    The `value` attribute of the sub-tier items is the index of the sub-tier,
    starting at 0 for the 1st sub-tier and incrementing as sub-tier increases.
    The `to_int` method returns the true sub-tier value, e.g., "ONE" returns 1.
    """

    ONE = 0
    """1st sub-tier."""
    TWO = 1
    """2nd sub-tier."""
    THREE = 2
    """3rd sub-tier."""
    FOUR = 3
    """4th sub-tier."""
    FIVE = 4
    """5th sub-tier."""
    SIX = 5
    """6th sub-tier. Highest sub-tier before advancing to the next tier."""

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
    """Not yet ranked or not applicable."""
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
