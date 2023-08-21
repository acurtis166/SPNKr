import json
from pathlib import Path
from typing import Any, Callable
from uuid import UUID

import pytest

from spnkr import responses as resp
from spnkr.parsers.pydantic import PydanticParser

RESPONSES = Path("tests/responses")


class MockClientResponse:
    def __init__(self, data: dict) -> None:
        self.data = data

    async def json(self, loads: Callable | None = None) -> dict[str, Any]:
        return self.data


def load_response(file_name: str) -> MockClientResponse:
    with open(RESPONSES / f"{file_name}.json") as f:
        data = json.load(f)
    return MockClientResponse(data)


@pytest.fixture
def parser():
    return PydanticParser()


@pytest.mark.asyncio
async def test_parse_match_skill(parser: PydanticParser):
    client_response = load_response("get_match_skill")
    response = resp.MatchSkillResponse(client_response)
    result = await parser.parse_match_skill(response)
    assert result.value[0].id == "xuid(2535445291321133)"


@pytest.mark.asyncio
async def test_parse_playlist_csv(parser: PydanticParser):
    client_response = load_response("get_playlist_csr")
    response = resp.PlaylistCsrResponse(client_response)
    result = await parser.parse_playlist_csr(response)
    assert result.value[0].id == "xuid(2535445291321133)"


@pytest.mark.asyncio
async def test_parse_match_count(parser: PydanticParser):
    client_response = load_response("get_match_count")
    response = resp.MatchCountResponse(client_response)
    result = await parser.parse_match_count(response)
    assert result.matchmade_matches_played_count == 729


@pytest.mark.asyncio
async def test_parse_match_history(parser: PydanticParser):
    client_response = load_response("get_match_history")
    response = resp.MatchHistoryResponse(client_response)
    result = await parser.parse_match_history(response)
    expected = UUID("a1219f5c-5942-4cd5-9ff1-4b6ea89905bc")
    assert result.results[0].match_id == expected


@pytest.mark.asyncio
async def test_parse_match_stats(parser: PydanticParser):
    client_response = load_response("get_match_stats")
    response = resp.MatchStatsResponse(client_response)
    result = await parser.parse_match_stats(response)
    expected = UUID("6f050134-bede-47bc-a6df-eeafdcb9f97f")
    assert result.match_id == expected


@pytest.mark.asyncio
async def test_parse_game_variant(parser: PydanticParser):
    client_response = load_response("get_ugc_game_variant")
    response = resp.UgcGameVariantResponse(client_response)
    result = await parser.parse_game_variant(response)
    assert result.public_name == "Fiesta:Slayer"


@pytest.mark.asyncio
async def test_parse_map_mode_pair(parser: PydanticParser):
    client_response = load_response("get_map_mode_pair")
    response = resp.MapModePairResponse(client_response)
    result = await parser.parse_map_mode_pair(response)
    assert result.public_name == "Arena:Shotty Snipes Slayer on Catalyst"


@pytest.mark.asyncio
async def test_parse_map(parser: PydanticParser):
    client_response = load_response("get_map")
    response = resp.MapResponse(client_response)
    result = await parser.parse_map(response)
    assert result.public_name == "Forge Space"


@pytest.mark.asyncio
async def test_parse_playlist(parser: PydanticParser):
    client_response = load_response("get_playlist")
    response = resp.PlaylistResponse(client_response)
    result = await parser.parse_playlist(response)
    assert result.public_name == "Ranked Arena"


if __name__ == "__main__":
    pytest.main()
