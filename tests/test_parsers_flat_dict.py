"""Test flattened dictionary parsing of Halo Infinite API responses."""

import json
from pathlib import Path
from typing import Any

import pytest

from spnkr.parsers import records

RESPONSES = Path("tests/responses")


def load_response(name: str) -> Any:
    with open(RESPONSES / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def test_parse_medal_metadata():
    data = load_response("get_medal_metadata")
    result = records.parse_medal_metadata(data)
    assert result[0]["name_id"] == 622331684


def test_parse_match_skill():
    data = load_response("get_match_skill")
    result = records.parse_match_skill(data)
    assert result[0]["xuid"] == "xuid(2535445291321133)"


def test_parse_playlist_csr():
    data = load_response("get_playlist_csr")
    result = records.parse_playlist_csr(data)
    assert result[0]["xuid"] == "xuid(2535445291321133)"


def test_parse_match_count():
    data = load_response("get_match_count")
    result = records.parse_match_count(data)
    assert result["matchmade"] == 729


def test_parse_match_history():
    data = load_response("get_match_history")
    result = records.parse_match_history(data)
    expected = "a1219f5c-5942-4cd5-9ff1-4b6ea89905bc"
    assert result[0]["match_id"] == expected


def test_parse_match_stats_match_info():
    data = load_response("get_match_stats")
    result = records.parse_match_info(data)
    expected = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert result["match_id"] == expected


def test_parse_match_stats_team_core_stats():
    data = load_response("get_match_stats")
    result = records.parse_team_core_stats(data)
    expected = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert result[0]["match_id"] == expected


def test_parse_match_stats_player_core_stats():
    data = load_response("get_match_stats")
    result = records.parse_player_core_stats(data)
    expected = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert result[0]["match_id"] == expected


def test_parse_match_stats_player_medal_stats():
    data = load_response("get_match_stats")
    result = records.parse_player_core_stats(data)
    expected = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert result[0]["match_id"] == expected


def test_parse_game_variant():
    data = load_response("get_ugc_game_variant")
    result = records.parse_asset(data)
    assert result["name"] == "Fiesta:Slayer"


def test_parse_map_mode_pair():
    data = load_response("get_map_mode_pair")
    result = records.parse_asset(data)
    assert result["name"] == "Arena:Shotty Snipes Slayer on Catalyst"


def test_parse_map():
    data = load_response("get_map")
    result = records.parse_asset(data)
    assert result["name"] == "Forge Space"


def test_parse_playlist():
    data = load_response("get_playlist")
    result = records.parse_asset(data)
    assert result["name"] == "Ranked Arena"


if __name__ == "__main__":
    pytest.main()
