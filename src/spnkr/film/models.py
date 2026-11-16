from enum import IntEnum, StrEnum
from typing import NamedTuple, Self

from pydantic import BaseModel, computed_field, model_validator


class EventType(StrEnum):
    KILL = "kill"
    DEATH = "death"
    MEDAL = "medal"
    MODE = "mode"


class Medal(IntEnum):
    DOUBLE_KILL = 0
    TRIPLE_KILL = 1
    OVERKILL = 2
    KILLTACULAR = 3
    KILLTROCITY = 4
    KILLAMANJARO = 5
    KILLTASTROPHE = 6
    KILLPOCALYPSE = 7
    KILLIONAIRE = 8
    KILLING_SPREE = 9
    KILLING_FRENZY = 10
    RUNNING_RIOT = 11
    RAMPAGE = 12
    PERFECTION = 13
    KILLJOY = 26
    NIGHTMARE = 27
    BOOGEYMAN = 28
    GRIM_REAPER = 29
    DEMON = 30
    FLAWLESS_VICTORY = 31
    STEAKTACULAR = 32
    STOPPED_SHORT = 36
    FLAG_JOUST = 37
    GOAL_LINE_STAND = 38
    NECROMANCER = 39
    IMMORTAL = 40
    LONE_WOLF = 41
    DUELIST = 42
    ACE = 43
    EXTERMINATION = 44
    SOLE_SURVIVOR = 45
    UNTAINTED = 46
    BLIGHT = 47
    DISEASE = 48
    PLAGUE = 49
    SCOURGE = 50
    PESTILENCE = 51
    APOCALYPSE = 52
    CULLING = 53
    CLEANSING = 54
    PURGE = 55
    PURIFICATION = 56
    DIVINE_INTERVENTION = 57
    ZOMBIE_SLAYER = 58
    UNDEAD_HUNTER = 59
    HELLS_JANITOR = 60
    THE_SICKNESS = 61
    SPOTTER = 62
    TREASURE_HUNTER = 63
    SABOTEUR = 64
    WINGMAN = 65
    WHEELMAN = 66
    GUNNER = 67
    DRIVER = 68
    PILOT = 69
    TANKER = 70
    RIFLEMAN = 71
    BOMBER = 72
    GRENADIER = 73
    BOXER = 74
    WARRIOR = 75
    GUNSLINGER = 76
    SCATTERGUNNER = 77
    SHARPSHOOTER = 78
    MARKSMAN = 79
    HEAVY = 80
    BODYGUARD = 81
    BACK_SMACK = 82
    NUCLEAR_FOOTBALL = 83
    BOOM_BLOCK = 84
    BULLTRUE = 85
    CLUSTER_LUCK = 86
    DOGFIGHT = 87
    HARPOON = 88
    MIND_THE_GAP = 89
    NINJA = 90
    ODINS_RAVEN = 91
    PANCAKE = 92
    QUIGLEY = 93
    REMOTE_DETONATION = 94
    RETURN_TO_SENDER = 95
    RIDESHARE = 96
    SKYJACK = 97
    STICK = 98
    TAG_AND_BAG = 99
    WHIPLASH = 100
    KONG = 101
    AUTOPILOT_ENGAGED = 102
    SNEAK_KING = 103
    WINDSHIELD_WIPER = 104
    REVERSAL = 105
    HAIL_MARY = 106
    NADE_SHOT = 107
    SNIPE = 108
    PERFECT = 109
    BANK_SHOT = 110
    FIRE_AND_FORGET = 111
    BALLISTA = 112
    PULL = 113
    NO_SCOPE = 114
    ACHILLES_SPINE = 115
    GRAND_SLAM = 116
    GUARDIAN_ANGEL = 117
    INTERLINKED = 118
    DEATH_RACE = 119
    CHAIN_REACTION = 120
    THREE_SIXTY = 121
    COMBAT_EVOLVED = 122
    DEADLY_CATCH = 123
    DRIVEBY = 124
    FASTBALL = 125
    FLYIN_HIGH = 126
    FROM_THE_GRAVE = 127
    FROM_THE_VOID = 128
    GRAPPLE_JACK = 129
    HOLD_THIS = 130
    LAST_SHOT = 131
    LAWNMOWER = 132
    MOUNT_UP = 133
    OFF_THE_RACK = 134
    QUICK_DRAW = 135
    PARTYS_OVER = 136
    PINEAPPLE_EXPRESS = 137
    RAMMING_SPEED = 138
    RECLAIMER = 139
    SHOT_CALLER = 140
    YARD_SALE = 141
    SPECIAL_DELIVERY = 142
    STREET_SWEEPER = 143
    FUMBLE = 146
    STRAIGHT_BALLING = 148
    BIG_DEAL = 150
    ALWAYS_ROTATING = 151
    HILL_GUARDIAN = 152
    CLOCK_STOP = 153
    SECURE_LINE = 154
    SIGNAL_BLOCK = 155
    SPLATTER = 156
    CLASH_OF_KINGS = 157
    CONTRACT_KILLER = 158
    WATCH_THE_THRONE = 160
    ALL_THAT_JUICE = 162
    GREAT_JOURNEY = 163
    POWER_OUTAGE = 164
    BREACHER = 165
    MOUNTED_AND_LOADED = 166
    MONOPOLY = 167
    COUNTER_SNIPE = 168
    DRIVING_SPREE = 174
    DEATH_CABBIE = 175
    IMMORTAL_CHAUFFEUR = 176
    BLIND_FIRE = 177
    HANG_UP = 178
    CALL_BLOCKED = 179
    CLEAR_RECEPTION = 180

    @property
    def display_name(self) -> str:
        """Return the display name of the medal."""
        return _MEDAL_NAMES[self]


class HighlightEvent(BaseModel, frozen=True):
    """A kill, death, mode-related, or medal game event in a Halo Infinite match."""

    xuid: int
    """Xbox user ID of the player the event is tied to."""
    gamertag: str
    """Gamertag of the player the event is tied to."""
    event_type: EventType
    """Inferred event type. One of 'kill', 'death', 'mode', or 'medal'."""
    time_ms: int
    """Timestamp of the event in milliseconds following the start of the match."""
    medal: Medal | None
    """Medal awarded for 'medal' event types. Otherwise `None`."""

    @model_validator(mode="after")
    def validate_medal(self) -> Self:
        if self.event_type is EventType.MEDAL and self.medal is None:
            raise ValueError("medal is required for medal events")
        if self.event_type is not EventType.MEDAL and self.medal is not None:
            raise ValueError("medal must be None for non-medal events")
        return self

    @computed_field
    @property
    def medal_name(self) -> str | None:
        return self.medal.display_name if self.medal is not None else None


class EventCounts(NamedTuple):
    """Container for storing expected or resulting event counts."""

    kills: int
    deaths: int
    medals: int


_MEDAL_NAMES = {
    Medal.DOUBLE_KILL: "Double Kill",
    Medal.TRIPLE_KILL: "Triple Kill",
    Medal.OVERKILL: "Overkill",
    Medal.KILLTACULAR: "Killtacular",
    Medal.KILLTROCITY: "Killtrocity",
    Medal.KILLAMANJARO: "Killamanjaro",
    Medal.KILLTASTROPHE: "Killtastrophe",
    Medal.KILLPOCALYPSE: "Killpocalypse",
    Medal.KILLIONAIRE: "Killionaire",
    Medal.KILLING_SPREE: "Killing Spree",
    Medal.KILLING_FRENZY: "Killing Frenzy",
    Medal.RUNNING_RIOT: "Running Riot",
    Medal.RAMPAGE: "Rampage",
    Medal.PERFECTION: "Perfection",
    Medal.KILLJOY: "Killjoy",
    Medal.NIGHTMARE: "Nightmare",
    Medal.BOOGEYMAN: "Boogeyman",
    Medal.GRIM_REAPER: "Grim Reaper",
    Medal.DEMON: "Demon",
    Medal.FLAWLESS_VICTORY: "Flawless Victory",
    Medal.STEAKTACULAR: "Steaktacular",
    Medal.STOPPED_SHORT: "Stopped Short",
    Medal.FLAG_JOUST: "Flag Joust",
    Medal.GOAL_LINE_STAND: "Goal Line Stand",
    Medal.NECROMANCER: "Necromancer",
    Medal.IMMORTAL: "Immortal",
    Medal.LONE_WOLF: "Lone Wolf",
    Medal.DUELIST: "Duelist",
    Medal.ACE: "Ace",
    Medal.EXTERMINATION: "Extermination",
    Medal.SOLE_SURVIVOR: "Sole Survivor",
    Medal.UNTAINTED: "Untainted",
    Medal.BLIGHT: "Blight",
    Medal.DISEASE: "Disease",
    Medal.PLAGUE: "Plague",
    Medal.SCOURGE: "Scourge",
    Medal.PESTILENCE: "Pestilence",
    Medal.APOCALYPSE: "Apocalypse",
    Medal.CULLING: "Culling",
    Medal.CLEANSING: "Cleansing",
    Medal.PURGE: "Purge",
    Medal.PURIFICATION: "Purification",
    Medal.DIVINE_INTERVENTION: "Divine Intervention",
    Medal.ZOMBIE_SLAYER: "Zombie Slayer",
    Medal.UNDEAD_HUNTER: "Undead Hunter",
    Medal.HELLS_JANITOR: "Hell's Janitor",
    Medal.THE_SICKNESS: "The Sickness",
    Medal.SPOTTER: "Spotter",
    Medal.TREASURE_HUNTER: "Treasure Hunter",
    Medal.SABOTEUR: "Saboteur",
    Medal.WINGMAN: "Wingman",
    Medal.WHEELMAN: "Wheelman",
    Medal.GUNNER: "Gunner",
    Medal.DRIVER: "Driver",
    Medal.PILOT: "Pilot",
    Medal.TANKER: "Tanker",
    Medal.RIFLEMAN: "Rifleman",
    Medal.BOMBER: "Bomber",
    Medal.GRENADIER: "Grenadier",
    Medal.BOXER: "Boxer",
    Medal.WARRIOR: "Warrior",
    Medal.GUNSLINGER: "Gunslinger",
    Medal.SCATTERGUNNER: "Scattergunner",
    Medal.SHARPSHOOTER: "Sharpshooter",
    Medal.MARKSMAN: "Marksman",
    Medal.HEAVY: "Heavy",
    Medal.BODYGUARD: "Bodyguard",
    Medal.BACK_SMACK: "Back Smack",
    Medal.NUCLEAR_FOOTBALL: "Nuclear Football",
    Medal.BOOM_BLOCK: "Boom Block",
    Medal.BULLTRUE: "Bulltrue",
    Medal.CLUSTER_LUCK: "Cluster Luck",
    Medal.DOGFIGHT: "Dogfight",
    Medal.HARPOON: "Harpoon",
    Medal.MIND_THE_GAP: "Mind the Gap",
    Medal.NINJA: "Ninja",
    Medal.ODINS_RAVEN: "Odin's Raven",
    Medal.PANCAKE: "Pancake",
    Medal.QUIGLEY: "Quigley",
    Medal.REMOTE_DETONATION: "Remote Detonation",
    Medal.RETURN_TO_SENDER: "Return to Sender",
    Medal.RIDESHARE: "Rideshare",
    Medal.SKYJACK: "Skyjack",
    Medal.STICK: "Stick",
    Medal.TAG_AND_BAG: "Tag & Bag",
    Medal.WHIPLASH: "Whiplash",
    Medal.KONG: "Kong",
    Medal.AUTOPILOT_ENGAGED: "Autopilot Engaged",
    Medal.SNEAK_KING: "Sneak King",
    Medal.WINDSHIELD_WIPER: "Windshield Wiper",
    Medal.REVERSAL: "Reversal",
    Medal.HAIL_MARY: "Hail Mary",
    Medal.NADE_SHOT: "Nade Shot",
    Medal.SNIPE: "Snipe",
    Medal.PERFECT: "Perfect",
    Medal.BANK_SHOT: "Bank Shot",
    Medal.FIRE_AND_FORGET: "Fire & Forget",
    Medal.BALLISTA: "Ballista",
    Medal.PULL: "Pull",
    Medal.NO_SCOPE: "No Scope",
    Medal.ACHILLES_SPINE: "Achilles Spine",
    Medal.GRAND_SLAM: "Grand Slam",
    Medal.GUARDIAN_ANGEL: "Guardian Angel",
    Medal.INTERLINKED: "Interlinked",
    Medal.DEATH_RACE: "Death Race",
    Medal.CHAIN_REACTION: "Chain Reaction",
    Medal.THREE_SIXTY: "360",
    Medal.COMBAT_EVOLVED: "Combat Evolved",
    Medal.DEADLY_CATCH: "Deadly Catch",
    Medal.DRIVEBY: "Driveby",
    Medal.FASTBALL: "Fastball",
    Medal.FLYIN_HIGH: "Flyin' High",
    Medal.FROM_THE_GRAVE: "From the Grave",
    Medal.FROM_THE_VOID: "From the Void",
    Medal.GRAPPLE_JACK: "Grapple-jack",
    Medal.HOLD_THIS: "Hold This",
    Medal.LAST_SHOT: "Last Shot",
    Medal.LAWNMOWER: "Lawnmower",
    Medal.MOUNT_UP: "Mount Up",
    Medal.OFF_THE_RACK: "Off the Rack",
    Medal.QUICK_DRAW: "Quick Draw",
    Medal.PARTYS_OVER: "Party's Over",
    Medal.PINEAPPLE_EXPRESS: "Pineapple Express",
    Medal.RAMMING_SPEED: "Ramming Speed",
    Medal.RECLAIMER: "Reclaimer",
    Medal.SHOT_CALLER: "Shot Caller",
    Medal.YARD_SALE: "Yard Sale",
    Medal.SPECIAL_DELIVERY: "Special Delivery",
    Medal.STREET_SWEEPER: "Street Sweeper",
    Medal.FUMBLE: "Fumble",
    Medal.STRAIGHT_BALLING: "Straight Balling",
    Medal.BIG_DEAL: "Big Deal",
    Medal.ALWAYS_ROTATING: "Always Rotating",
    Medal.HILL_GUARDIAN: "Hill Guardian",
    Medal.CLOCK_STOP: "Clock Stop",
    Medal.SECURE_LINE: "Secure Line",
    Medal.SIGNAL_BLOCK: "Signal Block",
    Medal.SPLATTER: "Splatter",
    Medal.CLASH_OF_KINGS: "Clash of Kings",
    Medal.CONTRACT_KILLER: "Contract Killer",
    Medal.WATCH_THE_THRONE: "Watch the Throne",
    Medal.ALL_THAT_JUICE: "All That Juice",
    Medal.GREAT_JOURNEY: "Great Journey",
    Medal.POWER_OUTAGE: "Power Outage",
    Medal.BREACHER: "Breacher",
    Medal.MOUNTED_AND_LOADED: "Mounted & Loaded",
    Medal.MONOPOLY: "Monopoly",
    Medal.COUNTER_SNIPE: "Counter-snipe",
    Medal.DRIVING_SPREE: "Driving Spree",
    Medal.DEATH_CABBIE: "Death Cabbie",
    Medal.IMMORTAL_CHAUFFEUR: "Immortal Chauffeur",
    Medal.BLIND_FIRE: "Blind Fire",
    Medal.HANG_UP: "Hang Up",
    Medal.CALL_BLOCKED: "Call Blocked",
    Medal.CLEAR_RECEPTION: "Clear Reception",
}
