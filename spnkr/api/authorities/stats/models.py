
from dataclasses import dataclass
import datetime as dt
from uuid import UUID

from spnkr.api import enums
from spnkr.models import PascalModel


@dataclass
class MatchCount(PascalModel):
    custom_matches_played_count: int
    matches_played_count: int
    matchmade_matches_played_count: int
    local_matches_played_count: int


@dataclass
class AssetStub(PascalModel):
    asset_kind: enums.AssetKind
    asset_id: UUID
    version_id: UUID


@dataclass
class MatchInfo(PascalModel):
    start_time: dt.datetime
    end_time: dt.datetime
    duration: dt.timedelta
    lifecycle_mode: enums.LifecycleMode
    game_variant_category: enums.GameVariantCategory
    level_id: UUID
    map_variant: AssetStub
    ugc_game_variant: AssetStub
    clearance_id: UUID
    playlist: AssetStub | None
    playlist_experience: enums.PlaylistExperience | None
    playlist_map_mode_pair: AssetStub | None
    season_id: str
    playable_duration: dt.timedelta
    teams_enabled: bool
    team_scoring_enabled: bool


@dataclass
class PlayerMatchHistoryRecord(PascalModel):
    match_id: UUID
    match_info: MatchInfo
    last_team_id: int
    outcome: enums.Outcome
    rank: int
    present_at_end_of_match: bool


@dataclass
class Links(PascalModel):
    pass


@dataclass
class MatchHistoryResponse(PascalModel):
    start: int
    count: int
    result_count: int
    results: list[PlayerMatchHistoryRecord]
    links: Links


@dataclass
class MatchResultPersonalScoreStats(PascalModel):
    name_id: int
    count: int
    total_personal_score_awarded: int


@dataclass
class MatchResultMedalStats(PascalModel):
    name_id: int
    count: int
    total_personal_score_awarded: int


@dataclass
class CoreStats(PascalModel):
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
    medals: list[MatchResultMedalStats]
    personal_scores: list[MatchResultPersonalScoreStats]
    deprecated_damage_dealt: float
    deprecated_damage_taken: float
    spawns: int


@dataclass
class BombStats(PascalModel):
    bomb_carriers_killed: int
    bomb_defusals: int
    bomb_defusers_killed: int
    bomb_detonations: int
    bomb_pick_ups: int
    bomb_plants: int
    bomb_returns: int
    kills_as_bomb_carrier: int
    time_as_bomb_carrier: dt.timedelta


@dataclass
class CaptureTheFlagStats(PascalModel):
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


@dataclass
class EliminationStats(PascalModel):
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


@dataclass
class ExtractionStats(PascalModel):
    extraction_conversions_completed: int
    extraction_conversions_denied: int
    extraction_initiations_completed: int
    extraction_initiations_denied: int
    successful_extractions: int


@dataclass
class InfectionStats(PascalModel):
    pass


@dataclass
class OddballStats(PascalModel):
    kills_as_skull_carrier: int
    longest_time_as_skull_carrier: dt.timedelta
    skull_carriers_killed: int
    skull_grabs: int
    time_as_skull_carrier: dt.timedelta
    skull_scoring_ticks: int


@dataclass
class ZonesStats(PascalModel):
    zone_captures: int
    zone_defensive_kills: int
    zone_offensive_kills: int
    zone_secures: int
    total_zone_occupation_time: dt.timedelta
    zone_scoring_ticks: int


@dataclass
class StockpileStats(PascalModel):
    kills_as_power_seed_carrier: int
    power_seeds_deposited: int
    power_seeds_stolen: int
    power_seed_carriers_killed: int
    time_as_power_seed_carrier: dt.timedelta
    time_as_power_seed_driver: dt.timedelta


@dataclass
class Stats(PascalModel):
    core_stats: CoreStats
    bomb_stats: BombStats | None
    capture_the_flag_stats: CaptureTheFlagStats | None
    elimination_stats: EliminationStats | None
    extraction_stats: ExtractionStats | None
    infection_stats: InfectionStats | None
    oddball_stats: OddballStats | None
    zones_stats: ZonesStats | None
    stockpile_stats: StockpileStats | None


@dataclass
class Team(PascalModel):
    team_id: int
    outcome: enums.Outcome
    rank: int
    stats: Stats


@dataclass
class BotAttributes(PascalModel):
    difficulty: enums.BotDifficulty


@dataclass
class ParticipationInfo(PascalModel):
    first_joined_time: dt.datetime
    last_leave_time: dt.datetime | None
    present_at_beginning: bool
    joined_in_progress: bool
    left_in_progress: bool
    present_at_completion: bool
    time_played: dt.timedelta
    confirmed_participation: bool | None


@dataclass
class PlayerTeamStats(PascalModel):
    team_id: int
    stats: Stats


@dataclass
class Player(PascalModel):
    player_id: str
    player_type: enums.PlayerType
    bot_attributes: BotAttributes | None
    last_team_id: int
    outcome: int
    rank: int
    participation_info: ParticipationInfo
    player_team_stats: list[PlayerTeamStats]


@dataclass
class MatchStats(PascalModel):
    match_id: UUID
    match_info: MatchInfo
    teams: list[Team]
    players: list[Player]

