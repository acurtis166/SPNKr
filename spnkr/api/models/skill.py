"""Models for the skill authority."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CsrContainer:
    """Container for a player's CSR info.

    Attributes:
        value (int): The player's CSR value.
        measurement_matches_remaining (int): The number of matches remaining
            until the player's CSR is determined.
        tier (str): The player's CSR tier.
        tier_start (int): The CSR value at which the player's current tier
            starts.
        sub_tier (int): The player's CSR sub-tier.
        next_tier (str): The player's next CSR tier.
        next_tier_start (int): The CSR value at which the player's next tier
            starts.
        next_sub_tier (int): The player's next CSR sub-tier.
        initial_measurement_matches (int): The number of matches required to
            determine the player's CSR.
    """

    value: int
    measurement_matches_remaining: int
    tier: str
    tier_start: int
    sub_tier: int
    next_tier: str
    next_tier_start: int
    next_sub_tier: int
    initial_measurement_matches: int

    @classmethod
    def from_dict(cls, data: dict) -> CsrContainer:
        return cls(
            value=data["Value"],
            measurement_matches_remaining=data["MeasurementMatchesRemaining"],
            tier=data["Tier"],
            tier_start=data["TierStart"],
            sub_tier=data["SubTier"],
            next_tier=data["NextTier"],
            next_tier_start=data["NextTierStart"],
            next_sub_tier=data["NextSubTier"],
            initial_measurement_matches=data["InitialMeasurementMatches"],
        )


@dataclass(frozen=True, slots=True)
class MatchSkillResult:
    """Container for a player's skill info for a specific match.

    Attributes:
        id (str): The player's Xbox Live ID, wrapped in `xuid()`.
        result_code (int): The result code. A result code of 0 indicates that
            the result is reliable. A convenience property `is_valid` is
            provided to determine whether the result is reliable.
        is_valid (bool): Whether the result is reliable.
        team_mmr (float): The player's team MMR.
        pre_match_csr (CsrContainer): The player's CSR info before the match.
        post_match_csr (CsrContainer): The player's CSR info after the match.
        team_id (int): The player's team ID.
        team_mmrs (dict[int, float]): The team MMRs for each team. Keys are
            integers of team IDs.
        expected_kills (float): The player's expected kills.
        expected_deaths (float): The player's expected deaths.
    """

    id: str
    result_code: int
    is_valid: bool
    team_mmr: float
    pre_match_csr: CsrContainer
    post_match_csr: CsrContainer
    team_id: int
    team_mmrs: dict[int, float]
    expected_kills: float
    expected_deaths: float

    @classmethod
    def from_dict(cls, data: dict) -> MatchSkillResult:
        """Create a new instance from a dictionary."""
        rank_recap = data["Result"]["RankRecap"]
        performance = data["Result"]["StatPerformances"]
        return cls(
            id=data["Id"],
            result_code=data["ResultCode"],
            is_valid=data["ResultCode"] == 0,
            team_mmr=data["Result"]["TeamMmr"],
            pre_match_csr=CsrContainer.from_dict(rank_recap["PreMatchCsr"]),
            post_match_csr=CsrContainer.from_dict(rank_recap["PostMatchCsr"]),
            team_id=data["Result"]["TeamId"],
            team_mmrs={
                int(k): v for k, v in data["Result"]["TeamMmrs"].items()
            },
            expected_kills=performance["Kills"]["Expected"],
            expected_deaths=performance["Deaths"]["Expected"],
        )


@dataclass(frozen=True, slots=True)
class MatchSkillResponse:
    """Skill data for a given match.

    Attributes:
        raw (dict): The raw data returned by the API.
        results (dict[MatchSkillResult]): The skill data for each player in the
            match. Keys are player Xbox Live IDs.
    """

    raw: dict
    results: dict[str, MatchSkillResult]

    @classmethod
    def from_dict(cls, data: dict) -> MatchSkillResponse:
        """Create a new instance from a dictionary."""
        results = {
            r["Id"]: MatchSkillResult.from_dict(r) for r in data["Value"]
        }
        return cls(data, results)


@dataclass(frozen=True, slots=True)
class PlaylistCsrResult:
    """Container for a player's CSR info for a specific playlist.

    Attributes:
        id (str): The player's Xbox Live ID, wrapped in `xuid()`.
        result_code (int): The result code. A result code of 0 indicates that
            the result is reliable. A convenience property `is_valid` is
            provided to determine whether the result is reliable.
        is_valid (bool): Whether the result is reliable.
        current (CsrContainer): The player's current CSR info.
        season_max (CsrContainer): The player's max CSR info for the current
            season.
        all_time_max (CsrContainer): The player's all-time max CSR info.
    """

    id: str
    result_code: int
    is_valid: bool
    current: CsrContainer
    season_max: CsrContainer
    all_time_max: CsrContainer

    @classmethod
    def from_dict(cls, data: dict) -> PlaylistCsrResult:
        """Create a new instance from a dictionary."""
        return cls(
            id=data["Id"],
            result_code=data["ResultCode"],
            is_valid=data["ResultCode"] == 0,
            current=CsrContainer.from_dict(data["Result"]["Current"]),
            season_max=CsrContainer.from_dict(data["Result"]["SeasonMax"]),
            all_time_max=CsrContainer.from_dict(data["Result"]["AllTimeMax"]),
        )


@dataclass(frozen=True, slots=True)
class PlaylistCsrResponse:
    """Skill data for a given playlist.

    Attributes:
        raw (dict): The raw data returned by the API.
        results (dict[str, PlaylistCsrResult]): The skill data for each
            player requested. Keys are player Xbox Live IDs.
    """

    raw: dict
    results: dict[str, PlaylistCsrResult]

    @classmethod
    def from_dict(cls, data: dict) -> PlaylistCsrResponse:
        """Create a new instance from a dictionary."""
        results = {
            r["Id"]: PlaylistCsrResult.from_dict(r) for r in data["Value"]
        }
        return cls(data, results)
