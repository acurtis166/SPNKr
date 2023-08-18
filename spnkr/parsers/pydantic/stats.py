import datetime as dt
from uuid import UUID

from pydantic import Field

from ..refdata import (
    AssetKind,
    BotDifficulty,
    GameVariantCategory,
    LifecycleMode,
    Outcome,
    PlayerType,
    PlaylistExperience,
    Team,
)
from .base import PascalCaseModel


class MatchCount(PascalCaseModel):
    custom_matches_played_count: int = Field(ge=0)
    matches_played_count: int = Field(ge=0)
    matchmade_matches_played_count: int = Field(ge=0)
    local_matches_played_count: int = Field(ge=0)


class Asset(PascalCaseModel):
    asset_kind: AssetKind
    asset_id: UUID
    version_id: UUID


class MatchInfo(PascalCaseModel):
    start_time: dt.datetime
    end_time: dt.datetime
    duration: dt.timedelta
    lifecycle_mode: LifecycleMode
    game_variant_category: GameVariantCategory
    level_id: UUID
    map_variant: Asset
    ugc_game_variant: Asset
    clearance_id: UUID
    playlist: Asset
    playlist_experience: PlaylistExperience
    playlist_map_mode_pair: Asset
    season_id: str
    playable_duration: dt.timedelta
    teams_enabled: bool
    team_scoring_enabled: bool


class MatchHistoryResult(PascalCaseModel):
    match_id: UUID
    match_info: MatchInfo
    last_team_id: Team
    outcome: Outcome
    rank: int = Field(ge=1)
    present_at_end_of_match: bool


class MatchHistory(PascalCaseModel):
    start: int = Field(ge=0)
    count: int = Field(ge=0)
    result_count: int = Field(ge=0, le=25)
    results: list[MatchHistoryResult]


class AwardCount(PascalCaseModel):
    name_id: int
    count: int
    total_personal_score_awarded: int


class CoreStats(PascalCaseModel):
    score: int
    personal_score: int
    rounds_won: int
    rounds_lost: int
    rounds_tied: int
    kills: int
    deaths: int
    assists: int
    kda: float
    suicides: int
    betrayals: int
    average_life_duration: dt.timedelta
    grenade_kills: int
    headshot_kills: int
    melee_kills: int
    power_weapon_kills: int
    shots_fired: int
    shots_hit: int
    accuracy: float
    damage_dealt: int
    damage_taken: int
    callout_assists: int
    vehicle_destroys: int
    driver_assists: int
    hijacks: int
    emp_assists: int
    max_killing_spree: int
    medals: list[AwardCount]
    personal_scores: list[AwardCount]
    deprecated_damage_dealt: float
    deprecated_damage_taken: float
    spawns: int


class BombStats(PascalCaseModel):
    bomb_carriers_killed: int
    bomb_defusals: int
    bomb_defusers_killed: int
    bomb_detonations: int
    bomb_pick_ups: int
    bomb_plants: int
    bomb_returns: int
    kills_as_bomb_carrier: int
    time_as_bomb_carrier: dt.timedelta


class CaptureTheFlagStats(PascalCaseModel):
    flag_capture_assists: int
    flag_captures: int
    flag_carriers_killed: int
    flag_grabs: int
    flag_returners_killed: int
    flag_returns: int
    flag_secures: int
    flag_steals: int
    kills_as_flag_carrier: int
    kills_as_flag_returner: int
    time_as_flag_carrier: dt.timedelta


class EliminationStats(PascalCaseModel):
    allies_revived: int
    elimination_assists: int
    eliminations: int
    enemy_revives_denied: int
    executions: int
    kills_as_last_player_standing: int
    last_players_standing_killed: int
    rounds_survived: int
    times_revived_by_ally: int
    lives_remaining: int | None
    elimination_order: int


class ExtractionStats(PascalCaseModel):
    extraction_conversions_completed: int
    extraction_conversions_denied: int
    extraction_initiations_completed: int
    extraction_initiations_denied: int
    successful_extractions: int


class InfectionStats(PascalCaseModel):
    pass


class OddballStats(PascalCaseModel):
    kills_as_skull_carrier: int
    longest_time_as_skull_carrier: dt.timedelta
    skull_carriers_killed: int
    skull_grabs: int
    time_as_skull_carrier: dt.timedelta
    skull_scoring_ticks: int


class ZonesStats(PascalCaseModel):
    stronghold_captures: int
    stronghold_defensive_kills: int
    stronghold_offensive_kills: int
    stronghold_secures: int
    stronghold_occupation_time: dt.timedelta
    stronghold_scoring_ticks: int


class StockpileStats(PascalCaseModel):
    kills_as_power_seed_carrier: int
    power_seeds_deposited: int
    power_seeds_stolen: int
    power_seed_carriers_killed: int
    time_as_power_seed_carrier: dt.timedelta
    time_as_power_seed_driver: dt.timedelta


class Stats(PascalCaseModel):
    core_stats: CoreStats
    bomb_stats: BombStats | None
    capture_the_flag_stats: CaptureTheFlagStats | None
    elimination_stats: EliminationStats | None
    extraction_stats: ExtractionStats | None
    infection_stats: InfectionStats | None
    oddball_stats: OddballStats | None
    zones_stats: ZonesStats | None
    stockpile_stats: StockpileStats | None


class TeamStats(PascalCaseModel):
    team_id: Team
    outcome: Outcome
    rank: int = Field(ge=1)
    stats: Stats


class BotAttributes(PascalCaseModel):
    difficulty: BotDifficulty


class ParticipationInfo(PascalCaseModel):
    first_joined_time: dt.datetime
    last_leave_time: dt.datetime | None
    present_at_beginning: bool
    joined_in_progress: bool
    left_in_progress: bool
    present_at_completion: bool
    time_played: dt.timedelta
    confirmed_participation: bool | None


class PlayerTeamStats(PascalCaseModel):
    team_id: Team
    stats: Stats


class PlayerStats(PascalCaseModel):
    player_id: str
    player_type: PlayerType
    bot_attributes: BotAttributes | None
    last_team_id: Team
    outcome: Outcome
    rank: int = Field(ge=1)
    participation_info: ParticipationInfo
    player_team_stats: list[PlayerTeamStats]


class MatchStats(PascalCaseModel):
    match_id: UUID
    match_info: MatchInfo
    teams: list[TeamStats]
    players: list[PlayerStats]
