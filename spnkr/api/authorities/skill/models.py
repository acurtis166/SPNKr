from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class CsrContainer:
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
        return CsrContainer(
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


@dataclass(frozen=True)
class StatPerformance:
    count: int
    expected: float
    std_dev: float

    @classmethod
    def from_dict(cls, data: dict) -> StatPerformance:
        return StatPerformance(
            count=data["Count"],
            expected=data["Expected"],
            std_dev=data["StdDev"],
        )


@dataclass(frozen=True)
class StatPerformances:
    kills: StatPerformance
    deaths: StatPerformance

    @classmethod
    def from_dict(cls, data: dict) -> StatPerformances:
        return StatPerformances(
            kills=StatPerformance.from_dict(data["Kills"]),
            deaths=StatPerformance.from_dict(data["Deaths"]),
        )


@dataclass(frozen=True)
class RankRecap:
    pre_match_csr: CsrContainer
    post_match_csr: CsrContainer

    @classmethod
    def from_dict(cls, data: dict) -> RankRecap:
        return RankRecap(
            pre_match_csr=CsrContainer.from_dict(data["PreMatchCsr"]),
            post_match_csr=CsrContainer.from_dict(data["PostMatchCsr"]),
        )


@dataclass(frozen=True)
class Counterfactual:
    kills: float
    deaths: float

    @classmethod
    def from_dict(cls, data: dict) -> Counterfactual:
        return Counterfactual(kills=data["Kills"], deaths=data["Deaths"])


@dataclass(frozen=True)
class TierCounterfactuals:
    bronze: Counterfactual
    silver: Counterfactual
    gold: Counterfactual
    platinum: Counterfactual
    diamond: Counterfactual
    onyx: Counterfactual

    @classmethod
    def from_dict(cls, data: dict) -> TierCounterfactuals:
        return TierCounterfactuals(
            bronze=Counterfactual.from_dict(data["Bronze"]),
            silver=Counterfactual.from_dict(data["Silver"]),
            gold=Counterfactual.from_dict(data["Gold"]),
            platinum=Counterfactual.from_dict(data["Platinum"]),
            diamond=Counterfactual.from_dict(data["Diamond"]),
            onyx=Counterfactual.from_dict(data["Onyx"]),
        )


@dataclass(frozen=True)
class Counterfactuals:
    self_counterfactuals: Counterfactual
    tier_counterfactuals: TierCounterfactuals | None

    @classmethod
    def from_dict(cls, data: dict) -> Counterfactuals:
        tier_counterfactuals = None
        if data["TierCounterfactuals"]:
            tier_counterfactuals = TierCounterfactuals.from_dict(
                data["TierCounterfactuals"]
            )
        return Counterfactuals(
            self_counterfactuals=Counterfactual.from_dict(
                data["SelfCounterfactuals"]
            ),
            tier_counterfactuals=tier_counterfactuals,
        )


@dataclass(frozen=True)
class RankedRewards:
    reward_id: uuid.UUID
    awarded_rewards: dict[str, uuid.UUID]

    @classmethod
    def from_dict(cls, data: dict) -> RankedRewards:
        return RankedRewards(
            reward_id=uuid.UUID(data["RewardId"]),
            awarded_rewards={
                k: uuid.UUID(v) for k, v in data["AwardedRewards"].items()
            },
        )


@dataclass(frozen=True)
class SkillResult:
    team_mmr: float
    rank_recap: RankRecap
    stat_performances: StatPerformances
    team_id: int
    team_mmrs: dict[int, float]  # keys are strings of team ids (e.g., "0")
    ranked_rewards: None
    counterfactuals: Counterfactuals

    @classmethod
    def from_dict(cls, data: dict) -> SkillResult:
        return SkillResult(
            team_mmr=data["TeamMmr"],
            rank_recap=RankRecap.from_dict(data["RankRecap"]),
            stat_performances=StatPerformances.from_dict(
                data["StatPerformances"]
            ),
            team_id=data["TeamId"],
            team_mmrs={int(k): v for k, v in data["TeamMmrs"].items()},
            ranked_rewards=None,
            counterfactuals=Counterfactuals.from_dict(data["Counterfactuals"]),
        )


@dataclass(frozen=True)
class SkillResultContainer:
    id: str
    result_code: int
    result: SkillResult

    @classmethod
    def from_dict(cls, data: dict) -> SkillResultContainer:
        return SkillResultContainer(
            id=data["Id"],
            result_code=data["ResultCode"],
            result=SkillResult.from_dict(data["Result"]),
        )


@dataclass(frozen=True)
class MatchSkillInfo:
    value: list[SkillResultContainer]

    @classmethod
    def from_dict(cls, data: dict) -> MatchSkillInfo:
        return MatchSkillInfo(
            value=[SkillResultContainer.from_dict(d) for d in data["Value"]]
        )


@dataclass(frozen=True)
class PlaylistCsrContainer:
    current: CsrContainer
    season_max: CsrContainer
    all_time_max: CsrContainer

    @classmethod
    def from_dict(cls, data: dict) -> PlaylistCsrContainer:
        return PlaylistCsrContainer(
            current=CsrContainer.from_dict(data["Current"]),
            season_max=CsrContainer.from_dict(data["SeasonMax"]),
            all_time_max=CsrContainer.from_dict(data["AllTimeMax"]),
        )


@dataclass(frozen=True)
class PlayerPlaylistCsrResult:
    id: str
    result_code: int
    result: PlaylistCsrContainer

    @classmethod
    def from_dict(cls, data: dict) -> PlayerPlaylistCsrResult:
        return PlayerPlaylistCsrResult(
            id=data["Id"],
            result_code=data["ResultCode"],
            result=PlaylistCsrContainer.from_dict(data["Result"]),
        )


@dataclass(frozen=True)
class PlaylistCsrInfo:
    value: list[PlayerPlaylistCsrResult]

    @classmethod
    def from_dict(cls, data: dict) -> PlaylistCsrInfo:
        return PlaylistCsrInfo(
            value=[PlayerPlaylistCsrResult.from_dict(d) for d in data["Value"]]
        )
