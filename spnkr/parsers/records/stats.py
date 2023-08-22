"""Parsing functions for the "stats" authority."""

import datetime as dt
from typing import Any, NamedTuple
from uuid import UUID

from ...xuid import wrap_xuid
from ..refdata import (
    BotDifficulty,
    GameVariantCategory,
    LifecycleMode,
    Outcome,
    PlayerType,
)


class MatchCountRecord(NamedTuple):
    """A player's match count summary."""

    player_id: str
    """The player's Xbox Live ID."""
    total: int
    """The total number of matches played."""
    custom: int
    """The number of custom matches played."""
    matchmade: int
    """The number of matchmade matches played."""
    local: int
    """The number of local matches played."""


class MatchHistoryRecord(NamedTuple):
    """A single match from a player's match history."""

    match_id: UUID
    """The match GUID."""
    start_time: dt.datetime
    """The UTC datetime the match started."""
    end_time: dt.datetime
    """The UTC datetime the match ended."""
    duration: dt.timedelta
    """The duration of the match."""
    lifecycle_mode: LifecycleMode
    """The lifecycle mode of the match."""
    game_variant_category: GameVariantCategory
    """The game variant category of the match."""
    level_id: str
    """The ID of the level the match was played on."""
    map_asset_id: str
    """The asset ID of the map variant."""
    map_version_id: int
    """The version ID of the map variant."""
    game_variant_asset_id: str
    """The asset ID of the game mode."""
    game_variant_version_id: int
    """The version ID of the game mode."""
    playlist_asset_id: str | None
    """The asset ID of the playlist."""
    playlist_version_id: int | None
    """The version ID of the playlist."""
    map_mode_pair_asset_id: str | None
    """The asset ID of the map mode pair."""
    map_mode_pair_version_id: int | None
    """The version ID of the map mode pair."""
    season_id: int | None
    """The ID of the season the match was played in."""
    playable_duration: dt.timedelta
    """The duration of the match that was playable."""
    last_team_id: int
    """The ID of the team the player was on at the end of the match."""
    outcome: Outcome
    """The outcome of the match for the player."""
    rank: int
    """The player's rank in the match."""
    present_at_end_of_match: bool
    """Whether the player was present at the end of the match."""


class MatchInfoRecord(NamedTuple):
    """Information about a single match."""

    match_id: UUID
    """The match GUID."""
    start_time: dt.datetime
    """The UTC datetime the match started."""
    end_time: dt.datetime
    """The UTC datetime the match ended."""
    duration: dt.timedelta
    """The duration of the match."""
    lifecycle_mode: LifecycleMode
    """The lifecycle mode of the match."""
    game_variant_category: GameVariantCategory
    """The game variant category of the match."""
    level_id: str
    """The ID of the level the match was played on."""
    map_asset_id: str
    """The asset ID of the map variant."""
    map_version_id: int
    """The version ID of the map variant."""
    game_variant_asset_id: str
    """The asset ID of the game mode."""
    game_variant_version_id: int
    """The version ID of the game mode."""
    playlist_asset_id: str | None
    """The asset ID of the playlist."""
    playlist_version_id: int | None
    """The version ID of the playlist."""
    map_mode_pair_asset_id: str | None
    """The asset ID of the map mode pair."""
    map_mode_pair_version_id: int | None
    """The version ID of the map mode pair."""
    season_id: int | None
    """The ID of the season the match was played in."""
    playable_duration: dt.timedelta
    """The duration of the match that was playable."""


class TeamCoreStatsRecord(NamedTuple):
    """A team's core stats for a single match."""

    match_id: UUID
    """The match GUID."""
    team_id: int
    """The team ID."""
    outcome: Outcome
    """The outcome of the match for the team."""
    rank: int
    """The team's rank in the match."""
    score: int
    """The team's score."""
    personal_score: int
    """The team's personal score."""
    rounds_won: int
    """The number of rounds the team won."""
    rounds_lost: int
    """The number of rounds the team lost."""
    rounds_tied: int
    """The number of rounds the team tied."""
    kills: int
    """The number of kills the team had."""
    deaths: int
    """The number of times the team died."""
    assists: int
    """The number of assists the team had."""
    kda: float
    """The team's kill-death-assist metric (kills + assists / 3 - deaths)."""
    suicides: int
    """The number of times the team's members committed suicide."""
    betrayals: int
    """The number of times the team's members killed each other."""
    average_life_duration: dt.timedelta
    """The average duration of the team's lives."""
    grenade_kills: int
    """The number of grenade kills the team had."""
    headshot_kills: int
    """The number of headshot kills the team had."""
    melee_kills: int
    """The number of melee kills the team had."""
    power_weapon_kills: int
    """The number of power weapon kills the team had."""
    shots_fired: int
    """The number of shots the team fired."""
    shots_hit: int
    """The number of shots the team hit."""
    accuracy: float
    """The team's accuracy (shots_hit / shots_fired * 100)."""
    damage_dealt: int
    """The amount of damage the team dealt."""
    damage_taken: int
    """The amount of damage the team took."""
    callout_assists: int
    """The number of marking assists the team had."""
    vehicle_destroys: int
    """The number of vehicles the team destroyed."""
    driver_assists: int
    """The number of driver assists the team had."""
    hijacks: int
    """The number of vehicles the team hijacked."""
    emp_assists: int
    """The number of EMP assists the team had."""
    max_killing_spree: int
    """The maximum killing spree across all team members."""
    spawns: int
    """The number of times the team spawned."""


class PlayerCoreStatsRecord(NamedTuple):
    """A player's core stats for a single match."""

    match_id: UUID
    """The match GUID."""
    player_id: str
    """The player's Xbox Live ID."""
    player_type: PlayerType
    """The player's type."""
    bot_difficulty: BotDifficulty | None
    """The bot's difficulty, if the player is a bot."""
    last_team_id: int
    """The ID of the team the player was on at the end of the match."""
    outcome: Outcome
    """The outcome of the match for the player."""
    rank: int
    """The player's rank in the match."""
    present_at_beginning: bool
    """Whether the player was present at the beginning of the match."""
    present_at_completion: bool
    """Whether the player was present at the completion of the match."""
    time_played: dt.timedelta
    """The amount of time the player was present in the match."""
    team_id: int
    """The ID of the team the player was on."""
    outcome: Outcome
    """The outcome of the match for the player."""
    rank: int
    """The player's rank in the match."""
    score: int
    """The player's score."""
    personal_score: int
    """The player's personal score."""
    rounds_won: int
    """The number of rounds the player's team won."""
    rounds_lost: int
    """The number of rounds the player's team lost."""
    rounds_tied: int
    """The number of rounds the player's team tied."""
    kills: int
    """The number of kills the player had."""
    deaths: int
    """The number of times the player died."""
    assists: int
    """The number of assists the player had."""
    kda: float
    """The player's kill-death-assist metric (kills + assists / 3 - deaths)."""
    suicides: int
    """The number of times the player committed suicide."""
    betrayals: int
    """The number of times the player betrayed a teammate."""
    average_life_duration: dt.timedelta
    """The average duration of the player's lives."""
    grenade_kills: int
    """The number of grenade kills the player had."""
    headshot_kills: int
    """The number of headshot kills the player had."""
    melee_kills: int
    """The number of melee kills the player had."""
    power_weapon_kills: int
    """The number of power weapon kills the player had."""
    shots_fired: int
    """The number of shots the player fired."""
    shots_hit: int
    """The number of shots the player hit."""
    accuracy: float
    """The player's accuracy (shots_hit / shots_fired * 100)."""
    damage_dealt: int
    """The amount of damage the player dealt."""
    damage_taken: int
    """The amount of damage the player took."""
    callout_assists: int
    """The number of callout assists the player had."""
    vehicle_destroys: int
    """The number of vehicles the player destroyed."""
    driver_assists: int
    """The number of driver assists the player had."""
    hijacks: int
    """The number of vehicles the player hijacked."""
    emp_assists: int
    """The number of EMP assists the player had."""
    max_killing_spree: int
    """The maximum killing spree the player had."""
    spawns: int
    """The number of times the player spawned."""


class PlayerMedalRecord(NamedTuple):
    """A single medal earned by a player in a match."""

    match_id: UUID
    """The match GUID."""
    player_id: str
    """The player's Xbox Live ID."""
    team_id: int
    """The team ID of the player."""
    name_id: int
    """The medal's ID."""
    count: int
    """The number of times the medal was earned."""


def parse_match_count(
    xuid: str | int, match_count: dict[str, Any]
) -> MatchCountRecord:
    """Parse a match count response into a match count record.

    Args:
        xuid: The player's Xbox Live ID.
        match_count: The deserialized JSON from the client's `get_match_count`
            method.

    Returns:
        A match count record.
    """
    return MatchCountRecord(
        player_id=wrap_xuid(xuid),
        total=match_count["MatchesPlayedCount"],
        custom=match_count["CustomMatchesPlayedCount"],
        matchmade=match_count["MatchmadeMatchesPlayedCount"],
        local=match_count["LocalMatchesPlayedCount"],
    )


def parse_match_history(
    match_history: dict[str, Any]
) -> list[MatchHistoryRecord]:
    """Parse a match history response into a list of match history records.

    Args:
        match_history: The deserialized JSON from the client's
            `get_match_history` method.

    Returns:
        A list of match history records.
    """
    return [_parse_match_history_result(r) for r in match_history["Results"]]


def parse_team_core_stats(
    match_stats: dict[str, Any]
) -> list[TeamCoreStatsRecord]:
    """Parse a match stats response into a list of team core stats records.

    Args:
        match_stats: The deserialized JSON from the client's `get_match_stats`
            method.

    Returns:
        A list of team core stats records.
    """
    out: list[TeamCoreStatsRecord] = []
    for team in match_stats["Teams"]:
        entry = TeamCoreStatsRecord(
            match_id=match_stats["MatchId"],
            team_id=team["TeamId"],
            outcome=Outcome(team["Outcome"]),
            rank=team["Rank"],
            **_parse_core_stats(team["Stats"]["CoreStats"]),
        )
        out.append(entry)
    return out


def parse_match_info(match_stats: dict[str, Any]) -> MatchInfoRecord:
    """Parse a match stats response into a match info record.

    Args:
        match_stats: The deserialized JSON from the client's `get_match_stats`
            method.

    Returns:
        A match info record.
    """
    return MatchInfoRecord(
        match_id=match_stats["MatchId"],
        **_parse_match_info(match_stats["MatchInfo"]),
    )


def parse_player_core_stats(
    match_stats: dict[str, Any]
) -> list[PlayerCoreStatsRecord]:
    """Parse a match stats response into a list of player core stats records.

    Args:
        match_stats: The deserialized JSON from the client's `get_match_stats`
            method.

    Returns:
        A list of player core stats records.
    """
    out: list[PlayerCoreStatsRecord] = []
    for player in match_stats["Players"]:
        participation = player["ParticipationInfo"]
        bot_attributes = player["BotAttributes"]
        difficulty = None
        if bot_attributes is not None:
            difficulty = BotDifficulty(bot_attributes["Difficulty"])
        for team in player["PlayerTeamStats"]:
            entry = PlayerCoreStatsRecord(
                match_id=match_stats["MatchId"],
                player_id=player["PlayerId"],
                player_type=PlayerType(player["PlayerType"]),
                bot_difficulty=difficulty,
                last_team_id=player["LastTeamId"],
                outcome=Outcome(player["Outcome"]),
                rank=player["Rank"],
                present_at_beginning=participation["PresentAtBeginning"],
                present_at_completion=participation["PresentAtCompletion"],
                time_played=_parse_iso_duration(participation["TimePlayed"]),
                team_id=team["TeamId"],
                **_parse_core_stats(team["Stats"]["CoreStats"]),
            )
            out.append(entry)
    return out


def parse_player_medals(match_stats: dict[str, Any]) -> list[PlayerMedalRecord]:
    """Parse a match stats response into a list of player medal records.

    Args:
        match_stats: The deserialized JSON from the client's `get_match_stats`
            method.

    Returns:
        A list of player medal records.
    """
    out: list[PlayerMedalRecord] = []
    for player in match_stats["Players"]:
        for team in player["PlayerTeamStats"]:
            for medal in team["Stats"]["CoreStats"]["Medals"]:
                entry = PlayerMedalRecord(
                    match_id=match_stats["MatchId"],
                    player_id=player["PlayerId"],
                    team_id=team["TeamId"],
                    name_id=medal["NameId"],
                    count=medal["Count"],
                )
                out.append(entry)
    return out


def _parse_match_history_result(result: dict[str, Any]) -> MatchHistoryRecord:
    info = result["MatchInfo"]
    return MatchHistoryRecord(
        match_id=result["MatchId"],
        **_parse_match_info(info),
        last_team_id=result["LastTeamId"],
        outcome=Outcome(result["Outcome"]),
        rank=result["Rank"],
        present_at_end_of_match=result["PresentAtEndOfMatch"],
    )


def _parse_match_info(info: dict[str, Any]) -> dict[str, Any]:
    playlist = info["Playlist"]
    playlist_asset_id = playlist_version_id = None
    if playlist is not None:
        playlist_asset_id = playlist["AssetId"]
        playlist_version_id = playlist["VersionId"]
    map_mode = info["PlaylistMapModePair"]
    map_mode_asset_id = map_mode_version_id = None
    if map_mode is not None:
        map_mode_asset_id = map_mode["AssetId"]
        map_mode_version_id = map_mode["VersionId"]
    return {
        "start_time": dt.datetime.fromisoformat(info["StartTime"]),
        "end_time": dt.datetime.fromisoformat(info["EndTime"]),
        "duration": _parse_iso_duration(info["Duration"]),
        "lifecycle_mode": LifecycleMode(info["LifecycleMode"]),
        "game_variant_category": GameVariantCategory(
            info["GameVariantCategory"]
        ),
        "level_id": info["LevelId"],
        "map_asset_id": info["MapVariant"]["AssetId"],
        "map_version_id": info["MapVariant"]["VersionId"],
        "game_variant_asset_id": info["UgcGameVariant"]["AssetId"],
        "game_variant_version_id": info["UgcGameVariant"]["VersionId"],
        "playlist_asset_id": playlist_asset_id,
        "playlist_version_id": playlist_version_id,
        "map_mode_pair_asset_id": map_mode_asset_id,
        "map_mode_pair_version_id": map_mode_version_id,
        "season_id": info.get("SeasonId"),
        "playable_duration": _parse_iso_duration(info["PlayableDuration"]),
    }


def _parse_core_stats(stats: dict[str, Any]) -> dict[str, Any]:
    return {
        "score": stats["Score"],
        "personal_score": stats["PersonalScore"],
        "rounds_won": stats["RoundsWon"],
        "rounds_lost": stats["RoundsLost"],
        "rounds_tied": stats["RoundsTied"],
        "kills": stats["Kills"],
        "deaths": stats["Deaths"],
        "assists": stats["Assists"],
        "kda": stats["KDA"],
        "suicides": stats["Suicides"],
        "betrayals": stats["Betrayals"],
        "average_life_duration": _parse_iso_duration(
            stats["AverageLifeDuration"]
        ),
        "grenade_kills": stats["GrenadeKills"],
        "headshot_kills": stats["HeadshotKills"],
        "melee_kills": stats["MeleeKills"],
        "power_weapon_kills": stats["PowerWeaponKills"],
        "shots_fired": stats["ShotsFired"],
        "shots_hit": stats["ShotsHit"],
        "accuracy": stats["Accuracy"],
        "damage_dealt": stats["DamageDealt"],
        "damage_taken": stats["DamageTaken"],
        "callout_assists": stats["CalloutAssists"],
        "vehicle_destroys": stats["VehicleDestroys"],
        "driver_assists": stats["DriverAssists"],
        "hijacks": stats["Hijacks"],
        "emp_assists": stats["EmpAssists"],
        "max_killing_spree": stats["MaxKillingSpree"],
        "spawns": stats["Spawns"],
    }


def _parse_iso_duration(value: str) -> dt.timedelta:
    """Parse an ISO 8601 duration string to a timedelta object.

    Example: PT12M34.1102934S => 12 minutes, 34.1102934 seconds

    Only hour, minute, and second components are supported.
    """
    if not value.startswith("PT"):
        raise ValueError(
            "Invalid ISO 8601 duration string. Only hours, minutes, and "
            "seconds are supported."
        )
    kwargs = {}
    haystack = value[2:]  # Remove "PT" prefix
    attributes = ("hours", "minutes", "seconds")
    for attribute in attributes:
        separator = attribute[0].upper()
        parts = haystack.split(separator)
        if len(parts) > 1:
            kwargs[attribute] = float(parts[0])
            haystack = parts[1]
    return dt.timedelta(**kwargs)
