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
    "bid(1.0)": "343 Connmando",
    "bid(2.0)": "343 Beard",
    "bid(3.0)": "343 Aloysius",
    "bid(4.0)": "343 Lemondade",
    "bid(5.0)": "343 Cream Corn",
    "bid(6.0)": "343 Rhinosaurus",
    "bid(7.0)": "343 Oscar",
    "bid(8.0)": "343 Marmot",
    "bid(9.0)": "343 Chilies",
    "bid(10.0)": "343 Cliffton",
    "bid(11.0)": "343 Ensrude",
    "bid(12.0)": "343 Godfather",
    "bid(13.0)": "343 Ritzy",
    "bid(14.0)": "343 Darkstar",
    "bid(15.0)": "343 Ham Sammich",
    "bid(16.0)": "343 Meowlnir",
    "bid(17.0)": "343 PardonMy",
    "bid(18.0)": "343 Mak",
    "bid(19.0)": "343 Ellis",
    "bid(20.0)": "343 Robot Hoida",
    "bid(21.0)": "343 Bergerton",
    "bid(22.0)": "343 Tedosaur",
    "bid(23.0)": "343 Cosmo",
    "bid(24.0)": "343 Shady Seal",
    "bid(25.0)": "343 Mumblebee",
    "bid(26.0)": "343 Total Ten",
    "bid(27.0)": "343 Byrontron",
    "bid(28.0)": "343 Forge Lord",
    "bid(29.0)": "343 Mickey",
    "bid(30.0)": "343 Lacuna",
    "bid(31.0)": "343 Hundy",
    "bid(32.0)": "343 Nando",
    "bid(33.0)": "343 Free Money",
    "bid(34.0)": "343 BF Scrub",
    "bid(35.0)": "343 Zero",
    "bid(36.0)": "343 Wiggle Cat",
    "bid(37.0)": "343 Brew Dog",
    "bid(38.0)": "343 The Thumb",
    "bid(39.0)": "343 Flippant",
    "bid(40.0)": "343 Donos",
    "bid(41.0)": "343 O Freruner",
    "bid(42.0)": "343 Tanuki",
    "bid(43.0)": "343 SpaceCase",
    "bid(44.0)": "343 GrappleMans",
    "bid(45.0)": "343 BERRYHILL",
    "bid(46.0)": "343 TooMilks",
    "bid(47.0)": "343 KaleDucky",
    "bid(48.0)": "343 BoboGan",
    "bid(49.0)": "343 Chaco",
    "bid(50.0)": "343 Colson",
    "bid(51.0)": "343 Ben Desk",
    "bid(52.0)": "343 The Referee",
    "bid(53.0)": "343 Doomfruit",
    "bid(54.0)": "343 Stone",
    "bid(55.0)": "343 Hollis",
    "bid(56.0)": "343 Razzle",
    "bid(57.0)": "343 Dazzle",
    "bid(58.0)": "343 Bachici",
    "bid(59.0)": "343 Sandwolf",
    "bid(60.0)": "343 Kubly",
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
    622331684: "Double Kill",
    2063152177: "Triple Kill",
    835814121: "Overkill",
    2137071619: "Killtacular",
    1430343434: "Killtrocity",
    3835606176: "Killamanjaro",
    2242633421: "Killtastrophe",
    3352648716: "Killpocalypse",
    3233051772: "Killionaire",
    2780740615: "Killing Spree",
    4261842076: "Killing Frenzy",
    418532952: "Running Riot",
    1486797009: "Rampage",
    865763896: "Perfection",
    3233952928: "Killjoy",
    710323196: "Nightmare",
    1720896992: "Boogeyman",
    2567026752: "Grim Reaper",
    2875941471: "Demon",
    1680000231: "Flawless Victory",
    1169390319: "Steaktacular",
    3488248720: "Stopped Short",
    976049027: "Flag Joust",
    3227840152: "Goal Line Stand",
    3011158621: "Necromancer",
    3120600565: "Immortal",
    2623698509: "Lone Wolf",
    4247875860: "Duelist",
    521420212: "Ace",
    4100966367: "Extermination",
    2477555653: "Spotter",
    1685043466: "Treasure Hunter",
    20397755: "Saboteur",
    1284032216: "Wingman",
    2926348688: "Wheelman",
    3783455472: "Gunner",
    3027762381: "Driver",
    2593226288: "Pilot",
    2278023431: "Tanker",
    2852571933: "Rifleman",
    1146876011: "Bomber",
    2648272972: "Grenadier",
    269174970: "Boxer",
    1210678802: "Warrior",
    1172766553: "Gunslinger",
    3347922939: "Scattergunner",
    4277328263: "Sharpshooter",
    2758320809: "Marksman",
    4086138034: "Heavy",
    555849395: "Bodyguard",
    548533137: "Back Smack",
    2253222811: "Nuclear Football",
    524758914: "Boom Block",
    3114137341: "Bulltrue",
    3905838030: "Cluster Luck",
    1229018603: "Dogfight",
    2418616582: "Harpoon",
    1880789493: "Mind the Gap",
    3085856613: "Ninja",
    87172902: "Odin's Raven",
    3876426273: "Pancake",
    1312042926: "Quigley",
    3160646854: "Remote Detonation",
    3059799290: "Return to Sender",
    656245292: "Rideshare",
    731054446: "Skyjack",
    3655682764: "Stick",
    1841872491: "Tag & Bag",
    1734214473: "Whiplash",
    3546244406: "Kong",
    1623236079: "Autopilot Engaged",
    670606868: "Sneak King",
    2827657131: "Windshield Wiper",
    2123530881: "Reversal",
    3934547153: "Hail Mary",
    265478668: "Nade Shot",
    4229934157: "Snipe",
    1512363953: "Perfect",
    2414983178: "Bank Shot",
    988255960: "Fire & Forget",
    4215552487: "Ballista",
    4132863117: "Pull",
    2602963073: "No Scope",
    3217141618: "Achilles Spine",
    1646928910: "Grand Slam",
    3334154676: "Guardian Angel",
    651256911: "Interlinked",
    677323068: "Death Race",
    1969067783: "Chain Reaction",
    1427176344: "360",
    641726424: "Combat Evolved",
    2396845048: "Deadly Catch",
    197913196: "Driveby",
    1211820913: "Fastball",
    3739610597: "Flyin' High",
    2625820422: "From the Grave",
    3588869844: "From the Void",
    690125105: "Grapple-jack",
    175594566: "Hold This",
    3091261182: "Last Shot",
    3475540930: "Lawnmower",
    1065136443: "Mount Up",
    1283796619: "Off the Rack",
    2861418269: "Quick Draw",
    3583966655: "Party's Over",
    2019283350: "Pineapple Express",
    1298835518: "Ramming Speed",
    1445036152: "Reclaimer",
    1169571763: "Shot Caller",
    1176569867: "Yard Sale",
    275666139: "Special Delivery",
    2967011722: "Street Sweeper",
    3732790338: "Fumble",
    781229683: "Straight Balling",
    1472686630: "Always Rotating",
    3630529364: "Clock Stop",
    221693153: "Splatter",
    3528500956: "All That Juice",
    1376646881: "Great Journey",
    629165579: "Power Outage",
    2750622016: "Breacher",
    1331361851: "Mounted & Loaded",
    2717755703: "Sole Survivor",
    1025827095: "Culling",
    88914608: "Blight",
    557309779: "Zombie Slayer",
    3467301935: "Purge",
    1155542859: "Disease",
    1447057920: "Undead Hunter",
    1064731598: "Untainted",
    1765213446: "Cleansing",
    3786134933: "Plague",
    217730222: "Hell's Janitor",
    17866865: "The Sickness",
    496411737: "Purification",
    1719203329: "Pestilence",
    2164872967: "Divine Intervention",
    3520382976: "Scourge",
    3653884673: "Apocalypse",
    394349536: "Clear Reception",
    4285712605: "Hang Up",
    2964157454: "Call Blocked",
    2426456555: "Secure Line",
    3931425309: "Signal Block",
    4007438389: "Blind Fire",
    1477806194: "Counter-snipe",
    1090931685: "Monopoly",
    580478179: "Hill Guardian",
    2848470465: "Death Cabbie",
    3169118333: "Driving Spree",
    1739996188: "Immortal Chauffeur",
    1053114074: "Clash of Kings",
    2125906504: "Big Deal",
    590706932: "Contract Killer",
    1210968206: "Watch the Throne",
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
