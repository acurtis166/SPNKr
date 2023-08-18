"""Define models for the "get match skill" response."""

from pydantic import Field

from ..refdata import SkillResultCode, SubTier, Team, Tier
from .base import PascalCaseModel


class CsrContainer(PascalCaseModel):
    """Container for a player's CSR info.

    Attributes:
        value: The player's CSR value.
        measurement_matches_remaining: The number of matches remaining
            until the player's CSR is determined.
        tier: The player's CSR tier.
        tier_start: The CSR value at which the player's current tier
            starts.
        sub_tier: The player's CSR sub-tier.
        next_tier: The player's next CSR tier.
        next_tier_start: The CSR value at which the player's next tier
            starts.
        next_sub_tier: The player's next CSR sub-tier.
        initial_measurement_matches: The number of matches required to
            determine the player's CSR.
    """

    value: int = Field(ge=-1, le=3000)
    measurement_matches_remaining: int = Field(ge=0, le=10)
    tier: Tier
    tier_start: int = Field(ge=-1, le=3000, multiple_of=50)
    sub_tier: SubTier
    next_tier: Tier
    next_tier_start: int = Field(ge=-1, le=3000, multiple_of=50)
    next_sub_tier: SubTier
    initial_measurement_matches: int = Field(ge=0, le=10)


class RankRecap(PascalCaseModel):
    pre_match_csr: CsrContainer
    post_match_csr: CsrContainer


class StatPerformance(PascalCaseModel):
    expected: float


class StatPerformances(PascalCaseModel):
    kills: StatPerformance
    deaths: StatPerformance


class Counterfactual(PascalCaseModel):
    kills: float
    deaths: float


class Counterfactuals(PascalCaseModel):
    self_counterfactuals: Counterfactual
    tier_counterfactuals: dict[Tier, Counterfactual]


class MatchSkillResult(PascalCaseModel):
    team_mmr: float
    rank_recap: RankRecap
    stat_performances: StatPerformances
    team_id: Team
    team_mmrs: dict[Team, float]
    ranked_rewards: None
    counterfactuals: Counterfactuals


class MatchSkillValue(PascalCaseModel):
    id: str
    result_code: SkillResultCode
    result: MatchSkillResult


class MatchSkill(PascalCaseModel):
    value: list[MatchSkillValue]


class PlaylistCsrResult(PascalCaseModel):
    current: CsrContainer
    season_max: CsrContainer
    all_time_max: CsrContainer


class PlaylistCsrValue(PascalCaseModel):
    id: str
    result_code: SkillResultCode
    result: PlaylistCsrResult


class PlaylistCsr(PascalCaseModel):
    value: list[PlaylistCsrValue]
