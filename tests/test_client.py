"""Test the SPNKR API client."""

import json

import pytest

from spnkr.client import HaloInfiniteClient


class MockResponse:
    def raise_for_status(self):
        ...


class MockSession:
    async def get(self, url: str, *args, **kwargs) -> MockResponse:
        return MockResponse()


@pytest.fixture
def client():
    return HaloInfiniteClient(MockSession(), "spartan", "clearance")  # type: ignore


@pytest.mark.asyncio
async def test_get_map_mode_pair(client: HaloInfiniteClient):
    result = await client.get_map_mode_pair("asset_id", "version_id")


# @pytest.mark.asyncio
# async def test_get_playlist(client: HaloInfiniteClient):
#     result = await client.get_playlist("asset_id", "version_id")
#     assert str(result.id) == "edfef3ac-9cbe-4fa2-b949-8f29deafd483"
#     assert result.name == "Ranked Arena"


# @pytest.mark.asyncio
# async def test_get_map(client: HaloInfiniteClient):
#     result = await client.get_map("asset_id", "version_id")
#     assert str(result.id) == "76669255-697d-48c9-a802-7ff2ec8257f1"
#     assert result.name == "Forge Space"


# @pytest.mark.asyncio
# async def test_get_ugc_game_variant(client: HaloInfiniteClient):
#     result = await client.get_ugc_game_variant("asset_id", "version_id")
#     assert str(result.id) == "aca7bbf8-7a18-4aae-8785-1bd3f58275fd"
#     assert result.name == "Fiesta:Slayer"


# @pytest.mark.asyncio
# async def test_get_match_skill(client: HaloInfiniteClient):
#     result = await client.get_match_skill("match_id", [123])
#     assert result.results["xuid(2535445291321133)"].pre_match_csr.value == 1530


# @pytest.mark.asyncio
# async def test_get_playlist_csr(client: HaloInfiniteClient):
#     result = await client.get_playlist_csr("playlist_id", [123])
#     assert result.results["xuid(2535445291321133)"].all_time_max.value == 1549


# @pytest.mark.asyncio
# async def test_get_match_count(client: HaloInfiniteClient):
#     result = await client.get_match_count(123)
#     assert result.total == 731


# @pytest.mark.asyncio
# async def test_get_match_history(client: HaloInfiniteClient):
#     result = await client.get_match_history(123)
#     assert len(result.matches) == 25


# @pytest.mark.asyncio
# async def test_get_match_stats(client: HaloInfiniteClient):
#     result = await client.get_match_stats("match_id")
#     assert len(result.players) == 8


if __name__ == "__main__":
    pytest.main()
