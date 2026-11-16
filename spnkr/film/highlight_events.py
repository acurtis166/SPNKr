"""Read highlight event film chunks."""

import collections
import zlib
from typing import Any

from bitstring import Bits

from spnkr.errors import FilmReadError
from spnkr.film.models import EventCounts, EventType, HighlightEvent, Medal
from spnkr.models.stats import MatchStats, PlayerStats
from spnkr.xuid import unwrap_xuid

_MIN_XUID = int(2e15)
_MAX_XUID = int(3e15)
_XUID_BITS = 64
_MODE = 10
_DEATH = 20
_KILL = 50
_MEDAL_SORTING_WEIGHTS = {
    50,
    51,
    52,
    100,
    101,
    150,
    200,
    205,
    210,
    220,
    225,
    230,
    235,
    240,
    245,
    250,
}


def read(data: bytes, version: int):
    """Iterate events found in highlight event file content.

    Args:
        data: The gzip-compressed file data.
        version: The major version of the film, available from either the film metadata
            or the film header.

    Yields:
        Highlight events.
    """
    bits = Bits(bytes=zlib.decompress(data))
    for start, _ in _find_xuids(bits):
        yield _parse_event(bits, start, version)


def _find_xuids(bits: Bits):
    """Iterate XUID (start, value) tuples found in binary data."""
    # Example:
    # ------xuid------ --marker-
    # 2a5bf9c8f1010900 (2d|25)c0
    for marker_start in bits.findall(Bits(hex="c0")):
        xuid_end = marker_start - 8
        if bits[xuid_end:marker_start].hex not in ("2d", "25"):
            continue
        xuid_start = xuid_end - _XUID_BITS
        xuid_bits = bits[xuid_start:xuid_end]
        if len(xuid_bits) < _XUID_BITS:
            continue
        xuid = xuid_bits.uintle
        if _MIN_XUID < xuid < _MAX_XUID:
            yield (xuid_start, xuid)


def _infer_event_type(hint: int, is_medal: bool) -> EventType:
    """Infer the type of an event given information from a couple bytes."""
    if is_medal and hint in _MEDAL_SORTING_WEIGHTS:
        return EventType.MEDAL
    if hint == _MODE:
        return EventType.MODE
    if hint == _DEATH:
        return EventType.DEATH
    if hint == _KILL:
        return EventType.KILL
    raise FilmReadError(f"Unhandled event type args: {hint=}, {is_medal=}")


def _tokens(version: int) -> list[str]:
    """Determine unpacking strategy based on the film major version."""
    if version <= 38 or version >= 41:
        return [
            "bytes:32",  # 16-character utf-16 gamertag (32 bytes)
            "pad:120",  # Skip (15 bytes)
            "uint:8",  # Type hint (1 byte)
            "uint:32",  # Timestamp in milliseconds (4 bytes)
            "pad:24",  # Skip (3 bytes)
            "uint:8",  # 1 if event is medal, otherwise 0 (1 byte)
            "pad:24",  # Skip (3 bytes)
            "uint:8",  # Medal type (1 byte)
        ]
    return [
        "pad:96",  # Skip (12 bytes)
        "bytes:32",  # 16-character utf-16 gamertag (32 bytes)
        "pad:24",  # Skip (3 bytes)
        "uint:8",  # Type hint (1 byte)
        "uint:32",  # Timestamp in milliseconds (4 bytes)
        "pad:24",  # Skip (3 bytes)
        "uint:8",  # 1 if event is medal, otherwise 0 (1 byte)
        "pad:24",  # Skip (3 bytes)
        "uint:8",  # Medal type (1 byte)
    ]


def _parse_event(bits: Bits, start: int, version: int) -> HighlightEvent:
    """Parse an event from `bits` starting at `start`."""
    selected = bits[start : start + 20_000]  # 20,000 bits just to capture the event
    # Grab the relevent 60 bytes of event data and unpack the attributes
    end = selected.find(Bits(hex="00002ee0"))[0]  # type: ignore
    event_bits = selected[end - (60 * 8) : end]
    values: list[Any] = event_bits.unpack(fmt=", ".join(_tokens(version)))
    gamertag_bytes, type_hint, time_ms, is_medal, medal_value = values
    event_type = _infer_event_type(type_hint, is_medal == 1)
    try:
        medal = Medal(medal_value) if event_type is EventType.MEDAL else None
    except ValueError as e:
        raise FilmReadError(f"Invalid medal value: {medal_value}, {version=}") from e
    return HighlightEvent(
        xuid=selected[:_XUID_BITS].uintle,
        gamertag=gamertag_bytes.decode("utf-16le").strip("\x00"),
        event_type=event_type,
        time_ms=time_ms,
        medal=medal,
    )


def check(events: list[HighlightEvent], match_stats: MatchStats) -> list[str]:
    """Check that parsed highlight events line up with match stats from the API.

    For each player, check that the number of kills, deaths, and medals parsed
    into events match retrieved match stats from the API. Note that this check excludes
    "mode" event counts.

    It is expected that this check will fail for "minigame" or "firefight" game modes
    where players fight AI opponents. Killing these enemies do not trigger kill events,
    but they are accounted for in match stats. Errors include the game variant category
    in the message, which can justify why there are no kill events for a firefight match.

    There are occassionally kills and/or deaths accounted for in match stats that are
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
