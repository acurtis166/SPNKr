
from dataclasses import dataclass
import uuid

from spnkr.models import PascalModel


@dataclass
class CsrContainer(PascalModel):
    value: int
    measurement_matches_remaining: int
    tier: str
    tier_start: int
    sub_tier: int
    next_tier: str
    next_tier_start: int
    next_sub_tier: int
    initial_measurement_matches: int


@dataclass
class StatPerformance(PascalModel):
    count: int
    expected: float
    std_dev: float


@dataclass
class StatPerformances(PascalModel):
    kills: StatPerformance
    deaths: StatPerformance


@dataclass
class RankRecap(PascalModel):
    pre_match_csr: CsrContainer
    post_match_csr: CsrContainer


@dataclass
class Counterfactual(PascalModel):
    kills: float
    deaths: float


@dataclass
class TierCounterfactuals(PascalModel):
    bronze: Counterfactual | None = None
    silver: Counterfactual | None = None
    gold: Counterfactual | None = None
    platinum: Counterfactual | None = None
    diamond: Counterfactual | None = None
    onyx: Counterfactual | None = None


@dataclass
class Counterfactuals(PascalModel):
    self_counterfactuals: Counterfactual
    tier_counterfactuals: TierCounterfactuals


@dataclass
class RankedRewards(PascalModel):
    reward_id: uuid.UUID
    awarded_rewards: dict[str, uuid.UUID]


@dataclass
class SkillResult(PascalModel):
    team_mmr: float
    rank_recap: RankRecap
    stat_performances: StatPerformances
    team_id: int
    team_mmrs: dict[int, float]  # keys are strings of team ids (e.g., "0")
    ranked_rewards: None
    counterfactuals: Counterfactuals


@dataclass
class SkillResultContainer(PascalModel):
    id: str
    result_code: int
    result: SkillResult


@dataclass
class MatchSkillInfo(PascalModel):
    value: list[SkillResultContainer]


@dataclass
class PlaylistCsrContainer(PascalModel):
    current: CsrContainer
    season_max: CsrContainer
    all_time_max: CsrContainer


@dataclass
class PlayerPlaylistCsrResult(PascalModel):
    id: str
    result_code: int
    result: PlaylistCsrContainer


@dataclass
class PlaylistCsrInfo(PascalModel):
    value: list[PlayerPlaylistCsrResult]

