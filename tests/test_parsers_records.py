"""Test record parsing of Halo Infinite API responses."""

import datetime as dt
import json
import uuid
from pathlib import Path
from typing import Any

import pytest

from spnkr.parsers import records
from spnkr.parsers.records.stats import _parse_iso_duration

RESPONSES = Path("tests/responses")
TEST_ISO8601_DURATIONS = [
    (dt.timedelta(seconds=0), "PT0S"),
    (dt.timedelta(seconds=1), "PT1S"),
    (dt.timedelta(seconds=60), "PT1M"),
    (dt.timedelta(seconds=3600), "PT1H"),
    (dt.timedelta(minutes=12, seconds=34.1102934), "PT12M34.1102934S"),
    (dt.timedelta(hours=1, seconds=1), "PT1H1S"),
]


def load_response(name: str) -> Any:
    with open(RESPONSES / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("delta, iso", TEST_ISO8601_DURATIONS)
def test_parse_iso_duration(delta: dt.timedelta, iso: str):
    result = _parse_iso_duration(iso)
    assert result == delta


def test_parse_iso_duration_unsupported_components():
    with pytest.raises(ValueError):
        _parse_iso_duration("P1DT1S")


def test_parse_medal_metadata():
    data = load_response("get_medal_metadata")
    result = records.parse_medal_metadata(data)
    assert result[0].name_id == 622331684


def test_parse_match_skill():
    data = load_response("get_match_skill")
    result = records.parse_match_skill(uuid.uuid4(), data)
    assert result[0].player_id == "xuid(2535445291321133)"


def test_parse_playlist_csr():
    data = load_response("get_playlist_csr")
    result = records.parse_playlist_csr(data)
    assert result[0].player_id == "xuid(2535445291321133)"


def test_parse_match_count():
    data = load_response("get_match_count")
    result = records.parse_match_count("xuid(123)", data)
    assert result.matchmade == 729


def test_parse_match_history():
    data = load_response("get_match_history")
    result = records.parse_match_history(data)
    expected = "a1219f5c-5942-4cd5-9ff1-4b6ea89905bc"
    assert result[0].match_id == expected


def test_parse_match_stats_match_info():
    data = load_response("get_match_stats")
    result = records.parse_match_info(data)
    expected = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert result.match_id == expected


def test_parse_match_stats_team_core_stats():
    data = load_response("get_match_stats")
    result = records.parse_team_core_stats(data)
    expected = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert result[0].match_id == expected


def test_parse_match_stats_player_core_stats():
    data = load_response("get_match_stats")
    result = records.parse_player_core_stats(data)
    expected = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert result[0].match_id == expected


def test_parse_match_stats_player_medal_stats():
    data = load_response("get_match_stats")
    result = records.parse_player_core_stats(data)
    expected = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert result[0].match_id == expected


def test_parse_game_variant():
    data = load_response("get_ugc_game_variant")
    result = records.parse_asset(data)
    assert result.name == "Fiesta:Slayer"


def test_parse_map_mode_pair():
    data = load_response("get_map_mode_pair")
    result = records.parse_asset(data)
    assert result.name == "Arena:Shotty Snipes Slayer on Catalyst"


def test_parse_map():
    data = load_response("get_map")
    result = records.parse_asset(data)
    assert result.name == "Forge Space"


def test_parse_playlist():
    data = load_response("get_playlist")
    result = records.parse_asset(data)
    assert result.name == "Ranked Arena"


if __name__ == "__main__":
    pytest.main()
