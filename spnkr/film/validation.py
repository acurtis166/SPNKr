"""Validate highlight events against match stats."""

import collections

from spnkr.film.models import EventCounts, EventType, HighlightEvent
from spnkr.models.stats import MatchStats, PlayerStats
from spnkr.xuid import unwrap_xuid


def check(events: list[HighlightEvent], match_stats: MatchStats) -> list[str]:
    """Check that parsed highlight events line up with match stats from the API.

    For each player, check that the number of kills, deaths, and medals parsed
    into events match retrieved match stats from the API. Note that this check excludes
    "mode" event counts.

    It is expected that this check will fail for "minigame" or "firefight" game modes
    where players fight AI opponents. Killing these enemies do not trigger kill events,
    but they are accounted for in match stats. Errors include the game variant category
    in the message, which can justify why there are no kill events for a firefight match.

    There are occasionally kills and/or deaths accounted for in match stats that are
    not found in the highlight events chunk data, but these misses seem to be rare and
    are typically only one kill or death.

    Args:
        events: Parsed highlight events.
        match_stats: The match stats data from the Halo Infinite API.

    Returns:
        Errors, if any, caught while comparing `events` and `match_stats`.
    """
    out = []
    events_by_xuid = _group_events_by_xuid(events)
    for player in match_stats.players:
        if not player.is_human:
            continue
        expected = _get_player_stat_event_type_counts(player)
        player_events = events_by_xuid.get(unwrap_xuid(player.player_id), [])
        result = _get_highlight_event_type_counts(player_events)
        if result != expected:
            out.append(
                f"Expected {expected} for player {player.player_id}. Got {result}. "
                f"({match_stats.match_info.game_variant_category.name})"
            )
    return out


def _group_events_by_xuid(
    events: list[HighlightEvent],
) -> dict[int, list[HighlightEvent]]:
    """Group highlight `events` by their XUID."""
    out = collections.defaultdict(list)
    for event in events:
        out[event.xuid].append(event)
    return out


def _get_player_stat_event_type_counts(player: PlayerStats) -> EventCounts:
    """Get expected event counts from player stats."""
    kills = deaths = medals = 0
    for player_team in player.player_team_stats:
        core = player_team.stats.core_stats
        kills += core.kills
        deaths += core.deaths
        medals += sum(m.count for m in core.medals)
    return EventCounts(kills, deaths, medals)


def _get_highlight_event_type_counts(events: list[HighlightEvent]) -> EventCounts:
    """Get event type counts for a list of `events`."""
    counter = collections.Counter(e.event_type for e in events)
    return EventCounts(
        kills=counter[EventType.KILL],
        deaths=counter[EventType.DEATH],
        medals=counter[EventType.MEDAL],
    )
