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
    "MEDAL_NAME_MAP",
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
    "bid(0.0)": "343 Ritzy",
    "bid(1.0)": "343 Meowlnir",
    "bid(2.0)": "343 Wiggle Cat",
    "bid(3.0)": "343 Ellis",
    "bid(4.0)": "343 Godfather",
    "bid(5.0)": "343 Colson",
    "bid(6.0)": "343 Donos",
    "bid(7.0)": "343 PardonMy",
    "bid(8.0)": "343 Ensrude",
    "bid(9.0)": "343 TooMilks",
    "bid(10.0)": "343 Beard",
    "bid(11.0)": "343 Razzle",
    "bid(12.0)": "343 Nando",
    "bid(13.0)": "343 GrappleMans",
    "bid(14.0)": "343 Zero",
    "bid(15.0)": "343 Mak",
    "bid(16.0)": "343 Hundy",
    "bid(17.0)": "343 Lacuna",
    "bid(18.0)": "343 Cream Corn",
    "bid(19.0)": "343 Brew Dog",
    "bid(20.0)": "343 Lemondade",
    "bid(21.0)": "343 Flippant",
    "bid(22.0)": "343 Connmando",
    "bid(23.0)": "343 Byrontron",
    "bid(24.0)": "343 Ham Sammich",
    "bid(25.0)": "343 BoboGan",
    "bid(26.0)": "343 Robot Hoida",
    "bid(27.0)": "343 Mumblebee",
    "bid(28.0)": "343 Tedosaur",
    "bid(29.0)": "343 Cliffton",
    "bid(30.0)": "343 Stone",
    "bid(31.0)": "343 Marmot",
    "bid(32.0)": "343 Mickey",
    "bid(33.0)": "343 Bachici",
    "bid(34.0)": "343 Ben Desk",
    "bid(35.0)": "343 BF Scrub",
    "bid(36.0)": "343 Chaco",
    "bid(37.0)": "343 Total Ten",
    "bid(38.0)": "343 Darkstar",
    "bid(39.0)": "343 Aloysius",
    "bid(40.0)": "343 Dazzle",
    "bid(41.0)": "343 Rhinosaurus",
    "bid(42.0)": "343 Doomfruit",
    "bid(43.0)": "343 Cosmo",
    "bid(44.0)": "343 Sandwolf",
    "bid(45.0)": "343 O Freruner",
    "bid(46.0)": "343 Bergerton",
    "bid(47.0)": "343 SpaceCase",
    "bid(48.0)": "343 KaleDucky",
    "bid(49.0)": "343 BERRYHILL",
    "bid(50.0)": "343 Oscar",
    "bid(51.0)": "343 The Referee",
    "bid(52.0)": "343 Free Money",
    "bid(53.0)": "343 Kubly",
    "bid(54.0)": "343 Tanuki",
    "bid(55.0)": "343 Shady Seal",
    "bid(56.0)": "343 Chilies",
    "bid(57.0)": "343 The Thumb",
    "bid(58.0)": "343 Forge Lord",
    "bid(59.0)": "343 Hollis",
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
MEDAL_NAME_MAP: dict[int, str] = {
    1427176344: "360",
    521420212: "Ace",
    3217141618: "Achilles Spine",
    2976102155: "Action Hero",
    3528500956: "All That Juice",
    1472686630: "Always Rotating",
    3653884673: "Apocalypse",
    1585298941: "Assured Destruction",
    1623236079: "Autopilot Engaged",
    548533137: "Back Smack",
    4215552487: "Ballista",
    2414983178: "Bank Shot",
    2125906504: "Big Deal",
    88914608: "Blight",
    4007438389: "Blind Fire",
    555849395: "Bodyguard",
    1146876011: "Bomber",
    1720896992: "Boogeyman",
    524758914: "Boom Block",
    269174970: "Boxer",
    2750622016: "Breacher",
    3114137341: "Bulltrue",
    2964157454: "Call Blocked",
    1969067783: "Chain Reaction",
    1053114074: "Clash of Kings",
    1765213446: "Cleansing",
    394349536: "Clear Reception",
    3630529364: "Clock Stop",
    3905838030: "Cluster Luck",
    641726424: "Combat Evolved",
    590706932: "Contract Killer",
    1477806194: "Counter-snipe",
    1025827095: "Culling",
    2396845048: "Deadly Catch",
    2848470465: "Death Cabbie",
    677323068: "Death Race",
    1254180082: "Deep Ball",
    2875941471: "Demon",
    1155542859: "Disease",
    2164872967: "Divine Intervention",
    1229018603: "Dogfight",
    622331684: "Double Kill",
    197913196: "Driveby",
    3027762381: "Driver",
    3169118333: "Driving Spree",
    4247875860: "Duelist",
    4100966367: "Extermination",
    4014259917: "Fast Break",
    3945864962: "Fast Lane",
    1211820913: "Fastball",
    988255960: "Fire & Forget",
    976049027: "Flag Joust",
    1680000231: "Flawless Victory",
    3739610597: "Flyin' High",
    2625820422: "From the Grave",
    3588869844: "From the Void",
    3732790338: "Fumble",
    3227840152: "Goal Line Stand",
    1646928910: "Grand Slam",
    690125105: "Grapple-jack",
    1376646881: "Great Journey",
    2648272972: "Grenadier",
    2567026752: "Grim Reaper",
    3334154676: "Guardian Angel",
    3783455472: "Gunner",
    1172766553: "Gunslinger",
    3934547153: "Hail Mary",
    4285712605: "Hang Up",
    1325926691: "Hang Time",
    2418616582: "Harpoon",
    4086138034: "Heavy",
    217730222: "Hell's Janitor",
    3041030832: "High Value Target",
    580478179: "Hill Guardian",
    175594566: "Hold This",
    3120600565: "Immortal",
    1739996188: "Immortal Chauffeur",
    2362950720: "Interception",
    651256911: "Interlinked",
    3835606176: "Killamanjaro",
    4261842076: "Killing Frenzy",
    2780740615: "Killing Spree",
    3233051772: "Killionaire",
    3233952928: "Killjoy",
    3352648716: "Killpocalypse",
    2137071619: "Killtacular",
    2242633421: "Killtastrophe",
    1430343434: "Killtrocity",
    3546244406: "Kong",
    3091261182: "Last Shot",
    1334138090: "Late Boomer",
    3475540930: "Lawnmower",
    2623698509: "Lone Wolf",
    2758320809: "Marksman",
    2005352812: "Meganaut",
    1880789493: "Mind the Gap",
    1090931685: "Monopoly",
    1065136443: "Mount Up",
    1331361851: "Mounted & Loaded",
    265478668: "Nade Shot",
    3011158621: "Necromancer",
    710323196: "Nightmare",
    3085856613: "Ninja",
    2602963073: "No Scope",
    2253222811: "Nuclear Football",
    87172902: "Odin's Raven",
    1283796619: "Off the Rack",
    835814121: "Overkill",
    3876426273: "Pancake",
    3583966655: "Party's Over",
    1512363953: "Perfect",
    865763896: "Perfection",
    1719203329: "Pestilence",
    2593226288: "Pilot",
    2019283350: "Pineapple Express",
    3786134933: "Plague",
    629165579: "Power Outage",
    4132863117: "Pull",
    3467301935: "Purge",
    496411737: "Purification",
    2861418269: "Quick Draw",
    1312042926: "Quigley",
    1298835518: "Ramming Speed",
    1486797009: "Rampage",
    1445036152: "Reclaimer",
    3160646854: "Remote Detonation",
    3059799290: "Return to Sender",
    2123530881: "Reversal",
    656245292: "Rideshare",
    2852571933: "Rifleman",
    418532952: "Running Riot",
    20397755: "Saboteur",
    3347922939: "Scattergunner",
    3520382976: "Scourge",
    2426456555: "Secure Line",
    4277328263: "Sharpshooter",
    1169571763: "Shot Caller",
    3931425309: "Signal Block",
    731054446: "Skyjack",
    670606868: "Sneak King",
    4229934157: "Snipe",
    2717755703: "Sole Survivor",
    275666139: "Special Delivery",
    221693153: "Splatter",
    2477555653: "Spotter",
    1169390319: "Steaktacular",
    3655682764: "Stick",
    3488248720: "Stopped Short",
    781229683: "Straight Balling",
    2967011722: "Street Sweeper",
    1841872491: "Tag & Bag",
    2278023431: "Tanker",
    17866865: "The Sickness",
    1685043466: "Treasure Hunter",
    2063152177: "Triple Kill",
    1447057920: "Undead Hunter",
    1064731598: "Untainted",
    1210678802: "Warrior",
    1210968206: "Watch the Throne",
    2926348688: "Wheelman",
    1734214473: "Whiplash",
    2827657131: "Windshield Wiper",
    1284032216: "Wingman",
    1176569867: "Yard Sale",
    557309779: "Zombie Slayer",
    420808268: "Zone Guardian",
}
"""Mapping of medal name IDs to medal names. For example, 622331684 -> 'Double Kill'."""


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
