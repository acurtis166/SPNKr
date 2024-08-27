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
    return list(highlight_events.read(data))


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
