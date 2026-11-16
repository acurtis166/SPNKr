import math
from dataclasses import dataclass

from spnkr.models.refdata import SubTier, Tier

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


@dataclass(frozen=True)
class CompetitiveSkillRank:
    """Represents a Competitive Skill Rank (CSR).

    CSR is broken up into a rank/tier and sub-rank/sub-tier. Each tier increment
    (Bronze to Onyx) represents an increase of 300 points and each sub-tier increment
    (1-6) represents an increase of 50 points (Onyx doesn't have sub-tiers).
    Bronze 1 starts at 0 and any value greater than or equal to 1500 is Onyx rank.

    - BRONZE (1-6)
    - SILVER (1-6)
    - GOLD (1-6)
    - PLATINUM (1-6)
    - DIAMOND (1-6)
    - ONYX

    Attributes:
        csr: The CSR value.

    Examples:
        >>> from spnkr.extras import CompetitiveSkillRank
        >>> str(CompetitiveSkillRank(25))
        'Bronze I'
        >>>
        >>> csr = CompetitiveSkillRank(1065)
        >>> (csr.tier, csr.sub_tier)
        (<Tier.PLATINUM: 'Platinum'>, <SubTier.IV: 3>)
    """

    csr: int | float

    TIERS = [
        Tier.BRONZE,
        Tier.SILVER,
        Tier.GOLD,
        Tier.PLATINUM,
        Tier.DIAMOND,
        Tier.ONYX,
    ]

    @property
    def tier(self) -> Tier:
        """The tier of the ranking (e.g., "Diamond")."""
        return self.TIERS[min(math.floor(self.csr) // 300, 5)]

    @property
    def sub_tier(self) -> SubTier:
        """The sub-tier of the ranking (1-6).

        Onyx doesn't have sub-tiers, but a return value of `SubTier.I` in that case
        aligns with the skill payload.
        """
        if self.tier is Tier.ONYX:
            return SubTier.I
        return SubTier((math.floor(self.csr) % 300) // 50)  # SubTier is 0-based

    def __str__(self) -> str:
        if self.tier is Tier.ONYX:
            return self.tier.value
        return f"{self.tier.value} {self.sub_tier.name}"
