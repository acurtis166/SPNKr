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
    """A player's match count summary.

    Attributes:
        custom_matches_played_count: The number of custom matches the player has played.
        matches_played_count: The number of matches the player has played.
        matchmade_matches_played_count: The number of matchmade matches the player has played.
        local_matches_played_count: The number of local matches the player has played.
    """

    custom_matches_played_count: int
    matches_played_count: int
    matchmade_matches_played_count: int
    local_matches_played_count: int


class Asset(PascalCaseModel):
    """ID information about a game asset, such as a map or game mode.

    Attributes:
        asset_kind: The kind of asset, such as "map variant" or "playlist".
        asset_id: The asset's GUID.
        version_id: The asset version's GUID.
    """

    asset_kind: AssetKind
    asset_id: UUID
    version_id: UUID


class MatchInfo(PascalCaseModel):
    """Information about a match.

    Attributes:
        start_time: The UTC datetime when the match started.
        end_time: The UTC datetime when the match ended.
        duration: The match's duration.
        lifecycle_mode: The match's lifecycle mode.
        game_variant_category: The game mode category.
        level_id: The ID of the level the match was played on.
        map_variant: The map the match was played on.
        ugc_game_variant: The game mode the match was played with.
        clearance_id: Clearance ID.
        playlist: The playlist the match was made in, if the match was matchmade.
        playlist_experience: The general category of playlist the match was made in, if the match was matchmade.
        playlist_map_mode_pair: The map and game mode the match was made in, if the match was matchmade.
        season_id: The ID of the season the match was played in, if the match was matchmade.
        playable_duration: The match's playable duration.
        teams_enabled: Whether teams were enabled in the match.
        team_scoring_enabled: Whether team scoring was enabled in the match.
    """

    start_time: dt.datetime
    end_time: dt.datetime
    duration: dt.timedelta
    lifecycle_mode: LifecycleMode
    game_variant_category: GameVariantCategory
    level_id: UUID
    map_variant: Asset
    ugc_game_variant: Asset
    clearance_id: UUID
    playlist: Asset | None
    playlist_experience: PlaylistExperience | None
    playlist_map_mode_pair: Asset | None
    season_id: str | None
    playable_duration: dt.timedelta
    teams_enabled: bool
    team_scoring_enabled: bool


class MatchHistoryResult(PascalCaseModel):
    """A match history entry.

    Attributes:
        match_id: The match's GUID.
        match_info: Information about the match.
        last_team_id: The ID of the last team the player was on.
        outcome: The player's outcome in the match.
        rank: The player's rank in the match.
        present_at_end_of_match: Whether the player was present at the end of the match.
    """

    match_id: UUID
    match_info: MatchInfo
    last_team_id: int
    outcome: Outcome
    rank: int
    present_at_end_of_match: bool


class MatchHistory(PascalCaseModel):
    """A page of a player's match history.

    Attributes:
        start: The index of the first match in the page. 0 is the most recent match.
        count: The number of matches requested.
        result_count: The actual number of matches in the page.
        results: The matches in the page.
    """

    start: int
    count: int
    result_count: int
    results: list[MatchHistoryResult]


class AwardCount(PascalCaseModel):
    """A count of a medal or personal score award.

    Attributes:
        name_id: The ID of the medal or personal score award.
        count: The number of times the medal or personal score award was earned.
        total_personal_score_awarded: The total personal score awarded by obtaining the medal or personal score award.
    """

    name_id: int
    count: int
    total_personal_score_awarded: int


class CoreStats(PascalCaseModel):
    """Core statistics about a player or team performance in a match.

    Attributes:
        score: Earned points related to the match outcome.
        personal_score: Earned points related to personal performance.
        rounds_won: The number of rounds won.
        rounds_lost: The number of rounds lost.
        rounds_tied: The number of rounds tied.
        kills: The number of kills.
        deaths: The number of deaths.
        assists: The number of assists.
        kda: Kill-death-assist metric (kills + assists / 3 - deaths).
        suicides: The number of suicides.
        betrayals: The number of betrayals.
        average_life_duration: The average time between deaths.
        grenade_kills: The number of kills using grenades.
        headshot_kills: The number of kills with headshots.
        melee_kills: The number of kills with melee or a melee weapon.
        power_weapon_kills: The number of kills with "power" weapons.
        shots_fired: The number of shots fired with weapons.
        shots_hit: The number of shots hit with weapons.
        accuracy: The accuracy of shots fired (shots_fired / shots_hit * 100).
        damage_dealt: The amount of damage dealt.
        damage_taken: The amount of damage taken.
        callout_assists: The number of assists earned by "marking" an enemy.
        vehicle_destroys: The number of vehicles destroyed.
        driver_assists: The number of assists earned by driving a teammate that gets a kill.
        hijacks: The number of times hijacking a vehicle.
        emp_assists: The number of assists earned by EMPing an enemy player or vehicle.
        max_killing_spree: The maximum number of kills without dying.
        medals: Medals earned.
        personal_scores: Personal score awards earned.
        deprecated_damage_dealt: Deprecated. Use damage_dealt instead.
        deprecated_damage_taken: Deprecated. Use damage_taken instead.
        spawns: The number of times spawned.
    """

    score: int
    personal_score: int
    rounds_won: int
    rounds_lost: int
    rounds_tied: int
    kills: int
    deaths: int
    assists: int
    kda: float = Field(alias="KDA")
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
    """Performance statistics for bomb game modes.

    Attributes:
        bomb_carriers_killed: Number of times an enemy bomb carrier was killed.
        bomb_defusals: Number of times a bomb was defused.
        bomb_defusers_killed: Number of times an enemy bomb defuser was killed.
        bomb_detonations: Number of times a bomb was detonated.
        bomb_pick_ups: Number of times a bomb was picked up.
        bomb_plants: Number of times a bomb was planted.
        bomb_returns: Number of times a bomb was returned.
        kills_as_bomb_carrier: Number of kills while carrying the bomb.
        time_as_bomb_carrier: Total time spent carrying the bomb.
    """

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
    """Performance statistics for capture the flag game modes.

    Attributes:
        flag_capture_assists: Number of times contributing to a flag capture.
        flag_captures: Number of times the enemy flag was captured.
        flag_carriers_killed: Number of times an enemy flag carrier was killed.
        flag_grabs: Number of times the enemy flag was grabbed.
        flag_returners_killed: Number of times an enemy flag returner was killed.
        flag_returns: Number of times the team flag was returned.
        flag_secures: Number of times the team flag was secured.
        flag_steals: Number of times stealing a flag.
        kills_as_flag_carrier: Number of kills while carrying the flag.
        kills_as_flag_returner: Number of kills while returning the flag.
        time_as_flag_carrier: Total time spent carrying the flag.
    """

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
    """Performance statistics for elimination game modes.

    Attributes:
        allies_revived: Number of times reviving a teammate.
        elimination_assists: Number of times contributing to an elimination.
        eliminations: Number of times eliminating an enemy.
        enemy_revives_denied: Number of times denying an enemy revive.
        executions: Number of times executing an enemy.
        kills_as_last_player_standing: Number of kills as the last player standing.
        last_players_standing_killed: Number of times killing the last player standing.
        rounds_survived: Number of rounds survived.
        times_revived_by_ally: Number of times revived by a teammate.
        lives_remaining: Number of lives remaining.
        elimination_order: The order eliminated.
    """

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
    """Performance statistics for extraction game modes.

    Attributes:
        extraction_conversions_completed: Number of times converting an extraction zone.
        extraction_conversions_denied: Number of times denying an enemy extraction zone conversion.
        extraction_initiations_completed: Number of times initiating an extraction zone.
        extraction_initiations_denied: Number of times denying an enemy extraction zone initiation.
        successful_extractions: Number of times extracting a zone.
    """

    extraction_conversions_completed: int
    extraction_conversions_denied: int
    extraction_initiations_completed: int
    extraction_initiations_denied: int
    successful_extractions: int


class InfectionStats(PascalCaseModel):
    """Performance statistics for infection game modes.

    Attributes:
        alphas_killed: Number of times infecting an alpha zombie.
        spartans_infected: Number of times infecting a spartan.
        spartans_infected_as_alpha: Number of times infecting a spartan as an alpha zombie.
        kills_as_last_spartan_standing: Number of kills as the last spartan standing.
        last_spartans_standing_infected: Number of times infecting the last spartan standing.
        rounds_as_alpha: Number of rounds as an alpha zombie.
        rounds_as_last_spartan_standing: Number of rounds as the last spartan standing.
        rounds_finished_as_infected: Number of rounds finished as an infected.
        rounds_survived_as_spartan: Number of rounds survived as a spartan.
        rounds_survived_as_last_spartan_standing: Number of rounds survived as the last spartan standing.
        time_as_last_spartan_standing: Total time spent as the last spartan standing.
        infected_killed: Number of times killing an infected.
    """

    alphas_killed: int
    spartans_infected: int
    spartans_infected_as_alpha: int
    kills_as_last_spartan_standing: int
    last_spartans_standing_infected: int
    rounds_as_alpha: int
    rounds_as_last_spartan_standing: int
    rounds_finished_as_infected: int
    rounds_survived_as_spartan: int
    rounds_survived_as_last_spartan_standing: int
    time_as_last_spartan_standing: dt.timedelta
    infected_killed: int


class OddballStats(PascalCaseModel):
    """Performance statistics for oddball game modes.

    Attributes:
        kills_as_skull_carrier: Number of kills while carrying the skull.
        longest_time_as_skull_carrier: Longest time spent carrying the skull.
        skull_carriers_killed: Number of times an enemy skull carrier was killed.
        skull_grabs: Number of times the skull was grabbed.
        time_as_skull_carrier: Total time spent carrying the skull.
        skull_scoring_ticks: Number of ticks the skull was held.
    """

    kills_as_skull_carrier: int
    longest_time_as_skull_carrier: dt.timedelta
    skull_carriers_killed: int
    skull_grabs: int
    time_as_skull_carrier: dt.timedelta
    skull_scoring_ticks: int


class ZonesStats(PascalCaseModel):
    """Performance statistics for zones game modes.

    Attributes:
        stronghold_captures: Number of times capturing a stronghold.
        stronghold_defensive_kills: Number of kills defending a stronghold.
        stronghold_offensive_kills: Number of kills attacking a stronghold.
        stronghold_secures: Number of times securing a stronghold.
        stronghold_occupation_time: Total time spent in a stronghold.
        stronghold_scoring_ticks: Number of ticks a stronghold was held.
    """

    stronghold_captures: int
    stronghold_defensive_kills: int
    stronghold_offensive_kills: int
    stronghold_secures: int
    stronghold_occupation_time: dt.timedelta
    stronghold_scoring_ticks: int


class StockpileStats(PascalCaseModel):
    """Performance statistics for stockpile game modes.

    Attributes:
        kills_as_power_seed_carrier: Number of kills while carrying a power seed.
        power_seeds_deposited: Number of power seeds deposited.
        power_seeds_stolen: Number of power seeds stolen.
        power_seed_carriers_killed: Number of times an enemy power seed carrier was killed.
        time_as_power_seed_carrier: Total time spent carrying a power seed.
        time_as_power_seed_driver: Total time spent driving a power seed.
    """

    kills_as_power_seed_carrier: int
    power_seeds_deposited: int
    power_seeds_stolen: int
    power_seed_carriers_killed: int
    time_as_power_seed_carrier: dt.timedelta
    time_as_power_seed_driver: dt.timedelta


class Stats(PascalCaseModel):
    """Performance statistics for a player or team in a match.

    Attributes:
        core_stats: Performance statistics common to all game modes.
        bomb_stats: Performance statistics for bomb game modes.
        capture_the_flag_stats: Performance statistics for capture the flag game modes.
        elimination_stats: Performance statistics for elimination game modes.
        extraction_stats: Performance statistics for extraction game modes.
        infection_stats: Performance statistics for infection game modes.
        oddball_stats: Performance statistics for oddball game modes.
        zones_stats: Performance statistics for zones game modes.
        stockpile_stats: Performance statistics for stockpile game modes.
    """

    core_stats: CoreStats
    bomb_stats: BombStats | None = None
    capture_the_flag_stats: CaptureTheFlagStats | None = None
    elimination_stats: EliminationStats | None = None
    extraction_stats: ExtractionStats | None = None
    infection_stats: InfectionStats | None = None
    oddball_stats: OddballStats | None = None
    zones_stats: ZonesStats | None = None
    stockpile_stats: StockpileStats | None = None


class TeamStats(PascalCaseModel):
    """Statistics for a team in a match.

    Attributes:
        team_id: The team's ID.
        outcome: The team's outcome in the match.
        rank: The team's rank in the match.
        stats: The team's performance statistics.
    """

    team_id: int
    outcome: Outcome
    rank: int
    stats: Stats


class BotAttributes(PascalCaseModel):
    """Attributes of a bot player.

    Attributes:
        difficulty: The bot's difficulty.
    """

    difficulty: BotDifficulty


class ParticipationInfo(PascalCaseModel):
    """Information about a player's participation in a match.

    Attributes:
        first_joined_time: The UTC datetime when the player first joined the match.
        last_leave_time: The UTC datetime when the player last left the match, if the player left the match.
        present_at_beginning: Whether the player was present at the beginning of the match.
        joined_in_progress: Whether the player joined the match in progress.
        left_in_progress: Whether the player left the match in progress.
        present_at_completion: Whether the player was present at the completion of the match.
        time_played: The amount of time the player was present in the match.
        confirmed_participation: Whether the player's participation was confirmed.
    """

    first_joined_time: dt.datetime
    last_leave_time: dt.datetime | None
    present_at_beginning: bool
    joined_in_progress: bool
    left_in_progress: bool
    present_at_completion: bool
    time_played: dt.timedelta
    confirmed_participation: bool | None


class PlayerTeamStats(PascalCaseModel):
    """Statistics for a player on a team in a match.

    Attributes:
        team_id: The team's ID.
        stats: The player's performance statistics while on the team.
    """

    team_id: int
    stats: Stats


class PlayerStats(PascalCaseModel):
    """Statistics for a player in a match.

    Attributes:
        player_id: The player's Xbox Live ID.
        player_type: The player's type, such as "human" or "bot".
        bot_attributes: Details about bot players, if applicable.
        last_team_id: The ID of the last team the player was on.
        outcome: The player's outcome in the match.
        rank: The player's rank in the match.
        participation_info: Information about the player's participation in the match.
        player_team_stats: The player's performance statistics for each team they were on during the match.
    """

    player_id: str
    player_type: PlayerType
    bot_attributes: BotAttributes | None
    last_team_id: int
    outcome: Outcome
    rank: int
    participation_info: ParticipationInfo
    player_team_stats: list[PlayerTeamStats]


class MatchStats(PascalCaseModel):
    """Player and team performance details for a match.

    Attributes:
        match_id: The match's GUID.
        match_info: Information about the match.
        teams: Performance statistics for all teams in the match.
        players: Performance statistics for all players in the match.
    """

    match_id: UUID
    match_info: MatchInfo
    teams: list[TeamStats]
    players: list[PlayerStats]
