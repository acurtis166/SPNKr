"""Models for the stats authority."""

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
)
from .base import PascalCaseModel


class MatchCount(PascalCaseModel):
    """A player's match count summary."""

    custom_matches_played_count: int
    """The number of custom matches the player has played."""
    matches_played_count: int
    """The number of matches the player has played."""
    matchmade_matches_played_count: int
    """The number of matchmade matches the player has played."""
    local_matches_played_count: int
    """The number of local matches the player has played."""


class Asset(PascalCaseModel):
    """ID information about a game asset, such as a map or game mode."""

    asset_kind: AssetKind
    """The kind of asset, such as "map variant" or "playlist"."""
    asset_id: UUID
    """The asset's GUID."""
    version_id: UUID
    """The asset version's GUID."""


class MatchInfo(PascalCaseModel):
    """Information about a match."""

    start_time: dt.datetime
    """The UTC datetime when the match started."""
    end_time: dt.datetime
    """The UTC datetime when the match ended."""
    duration: dt.timedelta
    """The match's duration."""
    lifecycle_mode: LifecycleMode
    """The match's lifecycle mode."""
    game_variant_category: GameVariantCategory
    """The game mode category."""
    level_id: UUID
    """The ID of the level the match was played on."""
    map_variant: Asset
    """The map the match was played on."""
    ugc_game_variant: Asset
    """The game mode the match was played with."""
    clearance_id: UUID
    playlist: Asset | None
    """The playlist the match was made in, if the match was matchmade."""
    playlist_experience: PlaylistExperience | None
    """The general category of playlist the match was made in, if the match was matchmade."""
    playlist_map_mode_pair: Asset | None
    """The map and game mode the match was made in, if the match was matchmade."""
    season_id: str | None
    """The ID of the season the match was played in, if the match was matchmade."""
    playable_duration: dt.timedelta
    """The match's playable duration."""
    teams_enabled: bool
    """Whether teams were enabled in the match."""
    team_scoring_enabled: bool
    """Whether team scoring was enabled in the match."""


class MatchHistoryResult(PascalCaseModel):
    """A match history entry."""

    match_id: UUID
    """The match's GUID."""
    match_info: MatchInfo
    """Information about the match."""
    last_team_id: int
    """The ID of the last team the player was on."""
    outcome: Outcome
    """The player's outcome in the match."""
    rank: int
    """The player's rank in the match."""
    present_at_end_of_match: bool
    """Whether the player was present at the end of the match."""


class MatchHistory(PascalCaseModel):
    """A page of a player's match history."""

    start: int
    """The index of the first match in the page. 0 is the most recent match."""
    count: int
    """The number of matches requested."""
    result_count: int
    """The actual number of matches in the page."""
    results: list[MatchHistoryResult]
    """The matches in the page."""


class AwardCount(PascalCaseModel):
    """A count of a medal or personal score award."""

    name_id: int
    """The ID of the medal or personal score award."""
    count: int
    """The number of times the medal or personal score award was earned."""
    total_personal_score_awarded: int
    """The total personal score awarded by obtaining the medal or personal score award."""


class CoreStats(PascalCaseModel):
    """Core statistics about a player or team performance in a match."""

    score: int
    """Earned points related to the match outcome."""
    personal_score: int
    """Earned points related to personal performance."""
    rounds_won: int
    """The number of rounds won."""
    rounds_lost: int
    """The number of rounds lost."""
    rounds_tied: int
    """The number of rounds tied."""
    kills: int
    """The number of kills."""
    deaths: int
    """The number of deaths."""
    assists: int
    """The number of assists."""
    kda: float = Field(alias="KDA")
    """Kill-death-assist metric (kills + assists / 3 - deaths)."""
    suicides: int
    """Number of times committed suicide."""
    betrayals: int
    """Number of times teammates were killed."""
    average_life_duration: dt.timedelta
    """Average time between deaths."""
    grenade_kills: int
    """Number of kills using grenades."""
    headshot_kills: int
    """Number of kills with headshots."""
    melee_kills: int
    """Number of kills with melee or a melee weapon."""
    power_weapon_kills: int
    """Number of kills with "power" weapons."""
    shots_fired: int
    """Number of shots fired with weapons."""
    shots_hit: int
    """Number of shots hit with weapons."""
    accuracy: float
    """Accuracy of shots fired (shots_fired / shots_hit * 100)."""
    damage_dealt: int
    """Amount of damage dealt."""
    damage_taken: int
    """Amount of damage taken."""
    callout_assists: int
    """Number of assists earned by "marking" an enemy."""
    vehicle_destroys: int
    """Number of vehicles destroyed."""
    driver_assists: int
    """Number of assists earned by driving a teammate that gets a kill."""
    hijacks: int
    """Number of times hijacking a vehicle."""
    emp_assists: int
    """Number of assists earned by EMPing an enemy player or vehicle."""
    max_killing_spree: int
    """Maximum number of kills without dying."""
    medals: list[AwardCount]
    """Medals earned."""
    personal_scores: list[AwardCount]
    """Personal score awards earned."""
    deprecated_damage_dealt: float
    """Deprecated. Use damage_dealt instead."""
    deprecated_damage_taken: float
    """Deprecated. Use damage_taken instead."""
    spawns: int
    """Number of times spawned."""


class BombStats(PascalCaseModel):
    """Performance statistics for bomb game modes."""

    bomb_carriers_killed: int
    """Number of times an enemy bomb carrier was killed."""
    bomb_defusals: int
    """Number of times a bomb was defused."""
    bomb_defusers_killed: int
    """Number of times an enemy bomb defuser was killed."""
    bomb_detonations: int
    """Number of times a bomb was detonated."""
    bomb_pick_ups: int
    """Number of times a bomb was picked up."""
    bomb_plants: int
    """Number of times a bomb was planted."""
    bomb_returns: int
    """Number of times a bomb was returned."""
    kills_as_bomb_carrier: int
    """Number of kills while carrying the bomb."""
    time_as_bomb_carrier: dt.timedelta
    """Total time spent carrying the bomb."""


class CaptureTheFlagStats(PascalCaseModel):
    """Performance statistics for capture the flag game modes."""

    flag_capture_assists: int
    """Number of times contributing to a flag capture."""
    flag_captures: int
    """Number of times the enemy flag was captured."""
    flag_carriers_killed: int
    """Number of times an enemy flag carrier was killed."""
    flag_grabs: int
    """Number of times the enemy flag was grabbed."""
    flag_returners_killed: int
    """Number of times an enemy flag returner was killed."""
    flag_returns: int
    """Number of times the team flag was returned."""
    flag_secures: int
    """Number of times the team flag was secured."""
    flag_steals: int
    """Number of times stealing a flag."""
    kills_as_flag_carrier: int
    """Number of kills while carrying the flag."""
    kills_as_flag_returner: int
    """Number of kills while returning the flag."""
    time_as_flag_carrier: dt.timedelta
    """Total time spent carrying the flag."""


class EliminationStats(PascalCaseModel):
    """Performance statistics for elimination game modes."""

    allies_revived: int
    """Number of times reviving a teammate."""
    elimination_assists: int
    """Number of times contributing to an elimination."""
    eliminations: int
    """Number of times eliminating an enemy."""
    enemy_revives_denied: int
    """Number of times denying an enemy revive."""
    executions: int
    """Number of times executing an enemy."""
    kills_as_last_player_standing: int
    """Number of kills as the last player standing."""
    last_players_standing_killed: int
    """Number of times killing the last player standing."""
    rounds_survived: int
    """Number of rounds survived."""
    times_revived_by_ally: int
    """Number of times revived by a teammate."""
    lives_remaining: int | None
    """Number of lives remaining."""
    elimination_order: int
    """The order eliminated."""


class ExtractionStats(PascalCaseModel):
    """Performance statistics for extraction game modes."""

    extraction_conversions_completed: int
    """Number of times converting an extraction zone."""
    extraction_conversions_denied: int
    """Number of times denying an enemy extraction zone conversion."""
    extraction_initiations_completed: int
    """Number of times initiating an extraction zone."""
    extraction_initiations_denied: int
    """Number of times denying an enemy extraction zone initiation."""
    successful_extractions: int
    """Number of times extracting a zone."""


class InfectionStats(PascalCaseModel):
    """Performance statistics for infection game modes."""

    # TODO: Add infection stats
    pass


class OddballStats(PascalCaseModel):
    """Performance statistics for oddball game modes."""

    kills_as_skull_carrier: int
    """Number of kills while carrying the skull."""
    longest_time_as_skull_carrier: dt.timedelta
    """Longest time spent carrying the skull."""
    skull_carriers_killed: int
    """Number of times an enemy skull carrier was killed."""
    skull_grabs: int
    """Number of times the skull was grabbed."""
    time_as_skull_carrier: dt.timedelta
    """Total time spent carrying the skull."""
    skull_scoring_ticks: int
    """Number of ticks the skull was held."""


class ZonesStats(PascalCaseModel):
    """Performance statistics for zones game modes."""

    stronghold_captures: int
    """Number of times capturing a stronghold."""
    stronghold_defensive_kills: int
    """Number of kills defending a stronghold."""
    stronghold_offensive_kills: int
    """Number of kills attacking a stronghold."""
    stronghold_secures: int
    """Number of times securing a stronghold."""
    stronghold_occupation_time: dt.timedelta
    """Total time spent in a stronghold."""
    stronghold_scoring_ticks: int
    """Number of ticks a stronghold was held."""


class StockpileStats(PascalCaseModel):
    """Performance statistics for stockpile game modes."""

    kills_as_power_seed_carrier: int
    """Number of kills while carrying a power seed."""
    power_seeds_deposited: int
    """Number of power seeds deposited."""
    power_seeds_stolen: int
    """Number of power seeds stolen."""
    power_seed_carriers_killed: int
    """Number of times an enemy power seed carrier was killed."""
    time_as_power_seed_carrier: dt.timedelta
    """Total time spent carrying a power seed."""
    time_as_power_seed_driver: dt.timedelta
    """Total time spent driving a power seed."""


class Stats(PascalCaseModel):
    """Performance statistics for a player or team in a match."""

    core_stats: CoreStats
    """Performance statistics common to all game modes."""
    bomb_stats: BombStats | None = None
    """Performance statistics for bomb game modes."""
    capture_the_flag_stats: CaptureTheFlagStats | None = None
    """Performance statistics for capture the flag game modes."""
    elimination_stats: EliminationStats | None = None
    """Performance statistics for elimination game modes."""
    extraction_stats: ExtractionStats | None = None
    """Performance statistics for extraction game modes."""
    infection_stats: InfectionStats | None = None
    """Performance statistics for infection game modes."""
    oddball_stats: OddballStats | None = None
    """Performance statistics for oddball game modes."""
    zones_stats: ZonesStats | None = None
    """Performance statistics for zones game modes."""
    stockpile_stats: StockpileStats | None = None
    """Performance statistics for stockpile game modes."""


class TeamStats(PascalCaseModel):
    """Statistics for a team in a match."""

    team_id: int
    """The team's ID."""
    outcome: Outcome
    """The team's outcome in the match."""
    rank: int
    """The team's rank in the match."""
    stats: Stats
    """The team's performance statistics."""


class BotAttributes(PascalCaseModel):
    """Attributes of a bot player."""

    difficulty: BotDifficulty
    """The bot's difficulty."""


class ParticipationInfo(PascalCaseModel):
    """Information about a player's participation in a match."""

    first_joined_time: dt.datetime
    """The UTC datetime when the player first joined the match."""
    last_leave_time: dt.datetime | None
    """The UTC datetime when the player last left the match, if the player left the match."""
    present_at_beginning: bool
    """Whether the player was present at the beginning of the match."""
    joined_in_progress: bool
    """Whether the player joined the match in progress."""
    left_in_progress: bool
    """Whether the player left the match in progress."""
    present_at_completion: bool
    """Whether the player was present at the completion of the match."""
    time_played: dt.timedelta
    """The amount of time the player was present in the match."""
    confirmed_participation: bool | None
    """Whether the player's participation was confirmed."""


class PlayerTeamStats(PascalCaseModel):
    """Statistics for a player on a team in a match."""

    team_id: int
    """The team's ID."""
    stats: Stats
    """The player's performance statistics for the team."""


class PlayerStats(PascalCaseModel):
    """Statistics for a player in a match."""

    player_id: str
    """The player's Xbox Live ID."""
    player_type: PlayerType
    """The player's type, such as "human" or "bot"."""
    bot_attributes: BotAttributes | None
    """Details about bot players, if applicable."""
    last_team_id: int
    """The ID of the last team the player was on."""
    outcome: Outcome
    """The player's outcome in the match."""
    rank: int
    """The player's rank in the match."""
    participation_info: ParticipationInfo
    """Information about the player's participation in the match."""
    player_team_stats: list[PlayerTeamStats]
    """The player's performance statistics for each team they were on during the match."""


class MatchStats(PascalCaseModel):
    """Statistics for a match."""

    match_id: UUID
    """The match's GUID."""
    match_info: MatchInfo
    """Information about the match."""
    teams: list[TeamStats]
    """Performance statistics for all teams in the match."""
    players: list[PlayerStats]
    """Performance statistics for all players in the match."""
