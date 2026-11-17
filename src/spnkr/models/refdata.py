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
    """Match origin/hosting method enumeration."""

    CUSTOM = 1
    MATCHMADE = 3
    CUSTOM_LAN = 7


class MedalNameId(IntEnum):
    """Medal award enumeration."""

    def __new__(cls, value: int, display_name: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._display_name = display_name  # type: ignore
        return obj

    @property
    def display_name(self) -> str:
        """Get the name of the medal as displayed in-game."""
        return self._display_name  # type: ignore

    THREE_SIXTY = 1427176344, "360"
    ACE = 521420212, "Ace"
    ACHILLES_SPINE = 3217141618, "Achilles Spine"
    ACTION_HERO = 2976102155, "Action Hero"
    ALL_THAT_JUICE = 3528500956, "All That Juice"
    ALWAYS_ROTATING = 1472686630, "Always Rotating"
    APOCALYPSE = 3653884673, "Apocalypse"
    ASSURED_DESTRUCTION = 1585298941, "Assured Destruction"
    AUTOPILOT_ENGAGED = 1623236079, "Autopilot Engaged"
    BACK_SMACK = 548533137, "Back Smack"
    BALLISTA = 4215552487, "Ballista"
    BANK_SHOT = 2414983178, "Bank Shot"
    BIG_DEAL = 2125906504, "Big Deal"
    BLIGHT = 88914608, "Blight"
    BLIND_FIRE = 4007438389, "Blind Fire"
    BODYGUARD = 555849395, "Bodyguard"
    BOMBER = 1146876011, "Bomber"
    BOOGEYMAN = 1720896992, "Boogeyman"
    BOOM_BLOCK = 524758914, "Boom Block"
    BOXER = 269174970, "Boxer"
    BREACHER = 2750622016, "Breacher"
    BULLTRUE = 3114137341, "Bulltrue"
    CALL_BLOCKED = 2964157454, "Call Blocked"
    CHAIN_REACTION = 1969067783, "Chain Reaction"
    CLASH_OF_KINGS = 1053114074, "Clash of Kings"
    CLEANSING = 1765213446, "Cleansing"
    CLEAR_RECEPTION = 394349536, "Clear Reception"
    CLOCK_STOP = 3630529364, "Clock Stop"
    CLUSTER_LUCK = 3905838030, "Cluster Luck"
    COMBAT_EVOLVED = 641726424, "Combat Evolved"
    CONTRACT_KILLER = 590706932, "Contract Killer"
    COUNTER_SNIPE = 1477806194, "Counter-snipe"
    CULLING = 1025827095, "Culling"
    DEADLY_CATCH = 2396845048, "Deadly Catch"
    DEATH_CABBIE = 2848470465, "Death Cabbie"
    DEATH_RACE = 677323068, "Death Race"
    DEEP_BALL = 1254180082, "Deep Ball"
    DEMON = 2875941471, "Demon"
    DISEASE = 1155542859, "Disease"
    DIVINE_INTERVENTION = 2164872967, "Divine Intervention"
    DOGFIGHT = 1229018603, "Dogfight"
    DOUBLE_KILL = 622331684, "Double Kill"
    DRIVEBY = 197913196, "Driveby"
    DRIVER = 3027762381, "Driver"
    DRIVING_SPREE = 3169118333, "Driving Spree"
    DUELIST = 4247875860, "Duelist"
    EXTERMINATION = 4100966367, "Extermination"
    FAST_BREAK = 4014259917, "Fast Break"
    FAST_LANK = 3945864962, "Fast Lane"
    FASTBALL = 1211820913, "Fastball"
    FIRE_AND_FORGET = 988255960, "Fire & Forget"
    FLAG_JOUST = 976049027, "Flag Joust"
    FLAWLESS_VICTORY = 1680000231, "Flawless Victory"
    FLYIN_HIGH = 3739610597, "Flyin' High"
    FROM_THE_GRAVE = 2625820422, "From the Grave"
    FROM_THE_VOID = 3588869844, "From the Void"
    FUMBLE = 3732790338, "Fumble"
    GOAL_LINE_STAND = 3227840152, "Goal Line Stand"
    GRAND_SLAM = 1646928910, "Grand Slam"
    GRAPPLE_JACK = 690125105, "Grapple-jack"
    GREAT_JOURNEY = 1376646881, "Great Journey"
    GRENADIER = 2648272972, "Grenadier"
    GRIM_REAPER = 2567026752, "Grim Reaper"
    GUARDIAN_ANGEL = 3334154676, "Guardian Angel"
    GUNNER = 3783455472, "Gunner"
    GUNSLINGER = 1172766553, "Gunslinger"
    HAIL_MARY = 3934547153, "Hail Mary"
    HANG_UP = 4285712605, "Hang Up"
    HANG_TIME = 1325926691, "Hang Time"
    HARPOON = 2418616582, "Harpoon"
    HEAVY = 4086138034, "Heavy"
    HELLS_JANITOR = 217730222, "Hell's Janitor"
    HIGH_VALUE_TARGET = 3041030832, "High Value Target"
    HILL_GUARDIAN = 580478179, "Hill Guardian"
    HOLD_THIS = 175594566, "Hold This"
    IMMORTAL = 3120600565, "Immortal"
    IMMORTAL_CHAUFFEUR = 1739996188, "Immortal Chauffeur"
    INTERCEPTION = 2362950720, "Interception"
    INTERLINKED = 651256911, "Interlinked"
    KILLAMANJARO = 3835606176, "Killamanjaro"
    KILLING_FRENZY = 4261842076, "Killing Frenzy"
    KILLING_SPREE = 2780740615, "Killing Spree"
    KILLIONAIRE = 3233051772, "Killionaire"
    KILLJOY = 3233952928, "Killjoy"
    KILLPOCALYPSE = 3352648716, "Killpocalypse"
    KILLTACULAR = 2137071619, "Killtacular"
    KILLTASTROPHE = 2242633421, "Killtastrophe"
    KILLTROCITY = 1430343434, "Killtrocity"
    KONG = 3546244406, "Kong"
    LAST_SHOT = 3091261182, "Last Shot"
    LATE_BOOMER = 1334138090, "Late Boomer"
    LAWNMOWER = 3475540930, "Lawnmower"
    LONE_WOLF = 2623698509, "Lone Wolf"
    MARKSMAN = 2758320809, "Marksman"
    MEGANAUT = 2005352812, "Meganaut"
    MIND_THE_GAP = 1880789493, "Mind the Gap"
    MONOPOLY = 1090931685, "Monopoly"
    MOUNT_UP = 1065136443, "Mount Up"
    MOUNTED_AND_LOADED = 1331361851, "Mounted & Loaded"
    NADE_SHOT = 265478668, "Nade Shot"
    NECROMANCER = 3011158621, "Necromancer"
    NIGHTMARE = 710323196, "Nightmare"
    NINJA = 3085856613, "Ninja"
    NO_SCOPE = 2602963073, "No Scope"
    NUCLEAR_FOOTBALL = 2253222811, "Nuclear Football"
    ODINS_RAVEN = 87172902, "Odin's Raven"
    OFF_THE_RACK = 1283796619, "Off the Rack"
    OVERKILL = 835814121, "Overkill"
    PANCAKE = 3876426273, "Pancake"
    PARTYS_OVER = 3583966655, "Party's Over"
    PERFECT = 1512363953, "Perfect"
    PERFECTION = 865763896, "Perfection"
    PESTILENCE = 1719203329, "Pestilence"
    PILOT = 2593226288, "Pilot"
    PINEAPPLE_EXPRESS = 2019283350, "Pineapple Express"
    PLAGUE = 3786134933, "Plague"
    POWER_OUTAGE = 629165579, "Power Outage"
    PULL = 4132863117, "Pull"
    PURGE = 3467301935, "Purge"
    PURIFICATION = 496411737, "Purification"
    QUICK_DRAW = 2861418269, "Quick Draw"
    QUIGLEY = 1312042926, "Quigley"
    RAMMING_SPEED = 1298835518, "Ramming Speed"
    RAMPAGE = 1486797009, "Rampage"
    RECLAIMER = 1445036152, "Reclaimer"
    REMOTE_DETONATION = 3160646854, "Remote Detonation"
    RETURN_TO_SENDER = 3059799290, "Return to Sender"
    REVERSAL = 2123530881, "Reversal"
    RIDESHARE = 656245292, "Rideshare"
    RIFLEMAN = 2852571933, "Rifleman"
    RUNNING_RIOT = 418532952, "Running Riot"
    SABOTEUR = 20397755, "Saboteur"
    SCATTERGUNNER = 3347922939, "Scattergunner"
    SCOURGE = 3520382976, "Scourge"
    SECURE_LINE = 2426456555, "Secure Line"
    SHARPSHOOTER = 4277328263, "Sharpshooter"
    SHOT_CALLER = 1169571763, "Shot Caller"
    SIGNAL_BLOCK = 3931425309, "Signal Block"
    SKYJACK = 731054446, "Skyjack"
    SNEAK_KING = 670606868, "Sneak King"
    SNIPE = 4229934157, "Snipe"
    SOLE_SURVIVOR = 2717755703, "Sole Survivor"
    SPECIAL_DELIVERY = 275666139, "Special Delivery"
    SPLATTER = 221693153, "Splatter"
    SPOTTER = 2477555653, "Spotter"
    STEAKTACULAR = 1169390319, "Steaktacular"
    STICK = 3655682764, "Stick"
    STOPPED_SHORT = 3488248720, "Stopped Short"
    STRAIGHT_BALLING = 781229683, "Straight Balling"
    STREET_SWEEPER = 2967011722, "Street Sweeper"
    TAG_AND_BAG = 1841872491, "Tag & Bag"
    TANKER = 2278023431, "Tanker"
    THE_SICKNESS = 17866865, "The Sickness"
    TREASURE_HUNTER = 1685043466, "Treasure Hunter"
    TRIPLE_KILL = 2063152177, "Triple Kill"
    UNDEAD_HUNTER = 1447057920, "Undead Hunter"
    UNTAINTED = 1064731598, "Untainted"
    WARRIOR = 1210678802, "Warrior"
    WATCH_THE_THRONE = 1210968206, "Watch the Throne"
    WHEELMAN = 2926348688, "Wheelman"
    WHIPLASH = 1734214473, "Whiplash"
    WINDSHIELD_WIPER = 2827657131, "Windshield Wiper"
    WINGMAN = 1284032216, "Wingman"
    YARD_SALE = 1176569867, "Yard Sale"
    ZOMBIE_SLAYER = 557309779, "Zombie Slayer"
    ZONE_GUARDIAN = 420808268, "Zone Guardian"


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


class PersonalScoreNameId(IntEnum):
    """Personal score award enumeration."""

    def __new__(cls, value: int, display_name: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._display_name = display_name  # type: ignore
        return obj

    @property
    def display_name(self) -> str:
        """Get the name of the personal score award as displayed in-game."""
        return self._display_name  # type: ignore

    BALL_CONTROL = 454168309, "Ball Control"  # 50
    BALL_TAKEN = 204144695, "Ball Taken"  # 10
    BETRAYED_PLAYER = 911992497, "Betrayed Player"  # -100
    CARRIER_KILLED = 4128329646, "Carrier Killed"  # 10, Stockpile
    CARRIER_STOPPED = 746397417, "Carrier Stopped"  # 25, Oddball
    COLLECTED_BONUS_XP = 522435689, "Collected Bonus XP"  # 300, Last Spartan Standing
    CONVERSION_DENIED = 4247243561, "Conversion Denied"  # 25
    CUSTOM = 4294967295, "Custom"  # Variable, scripted in a node graph
    DESTROYED_BANSHEE = 597066859, "Destroyed Banshee"  # 50
    DESTROYED_CHOPPER = 3472794399, "Destroyed Chopper"  # 50
    DESTROYED_FALCON = 395875864, "Destroyed Falcon"  # 75
    DESTROYED_GHOST = 4254982885, "Destroyed Ghost"  # 50
    DESTROYED_GUNGOOSE = 2107631925, "Destroyed Gungoose"  # 25
    DESTROYED_MONGOOSE = 1416267372, "Destroyed Mongoose"  # 25
    DESTROYED_PHANTOM = 2742351765, "Destroyed Phantom"  # 100
    DESTROYED_RAZORBACK = 1661163286, "Destroyed Razorback"  # 50
    DESTROYED_ROCKET_WARTHOG = 2008690931, "Destroyed Rocket Warthog"  # 50
    DESTROYED_SCORPION = 3454330054, "Destroyed Scorpion"  # 100
    DESTROYED_WARTHOG = 3107879375, "Destroyed Warthog"  # 50
    DESTROYED_WASP = 2106274556, "Destroyed Wasp"  # 50
    DESTROYED_WRAITH = 3243589708, "Destroyed Wraith"  # 100
    DRIVER_ASSIST = 963594075, "Driver Assist"  # 50
    EMP_ASSIST = 221060588, "EMP Assist"  # 50
    ELIMINATED_PLAYER = 2408971842, "Eliminated Player"  # 200
    EXTRACTION_COMPLETED = 4130011565, "Extraction Completed"  # 200
    EXTRACTION_CONVERTED = 1117301492, "Extraction Converted"  # 50
    EXTRACTION_DENIED = 1552628741, "Extraction Denied"  # 25
    EXTRACTION_INITIATED = 1825517751, "Extraction Initiated"  # 50
    FLAG_CAPTURE_ASSIST = 555570945, "Flag Capture Assist"  # 100
    FLAG_CAPTURED = 601966503, "Flag Captured"  # 300
    FLAG_RETURNED = 22113181, "Flag Returned"  # 25
    FLAG_STOLEN = 3002710045, "Flag Stolen"  # 25
    FLAG_TAKEN = 2387185397, "Flag Taken"  # 10
    HACKED_TERMINAL = 665081740, "Hacked Terminal"  # 100
    HIJACKED_BANSHEE = 3150095814, "Hijacked Banshee"  # 25
    HIJACKED_CHOPPER = 1059880024, "Hijacked Chopper"  # 25
    HIJACKED_FALCON = 586857799, "Hijacked Falcon"  # 25
    HIJACKED_GHOST = 1614285349, "Hijacked Ghost"  # 25
    HIJACKED_GUNGOOSE = 4186766732, "Hijacked Gungoose"  # 25
    HIJACKED_MONGOOSE = 2191528998, "Hijacked Mongoose"  # 25
    HIJACKED_RAZORBACK = 2848565291, "Hijacked Razorback"  # 25
    HIJACKED_ROCKET_WARTHOG = 4294405210, "Hijacked Rocket Warthog"  # 25
    HIJACKED_WARTHOG = 1834653062, "Hijacked Warthog"  # 25
    HIJACKED_WASP = 674964649, "Hijacked Wasp"  # 25
    HILL_CONTROL = 340198991, "Hill Control"  # 25
    HILL_SCORED = 1032565232, "Hill Scored"  # 100
    KILL_ASSIST = 638246808, "Kill Assist"  # 50
    KILLED_PLAYER = 1024030246, "Killed Player"  # 100
    MARK_ASSIST = 152718958, "Mark Assist"  # 10
    POWER_SEED_SECURED = 2188620691, "Power Seed Secured"  # 100
    POWER_SEED_STOLEN = 3996338664, "Power Seed Stolen"  # 50
    REVIVE_DENIED = 2130209372, "Revive Denied"  # 25
    REVIVED_PLAYER = 3428202435, "Revived Player"  # 100
    RUNNER_STOPPED = 316828380, "Runner Stopped"  # 25, CTF
    SELF_DESTRUCTION = 249491819, "Self-destruction"  # -100
    SENSOR_ASSIST = 1267013266, "Sensor Assist"  # 10
    STOCKPILE_SCORED = 2801241965, "Stockpile Scored"  # 150
    ZONE_CAPTURED_50 = 3507884073, "Zone Captured"  # 50
    ZONE_CAPTURED_75 = 4026987576, "Zone Captured"  # 75
    ZONE_CAPTURED_100 = 757037588, "Zone Captured"  # 100
    ZONE_SECURED = 709346128, "Zone Secured"  # 25


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
    """Type of experience provided by a matchmaking playlist."""

    UNKNOWN = -1
    NONE = 0
    UNTRACKED = 1
    ARENA = 2
    BTB = 3
    PVE_BOTS = 4
    FEATURED = 5
    PVE = 6


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

    I = 0  # noqa: E741
    II = 1
    III = 2
    IV = 3
    V = 4
    VI = 5

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
