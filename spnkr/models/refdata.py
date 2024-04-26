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


class GameVariantCategory(IntEnum):
    """Categories of multiplayer game modes."""

    UNKNOWN = -1
    """Unknown game mode category."""
    NONE = 0
    """No game mode category."""
    CAMPAIGN = 1
    """Campaign game modes."""
    FORGE = 2
    """Forge game modes."""
    ACADEMY = 3
    """Academy game modes."""
    ACADEMY_TUTORIAL = 4
    """Academy tutorial game modes."""
    ACADEMY_PRACTICE = 5
    """Academy practice game modes."""
    SLAYER = 6
    """Multiplayer slayer game modes."""
    ATTRITION = 7
    """Multiplayer attrition game modes."""
    ELIMINATION = 8
    """Multiplayer elimination game modes."""
    FIESTA = 9
    """Multiplayer fiesta game modes."""
    SWAT = 10
    """Multiplayer SWAT game modes."""
    STRONGHOLDS = 11
    """Multiplayer strongholds game modes."""
    BASTION = 12
    """Multiplayer bastion game modes."""
    KING_OF_THE_HILL = 13
    """Multiplayer king of the hill game modes."""
    TOTAL_CONTROL = 14
    """Multiplayer total control game modes."""
    CTF = 15
    """Multiplayer capture the flag game modes."""
    ASSAULT = 16
    """Multiplayer assault game modes."""
    EXTRACTION = 17
    """Multiplayer extraction game modes."""
    ODDBALL = 18
    """Multiplayer oddball game modes."""
    STOCKPILE = 19
    """Multiplayer stockpile game modes."""
    JUGGERNAUT = 20
    """Multiplayer juggernaut game modes."""
    REGICIDE = 21
    """Multiplayer regicide game modes."""
    INFECTION = 22
    """Multiplayer infection game modes."""
    ESCORT = 23
    """Multiplayer escort game modes."""
    GUN_GAME = 24
    """Multiplayer gun game game modes."""
    GRIFBALL = 25
    """Multiplayer grifball game modes."""
    RACE = 26
    """Multiplayer racing game modes."""
    PROTOTYPE = 27
    """Multiplayer prototype game modes."""
    TEST = 28
    """Test game modes."""
    TEST_ACADEMY = 29
    """Test academy game modes."""
    TEST_AUDIO = 30
    """Test audio game modes."""
    TEST_CAMPAIGN = 31
    """Test campaign game modes."""
    TEST_ENGINE = 32
    """Test engine game modes."""
    TEST_FORGE = 33
    """Test forge game modes."""
    TEST_GRAPHICS = 34
    """Test graphics game modes."""
    TEST_MULTIPLAYER = 35
    """Test multiplayer game modes."""
    TEST_SANDBOX = 36
    """Test sandbox game modes."""
    ACADEMY_TRAINING = 37
    """Academy training game modes."""
    ACADEMY_WEAPON_DRILL = 38
    """Academy weapon drill game modes."""
    LAND_GRAB = 39
    """Multiplayer land grab game modes."""
    MINIGAME = 41
    """Minigame game modes."""
    FIREFIGHT_BASTION = 42
    """Firefight king of the hill game modes."""

    @classmethod
    def _missing_(cls, value: int) -> "GameVariantCategory":
        """Return the default game mode category for an unknown value."""
        logger.error(f"Unknown game mode category: {value}")
        return cls.UNKNOWN


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
