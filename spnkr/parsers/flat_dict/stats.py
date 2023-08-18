import datetime as dt
from typing import Any

from ..refdata import (
    BotDifficulty,
    GameVariantCategory,
    LifecycleMode,
    Outcome,
    PlayerType,
    Team,
)


def parse_match_count(match_count: dict[str, Any]) -> dict[str, Any]:
    return {
        "total": match_count["MatchesPlayedCount"],
        "custom": match_count["CustomMatchesPlayedCount"],
        "matchmade": match_count["MatchmadeMatchesPlayedCount"],
        "local": match_count["LocalMatchesPlayedCount"],
    }


def parse_match_history(match_history: dict[str, Any]) -> list[dict[str, Any]]:
    return [_parse_match_history_result(r) for r in match_history["Results"]]


def parse_team_core_stats(match_stats: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for team in match_stats["Teams"]:
        entry = {
            "match_id": match_stats["MatchId"],
            "team_id": Team(team["TeamId"]),
            "outcome": Outcome(team["Outcome"]),
            "rank": team["Rank"],
        }
        entry.update(_parse_core_stats(team["Stats"]["CoreStats"]))
        out.append(entry)
    return out


def parse_match_info(match_stats: dict[str, Any]) -> dict[str, Any]:
    return {
        "match_id": match_stats["MatchId"],
        **_parse_match_info(match_stats["MatchInfo"]),
    }


def parse_player_core_stats(
    match_stats: dict[str, Any]
) -> list[dict[str, Any]]:
    out = []
    for player in match_stats["Players"]:
        participation = player["ParticipationInfo"]
        bot_attributes = player["BotAttributes"] or {}
        difficulty = BotDifficulty(bot_attributes.get("Difficulty"))
        for team in player["PlayerTeamStats"]:
            entry = {
                "match_id": match_stats["MatchId"],
                "player_id": player["PlayerId"],
                "player_type": PlayerType(player["PlayerType"]),
                "bot_difficulty": difficulty,
                "last_team_id": Team(player["LastTeamId"]),
                "outcome": Outcome(player["Outcome"]),
                "rank": player["Rank"],
                "present_at_beginning": participation["PresentAtBeginning"],
                "present_at_completion": participation["PresentAtCompletion"],
                "time_played": _parse_iso_duration(participation["TimePlayed"]),
                "team_id": Team(team["TeamId"]),
            }
            entry.update(_parse_core_stats(team["Stats"]["CoreStats"]))
            out.append(entry)
    return out


def parse_player_medals(match_stats: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for player in match_stats["Players"]:
        for team in player["PlayerTeamStats"]:
            for medal in team["Stats"]["MedalStats"]:
                out.append(
                    {
                        "match_id": match_stats["MatchId"],
                        "player_id": player["PlayerId"],
                        "team_id": Team(team["TeamId"]),
                        "name_id": medal["NameId"],
                        "count": medal["Count"],
                    }
                )
    return []


def _parse_match_history_result(result: dict[str, Any]) -> dict[str, Any]:
    info = result["MatchInfo"]
    return {
        "match_id": result["MatchId"],
        **_parse_match_info(info),
        "last_team_id": Team(result["LastTeamId"]),
        "outcome": Outcome(result["Outcome"]),
        "rank": result["Rank"],
        "present_at_end_of_match": result["PresentAtEndOfMatch"],
    }


def _parse_match_info(info: dict[str, Any]) -> dict[str, Any]:
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
        # TODO: Playlist can be null
        "playlist_asset_id": info["Playlist"]["AssetId"],
        "playlist_version_id": info["Playlist"]["VersionId"],
        # TODO: PlaylistMapModePair can be null
        "map_mode_pair_asset_id": info["PlaylistMapModePair"]["AssetId"],
        "map_mode_pair_version_id": info["PlaylistMapModePair"]["VersionId"],
        "season_id": info["SeasonId"],
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
    """Parse an ISO 8601 duration string to a timedelta object."""
    assert value.startswith("PT")
    kwargs = {}
    haystack = value[2:]  # Remove "PT" prefix
    attributes = ("weeks", "days", "hours", "minutes", "seconds")
    for attribute in attributes:
        separator = attribute[0].upper()  # "weeks" -> "W"
        parts = haystack.split(separator)
        if len(parts) > 1:
            kwargs[attribute] = float(parts[0])
            haystack = parts[1]
    return dt.timedelta(**kwargs)
