import json
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest

from spnkr.parsers import pydantic as pp

RESPONSES = Path("tests/responses")


def load_response(name: str) -> Any:
    with open(RESPONSES / f"{name}.json") as f:
        return json.load(f)


def test_parse_match_skill():
    data = load_response("get_match_skill")
    result = pp.MatchSkill(**data)
    assert result.value[0].id == "xuid(2535445291321133)"


def test_parse_playlist_csr():
    data = load_response("get_playlist_csr")
    result = pp.PlaylistCsr(**data)
    assert result.value[0].id == "xuid(2535445291321133)"


def test_parse_match_count():
    data = load_response("get_match_count")
    result = pp.MatchCount(**data)
    assert result.matchmade_matches_played_count == 729


def test_parse_match_history():
    data = load_response("get_match_history")
    result = pp.MatchHistory(**data)
    expected = UUID("a1219f5c-5942-4cd5-9ff1-4b6ea89905bc")
    assert result.results[0].match_id == expected


def test_parse_match_stats():
    data = load_response("get_match_stats")
    result = pp.MatchStats(**data)
    expected = UUID("6f050134-bede-47bc-a6df-eeafdcb9f97f")
    assert result.match_id == expected


def test_parse_game_variant():
    data = load_response("get_ugc_game_variant")
    result = pp.UgcGameVariant(**data)
    assert result.public_name == "Fiesta:Slayer"


def test_parse_map_mode_pair():
    data = load_response("get_map_mode_pair")
    result = pp.MapModePair(**data)
    assert result.public_name == "Arena:Shotty Snipes Slayer on Catalyst"


def test_parse_map():
    data = load_response("get_map")
    result = pp.Map(**data)
    assert result.public_name == "Forge Space"


def test_parse_playlist():
    data = load_response("get_playlist")
    result = pp.Playlist(**data)
    assert result.public_name == "Ranked Arena"


if __name__ == "__main__":
    pytest.main()