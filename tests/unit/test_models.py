import json
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest

from spnkr.models.discovery_ugc import (
    AssetSearchPage,
    Film,
    Map,
    MapModePair,
    Playlist,
    UgcGameVariant,
)
from spnkr.models.economy import PlayerCustomization
from spnkr.models.gamecms_hacs import (
    CareerRewardTrack,
    CsrSeasonCalendar,
    MedalMetadata,
    SeasonCalendar,
)
from spnkr.models.profile import User
from spnkr.models.refdata import PlayerType
from spnkr.models.skill import MatchSkill, PlaylistCsr
from spnkr.models.stats import (
    MatchCount,
    MatchHistory,
    MatchStats,
    ServiceRecord,
)

RESPONSES = Path("tests/responses")


def load_response(name: str) -> Any:
    with open(RESPONSES / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def test_parse_medal_metadata():
    data = load_response("get_medal_metadata")
    result = MedalMetadata(**data)
    assert result.medals[0].name_id == 622331684


def test_parse_csr_season_calendar():
    data = load_response("get_csr_season_calendar")
    result = CsrSeasonCalendar(**data)
    assert len(result.seasons) == 8


def test_parse_season_calendar():
    data = load_response("get_season_calendar")
    result = SeasonCalendar(**data)
    assert len(result.events) == 30


def test_parse_career_reward_track():
    data = load_response("get_career_reward_track")
    result = CareerRewardTrack(**data)
    assert len(result.ranks) == 272
    assert result.name.value == "Career Rank"


def test_parse_match_skill():
    data = load_response("get_match_skill")
    result = MatchSkill(**data)
    assert result.value[0].id == "xuid(2535445291321133)"


def test_parse_playlist_csr():
    data = load_response("get_playlist_csr")
    result = PlaylistCsr(**data)
    assert result.value[0].id == "xuid(2535445291321133)"


def test_parse_match_count():
    data = load_response("get_match_count")
    result = MatchCount(**data)
    assert result.matchmade_matches_played_count == 729


def test_parse_service_record():
    data = load_response("get_service_record")
    result = ServiceRecord(**data)
    assert result.matches_completed == 1915


def test_parse_service_record_empty():
    data = load_response("get_service_record_empty")
    result = ServiceRecord(**data)
    assert result.matches_completed == 0


def test_parse_match_history():
    data = load_response("get_match_history")
    result = MatchHistory(**data)
    expected = UUID("a1219f5c-5942-4cd5-9ff1-4b6ea89905bc")
    assert result.results[0].match_id == expected


def test_parse_match_stats():
    data = load_response("get_match_stats")
    result = MatchStats(**data)
    expected = UUID("6f050134-bede-47bc-a6df-eeafdcb9f97f")
    assert result.match_id == expected


def test_parse_match_stats_ctf():
    data = load_response("get_match_stats_ctf")
    result = MatchStats(**data)
    expected = UUID("ffccbba6-fd52-4ff8-aa41-4bdc6487cd92")
    assert result.match_id == expected
    mode = result.players[0].player_team_stats[0].stats.capture_the_flag_stats
    assert mode is not None


def test_parse_match_stats_zones():
    data = load_response("get_match_stats_zones")
    result = MatchStats(**data)
    expected = UUID("ff9af871-ea6b-40c4-abe6-9aab6bfe1808")
    assert result.match_id == expected
    mode = result.players[0].player_team_stats[0].stats.zones_stats
    assert mode is not None


def test_parse_match_stats_elimination():
    data = load_response("get_match_stats_elimination")
    result = MatchStats(**data)
    expected = UUID("fe368e0b-9281-43ad-9b3d-9b16fe1e9402")
    assert result.match_id == expected
    mode = result.players[0].player_team_stats[0].stats.elimination_stats
    assert mode is not None


def test_parse_match_stats_oddball():
    data = load_response("get_match_stats_oddball")
    result = MatchStats(**data)
    expected = UUID("fe75a257-acd6-41ac-a778-8f86765639cb")
    assert result.match_id == expected
    mode = result.players[0].player_team_stats[0].stats.oddball_stats
    assert mode is not None


def test_parse_match_stats_stockpile():
    data = load_response("get_match_stats_stockpile")
    result = MatchStats(**data)
    expected = UUID("f40f4aa4-cc28-466d-b4ec-86fd86424083")
    assert result.match_id == expected
    mode = result.players[0].player_team_stats[0].stats.stockpile_stats
    assert mode is not None


def test_parse_match_stats_extraction():
    data = load_response("get_match_stats_extraction")
    result = MatchStats(**data)
    expected = UUID("44b9ca37-1d91-438a-8ef1-aa4cb78a19b2")
    assert result.match_id == expected
    mode = result.players[0].player_team_stats[0].stats.extraction_stats
    assert mode is not None


def test_player_stats_is_human():
    data = load_response("get_match_stats")
    result = MatchStats(**data)
    player = result.players[0]
    player = player.model_copy(update={"player_type": PlayerType.HUMAN})
    assert player.is_human
    player = player.model_copy(update={"player_type": PlayerType.BOT})
    assert not player.is_human


def test_parse_game_variant():
    data = load_response("get_ugc_game_variant")
    result = UgcGameVariant(**data)
    assert result.public_name == "Fiesta:Slayer"


def test_parse_map_mode_pair():
    data = load_response("get_map_mode_pair")
    result = MapModePair(**data)
    assert result.public_name == "Arena:Shotty Snipes Slayer on Catalyst"


def test_parse_map():
    data = load_response("get_map")
    result = Map(**data)
    assert result.public_name == "Forge Space"


def test_parse_playlist():
    data = load_response("get_playlist")
    result = Playlist(**data)
    assert result.public_name == "Ranked Arena"


def test_parse_asset_search_page():
    data = load_response("search_assets")
    result = AssetSearchPage(**data)
    assert len(result.results) == 10


def test_parse_film():
    data = load_response("get_film_by_match_id")
    result = Film(**data)
    assert len(result.custom_data.chunks) == 27


def test_film_get_chunks_and_urls():
    data = load_response("get_film_by_match_id")
    result = Film(**data)
    chunk_urls = result.get_chunks_and_urls()
    assert len(chunk_urls) == 27
    assert chunk_urls[0][0].chunk_type == 1  # Chunk header
    assert chunk_urls[0][1] == (
        "https://blobs-infiniteugc.svc.halowaypoint.com/ugcstorage/film/3a86cc7e-4a15-49a0-b17d-1b1cdf16c49f/86ab777c-895d-4237-9fa0-43c7932322ac/filmChunk0"
    )


def test_parse_user():
    data = load_response("get_user")
    result = User(**data)
    assert result.xuid == 1234567890


def test_parse_users():
    data = load_response("get_users")
    result = [User(**user) for user in data]
    assert len(result) == 1
    assert result[0].xuid == 1234567890123456


def test_parse_player_customization():
    data = load_response("get_player_customization")
    result = PlayerCustomization(**data)
    assert result.spartan_body.left_arm == "None"


if __name__ == "__main__":
    pytest.main()
