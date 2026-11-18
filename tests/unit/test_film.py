import collections
import json
import zlib
from pathlib import Path

import pytest
from pydantic import ValidationError

from spnkr.errors import FilmReadError
from spnkr.film import EventType, HighlightEvent, Medal, highlight_events, validation
from spnkr.models.stats import MatchStats

FILM_DIR = Path(__file__).parents[1] / "data/film"
LOCAL_FILM_DIR = FILM_DIR / "local"
STATS_FILE = FILM_DIR / "match_stats.json"
SYNTHETIC_XUID = 2000000000000026


def make_highlight_events(version: int) -> bytes:
    gamertag = "TestPlayer".encode("utf-16le").ljust(32, b"\x00")
    prefix = b"\x00" * 12 if 38 < version < 41 else b""
    suffix = b"\x00" * (3 if 38 < version < 41 else 15)
    events = [
        (10, 23626, 0, 0),
        (50, 29198, 0, 0),
        (20, 50970, 0, 0),
        (50, 69873, 0, 0),
        (50, 69873, 1, Medal.NADE_SHOT),
        (10, 69875, 0, 0),
    ]
    data = b""
    for hint, time_ms, is_medal, medal in events:
        data += (
            SYNTHETIC_XUID.to_bytes(8, "little")
            + b"\x2d\xc0"
            + prefix
            + gamertag
            + suffix
            + bytes([hint])
            + time_ms.to_bytes(4, "big")
            + b"\x00" * 3
            + bytes([is_medal])
            + b"\x00" * 3
            + bytes([medal])
            + b"\x00\x00\x2e\xe0"
        )
    return data


@pytest.fixture
def events():
    return list(highlight_events.read(zlib.compress(make_highlight_events(37)), 37))


@pytest.fixture
def stats():
    data = STATS_FILE.read_bytes()
    return MatchStats(**json.loads(data))


def test_read_highlight_events(events: list[HighlightEvent]):
    """Test that events are parsed correctly."""
    expected = [
        ("mode", 24, None),
        ("kill", 29, None),
        ("death", 51, None),
        ("kill", 70, None),
        ("medal", 70, Medal.NADE_SHOT),
        ("mode", 70, None),
    ]
    result = [(e.event_type, round(e.time_ms / 1000), e.medal) for e in events]
    assert len(result) == 6
    for event in expected:
        assert event in result


def test_read_uncompressed_highlight_events(events: list[HighlightEvent]):
    data = make_highlight_events(37)
    assert list(highlight_events.read(data, 37)) == events


@pytest.mark.parametrize("version", [30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41])
def test_read_synthetic_highlight_events_for_versions(version):
    events = list(highlight_events.read(make_highlight_events(version), version))
    assert len(events) == 6
    assert all(event.xuid == SYNTHETIC_XUID for event in events)
    assert all(event.gamertag == "TestPlayer" for event in events)
    assert [event.event_type for event in events] == [
        EventType.MODE,
        EventType.KILL,
        EventType.DEATH,
        EventType.KILL,
        EventType.MEDAL,
        EventType.MODE,
    ]
    assert events[4].medal == Medal.NADE_SHOT


@pytest.mark.parametrize(
    "event_type,medal",
    [
        (EventType.MEDAL, Medal.DOUBLE_KILL),
        (EventType.KILL, None),
        (EventType.DEATH, None),
        (EventType.MODE, None),
    ],
)
def test_highlight_event_accepts_consistent_medal(event_type, medal):
    event = HighlightEvent(
        xuid=1, gamertag="player", event_type=event_type, time_ms=0, medal=medal
    )
    assert event.medal is medal


@pytest.mark.parametrize(
    "event_type,medal,message",
    [
        (EventType.MEDAL, None, "medal is required for medal events"),
        (EventType.KILL, Medal.DOUBLE_KILL, "medal must be None for non-medal events"),
        (EventType.DEATH, Medal.NADE_SHOT, "medal must be None for non-medal events"),
        (EventType.MODE, Medal.NADE_SHOT, "medal must be None for non-medal events"),
    ],
)
def test_highlight_event_rejects_inconsistent_medal(event_type, medal, message):
    with pytest.raises(ValidationError, match=message):
        HighlightEvent(
            xuid=1, gamertag="player", event_type=event_type, time_ms=0, medal=medal
        )


@pytest.mark.parametrize(
    "version,time_ms,kills,deaths,modes,medals",
    [
        (30, 29375, 60, 60, 104, 21),
        (31, 50017, 160, 165, 123, 80),
        (33, 34133, 84, 84, 0, 81),
        (34, 36205, 148, 150, 0, 52),
        (35, 43004, 134, 134, 52, 53),
        (36, 40241, 105, 105, 77, 48),
        (37, 40000, 96, 96, 0, 38),
        (38, 47053, 203, 203, 149, 85),
        (39, 45858, 130, 130, 98, 59),
        (40, 57801, 96, 96, 0, 34),
        (41, 37907, 116, 116, 86, 47),
    ],
    ids=[30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41],
)  # fmt: skip
def test_read_film_major_versions(version: int, time_ms, kills, deaths, modes, medals):
    path = LOCAL_FILM_DIR / f"v{version}"
    if not path.is_file():
        pytest.skip(f"Optional captured film for version {version} is not available")  # type: ignore
    events = list(highlight_events.read(path.read_bytes(), version))
    counts = collections.Counter([e.event_type for e in events])
    event = events[0]
    assert event.time_ms == time_ms
    assert counts[EventType.KILL] == kills
    assert counts[EventType.DEATH] == deaths
    assert counts[EventType.MODE] == modes
    assert counts[EventType.MEDAL] == medals


def test_infer_event_type_error():
    with pytest.raises(FilmReadError):
        highlight_events._infer_event_type(0, False)


def test_check_highlight_events_pass(events: list[HighlightEvent], stats: MatchStats):
    """Test that the check passes for matched event counts."""
    errors = validation.check(events, stats)
    assert not errors


def test_check_highlight_events_fail(events: list[HighlightEvent], stats: MatchStats):
    """Test that the check fails for mismatched event counts."""
    events.pop(2)
    errors = validation.check(events, stats)
    assert len(errors) == 1
