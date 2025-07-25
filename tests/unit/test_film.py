import collections
import json
from pathlib import Path

import pytest

from spnkr.errors import FilmReadError
from spnkr.film import highlight_events
from spnkr.models.stats import MatchStats

FILM_DIR = Path(__file__).parents[1] / "data/film"
HIGHLIGHT_EVENTS_FILE = FILM_DIR / "highlight_events.gzip"
STATS_FILE = FILM_DIR / "match_stats.json"


@pytest.fixture
def events():
    data = HIGHLIGHT_EVENTS_FILE.read_bytes()
    return list(highlight_events.read(data, 37))


@pytest.fixture
def stats():
    data = STATS_FILE.read_bytes()
    return MatchStats(**json.loads(data))


def test_read_highlight_events(events: list[highlight_events.HighlightEvent]):
    """Test that events are parsed correctly."""
    expected = [
        ("mode", 24, None),
        ("kill", 29, None),
        ("death", 51, None),
        ("kill", 70, None),
        ("medal", 70, "Nade Shot"),
        ("mode", 70, None),
    ]
    result = [(e.event_type, round(e.time_ms / 1000), e.medal_name) for e in events]
    assert len(result) == 6
    for event in expected:
        assert event in result


@pytest.mark.parametrize(
    "file_name,xuid,gamertag,time_ms,kills,deaths,modes,medals",
    [
        # fmt: off
        ("30_f3aea1fc-2382-4281-abfd-ddc864f83991.gzip", 2533274796688502, "ColeMiner4", 29375, 60, 60, 104, 21),
        ("31_2b29d32d-b2f5-4b0b-9b3e-11e68680ed6a.gzip", 2533274912097531, "TheSon0fFlynn", 50017, 160, 165, 123, 80),
        ("33_61190383-64a0-456e-9862-5798c36c6e61.gzip", 2535469531821339, "TwiningIsland83", 34133, 84, 84, 0, 81),
        ("34_7fe02b07-86af-4004-a577-a6a5725f843a.gzip", 2535412760927018, "SalmonSummer83", 36205, 148, 150, 0, 52),
        ("35_820426aa-a601-455e-8e21-772874e7b6d1.gzip", 2535430960480250, "Just cm J", 43004, 134, 134, 52, 53),
        ("36_d8094e6d-c000-4dc6-9e2e-27ee1cbcc81a.gzip", 2535445291321133, "aCurtis X89", 40241, 105, 105, 77, 48),
        ("37_adfde763-6996-4ffb-8cd5-55855454c5f0.gzip", 2535415224281334, "YoungStudSZN", 40000, 96, 96, 0, 38),
        ("38_63391382-6b88-43f9-9ff4-6313404c419c.gzip", 2535445291321133, "aCurtis X89", 47053, 203, 203, 149, 85),
        ("39_73607aca-3a23-4733-9e84-b7c2ea679ce2.gzip", 2712212454167317, "I1 DUCE", 45858, 130, 130, 98, 59),
        ("40_fbf6b19e-2b1d-419e-8d64-756f33fda990.gzip", 2535445291321133, "aCurtis X89", 57801, 96, 96, 0, 34),
        # fmt: on
    ],
    ids=[30, 31, 33, 34, 35, 36, 37, 38, 39, 40],
)
def test_read_film_major_versions(
    file_name: str, xuid, gamertag, time_ms, kills, deaths, modes, medals
):
    path = FILM_DIR / file_name
    version = int(file_name[:2])
    events = list(highlight_events.read(path.read_bytes(), version))
    counts = collections.Counter([e.event_type for e in events])
    event = events[0]
    assert event.xuid == xuid
    assert event.gamertag == gamertag
    assert event.time_ms == time_ms
    assert counts["kill"] == kills
    assert counts["death"] == deaths
    assert counts["mode"] == modes
    assert counts["medal"] == medals


def test_infer_event_type_error():
    with pytest.raises(FilmReadError):
        highlight_events._infer_event_type(0, False)


def test_check_highlight_events_pass(
    events: list[highlight_events.HighlightEvent], stats: MatchStats
):
    """Test that the check passes for matched event counts."""
    errors = highlight_events.check(events, stats)
    assert not errors


def test_check_highlight_events_fail(
    events: list[highlight_events.HighlightEvent], stats: MatchStats
):
    """Test that the check fails for mismatched event counts."""
    events.pop(2)
    errors = highlight_events.check(events, stats)
    assert len(errors) == 1
