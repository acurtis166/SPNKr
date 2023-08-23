"""Models for the "skill" authority."""

from uuid import UUID
from ..refdata import SkillResultCode, SubTier, Tier
from .base import PascalCaseModel


class CsrContainer(PascalCaseModel):
    """Container for a player's CSR info."""

    value: int
    """The player's CSR value."""
    measurement_matches_remaining: int
    """The number of matches remaining until the player's CSR is determined."""
    tier: Tier
    """The player's CSR tier."""
    tier_start: int
    """The CSR value at which the player's current tier starts."""
    sub_tier: SubTier
    """The player's CSR sub-tier."""
    next_tier: Tier
    """The player's next CSR tier."""
    next_tier_start: int
    """The CSR value at which the player's next tier starts."""
    next_sub_tier: SubTier
    """The player's next CSR sub-tier."""
    initial_measurement_matches: int
    """The number of matches required to determine the player's CSR."""


class RankRecap(PascalCaseModel):
    """Summary of the player's CSR change."""

    pre_match_csr: CsrContainer
    """The player's CSR details before the match."""
    post_match_csr: CsrContainer
    """The player's CSR details after the match."""


class StatPerformance(PascalCaseModel):
    """Comparison of actual to expected values for a game metric."""

    count: int
    """The actual value."""
    expected: float
    """The expected value."""
    std_dev: float
    """The standard deviation between actual and expected values."""


class StatPerformances(PascalCaseModel):
    """Comparison of actual to expected values for game metrics."""

    kills: StatPerformance
    """Comparison of actual to expected kills."""
    deaths: StatPerformance
    """Comparison of actual to expected deaths."""


class Counterfactual(PascalCaseModel):
    """Expected performance for a given player or skill tier in a match."""

    kills: float
    """Expected kills."""
    deaths: float
    """Expected deaths."""


class Counterfactuals(PascalCaseModel):
    """Expected performances for the player and all skill tiers in a match."""

    self_counterfactuals: Counterfactual
    """Expected performance for the player."""
    tier_counterfactuals: dict[Tier, Counterfactual]
    """Expected performances for all skill tiers."""


class RankedRewards(PascalCaseModel):
    """Rewards awarded to players based on skill acheivement."""

    reward_id: UUID
    """The ID of the player's reward."""


class MatchSkillResult(PascalCaseModel):
    """Skill data for a player in a match."""

    team_mmr: float
    """The MMR of the player's team."""
    rank_recap: RankRecap
    """Summary of the player's CSR change."""
    stat_performances: StatPerformances
    """Comparison of actual to expected values for player performance metrics."""
    team_id: int
    """The ID of the player's team."""
    team_mmrs: dict[int, float]
    """The MMRs of all teams in the match."""
    ranked_rewards: RankedRewards | None
    """Always null."""
    counterfactuals: Counterfactuals
    """Expected performances for the player and all skill tiers in a match."""


class MatchSkillValue(PascalCaseModel):
    """Skill data for a player in a match."""

    id: str
    """The player's Xbox Live ID."""
    result_code: SkillResultCode
    """The status of the skill result."""
    result: MatchSkillResult
    """Skill data for a player in a match."""


class MatchSkill(PascalCaseModel):
    """Summary of skill data for teams and players in a match."""

    value: list[MatchSkillValue]
    """List of player skill data entries."""


class PlaylistCsrResult(PascalCaseModel):
    """CSR details for a player in a playlist."""

    current: CsrContainer
    """Details on the player's current CSR in the playlist."""
    season_max: CsrContainer
    """Details on the player's highest CSR in the playlist for the season."""
    all_time_max: CsrContainer
    """Details on the player's highest CSR in the playlist for all seasons."""


class PlaylistCsrValue(PascalCaseModel):
    """Playlist CSR result for a single player."""

    id: str
    """The player's Xbox Live ID."""
    result_code: SkillResultCode
    """The status of the skill result."""
    result: PlaylistCsrResult
    """CSR details for a player in a playlist."""


class PlaylistCsr(PascalCaseModel):
    """Summary of CSR data for players in a playlist."""

    value: list[PlaylistCsrValue]
    """List of playlist-player CSR entries."""
