"""Models for the "skill" authority."""

from uuid import UUID

from spnkr.models.base import PascalCaseModel
from spnkr.models.refdata import SkillResultCode, SubTier, Tier
from spnkr.models.types import ReadOnlyDict


class CsrContainer(PascalCaseModel, frozen=True):
    """Container for a player's CSR info.

    Attributes:
        value: The player's CSR value.
        measurement_matches_remaining: The number of matches remaining until the player's CSR is determined.
        tier: The player's CSR tier.
        tier_start: The CSR value at which the player's current tier starts.
        sub_tier: The player's CSR sub-tier.
        next_tier: The player's next CSR tier.
        next_tier_start: The CSR value at which the player's next tier starts.
        next_sub_tier: The player's next CSR sub-tier.
        initial_measurement_matches: The number of matches required to determine the player's CSR.
    """

    value: int
    measurement_matches_remaining: int
    tier: Tier
    tier_start: int
    sub_tier: SubTier
    next_tier: Tier
    next_tier_start: int
    next_sub_tier: SubTier
    initial_measurement_matches: int


class RankRecap(PascalCaseModel, frozen=True):
    """Summary of the player's CSR change.

    Attributes:
        pre_match_csr: The player's CSR details before the match.
        post_match_csr: The player's CSR details after the match.
    """

    pre_match_csr: CsrContainer
    post_match_csr: CsrContainer


class StatPerformance(PascalCaseModel, frozen=True):
    """Comparison of actual to expected values for a game metric.

    Attributes:
        count: The actual value.
        expected: The expected value.
        std_dev: The standard deviation between actual and expected values.
    """

    count: int
    expected: float
    std_dev: float


class StatPerformances(PascalCaseModel, frozen=True):
    """Comparison of actual to expected values for game metrics.

    Attributes:
        kills: Comparison of actual to expected kills.
        deaths: Comparison of actual to expected deaths.
    """

    kills: StatPerformance
    deaths: StatPerformance


class Counterfactual(PascalCaseModel, frozen=True):
    """Expected performance for a given player or skill tier in a match.

    Attributes:
        kills: Expected kills.
        deaths: Expected deaths.
    """

    kills: float
    deaths: float


class Counterfactuals(PascalCaseModel, frozen=True):
    """Expected performances for the player and all skill tiers in a match.

    Attributes:
        self_counterfactuals: Expected performance for the player.
        tier_counterfactuals: Expected performances for all skill tiers.
    """

    self_counterfactuals: Counterfactual
    tier_counterfactuals: ReadOnlyDict[Tier, Counterfactual]


class RankedRewards(PascalCaseModel, frozen=True):
    """Rewards awarded to players based on skill acheivement.

    Attributes:
        reward_id: The ID of the player's reward.
    """

    reward_id: UUID


class MatchSkillResult(PascalCaseModel, frozen=True):
    """Skill data for a player in a match.

    Attributes:
        team_mmr: The MMR of the player's team.
        rank_recap: Summary of the player's CSR change.
        stat_performances: Comparison of actual to expected values for player performance metrics.
        team_id: The ID of the player's team.
        team_mmrs: The MMRs of all teams in the match.
        ranked_rewards: Always null.
        counterfactuals: Expected performances for the player and all skill tiers in a match.
    """

    team_mmr: float
    rank_recap: RankRecap
    stat_performances: StatPerformances
    team_id: int
    team_mmrs: ReadOnlyDict[int, float]
    ranked_rewards: RankedRewards | None
    counterfactuals: Counterfactuals


class MatchSkillValue(PascalCaseModel, frozen=True):
    """Skill data for a player in a match.

    Attributes:
        id: The player's Xbox Live ID.
        result_code: The status of the skill result.
        result: Skill data for a player in a match.
    """

    id: str
    result_code: SkillResultCode
    result: MatchSkillResult


class MatchSkill(PascalCaseModel, frozen=True):
    """Summary of skill data for teams and players in a match.

    Attributes:
        value: List of player skill data entries.
    """

    value: tuple[MatchSkillValue, ...]


class PlaylistCsrResult(PascalCaseModel, frozen=True):
    """CSR details for a player in a playlist.

    Attributes:
        current: Details on the player's current CSR in the playlist.
        season_max: Details on the player's highest CSR in the playlist for the season.
        all_time_max: Details on the player's highest CSR in the playlist for all seasons.
    """

    current: CsrContainer
    season_max: CsrContainer
    all_time_max: CsrContainer


class PlaylistCsrValue(PascalCaseModel, frozen=True):
    """Playlist CSR result for a single player.

    Attributes:
        id: The player's Xbox Live ID.
        result_code: The status of the skill result.
        result: CSR details for a player in a playlist.
    """

    id: str
    result_code: SkillResultCode
    result: PlaylistCsrResult


class PlaylistCsr(PascalCaseModel, frozen=True):
    """Summary of CSR data for players in a playlist.

    Attributes:
        value: List of playlist-player CSR entries.
    """

    value: tuple[PlaylistCsrValue, ...]
