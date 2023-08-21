"""Test the SPNKR API client."""

from unittest.mock import AsyncMock

import pytest

from spnkr.client import HaloInfiniteClient


class MockSession:
    def __init__(self) -> None:
        self.headers = {}
        self.get = AsyncMock()


SESSION = MockSession()


@pytest.fixture
def client():
    return HaloInfiniteClient(SESSION, "spartan", "clearance")  # type: ignore


def test_header_update(client: HaloInfiniteClient):
    assert client.session.headers == {
        "Accept": "application/json",
        "x-343-authorization-spartan": "spartan",
        "343-clearance": "clearance",
    }


@pytest.mark.asyncio
async def test_get_medal_metadata(client: HaloInfiniteClient):
    await client.get_medal_metadata()
    SESSION.get.assert_called_with(
        "https://gamecms-hacs.svc.halowaypoint.com/hi/Waypoint/file/medals/metadata.json"
    )


@pytest.mark.asyncio
async def test_get_map_mode_pair(client: HaloInfiniteClient):
    await client.get_map_mode_pair("asset_id", "version_id")
    SESSION.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/mapModePairs/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_playlist(client: HaloInfiniteClient):
    await client.get_playlist("asset_id", "version_id")
    SESSION.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/playlists/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_map(client: HaloInfiniteClient):
    await client.get_map("asset_id", "version_id")
    SESSION.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/maps/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_ugc_game_variant(client: HaloInfiniteClient):
    await client.get_ugc_game_variant("asset_id", "version_id")
    SESSION.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/ugcGameVariants/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_match_skill(client: HaloInfiniteClient):
    await client.get_match_skill("match_id", [123])
    SESSION.get.assert_called_with(
        "https://skill.svc.halowaypoint.com:443/hi/matches/match_id/skill",
        params={"players": ["xuid(123)"]},
    )


@pytest.mark.asyncio
async def test_get_playlist_csr(client: HaloInfiniteClient):
    await client.get_playlist_csr("playlist_id", [123, 456])
    SESSION.get.assert_called_with(
        "https://skill.svc.halowaypoint.com:443/hi/playlist/playlist_id/csrs",
        params={"players": ["xuid(123)", "xuid(456)"]},
    )


@pytest.mark.asyncio
async def test_get_match_count(client: HaloInfiniteClient):
    await client.get_match_count(123)
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(123)/matches/count"
    )


@pytest.mark.asyncio
async def test_get_match_history(client: HaloInfiniteClient):
    await client.get_match_history(123, 0, 10, "all")
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(123)/matches",
        params={"start": 0, "count": 10, "type": "all"},
    )


@pytest.mark.asyncio
async def test_get_match_stats(client: HaloInfiniteClient):
    await client.get_match_stats("match_id")
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/matches/match_id/stats"
    )


if __name__ == "__main__":
    pytest.main()
