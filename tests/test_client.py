"""Test the SPNKR API client."""

import time
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
    """Test that the client headers are updated as expected."""
    assert client._session.headers == {
        "Accept": "application/json",
        "x-343-authorization-spartan": "spartan",
        "343-clearance": "clearance",
    }


def test_async_limiter_set(client: HaloInfiniteClient):
    """Test that the async limiter is set as expected."""
    assert client._rate_limiter is not None
    assert client._rate_limiter.max_rate / client._rate_limiter.time_period == 5


@pytest.mark.asyncio
async def test_rate_limiter(client: HaloInfiniteClient):
    """Test that the rate limiter limits requests as expected."""
    t0 = time.time()
    # Use 6 requests due to the default rate of 5 requests per second.
    for _ in range(6):
        await client._get("url")
    t1 = time.time()
    assert t1 - t0 >= 1


@pytest.mark.asyncio
async def test_rate_limiter_none(client: HaloInfiniteClient):
    """Test that the rate limiter does not limit requests if None."""
    client._rate_limiter = None
    t0 = time.time()
    for _ in range(6):
        await client._get("url")
    t1 = time.time()
    assert t1 - t0 < 1


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
    await client.get_match_skill("match_id", [1234567890123456])
    SESSION.get.assert_called_with(
        "https://skill.svc.halowaypoint.com:443/hi/matches/match_id/skill",
        params={"players": ["xuid(1234567890123456)"]},
    )


@pytest.mark.asyncio
async def test_get_playlist_csr(client: HaloInfiniteClient):
    await client.get_playlist_csr(
        "playlist_id", [1234567890123456, 2345678901234567]
    )
    SESSION.get.assert_called_with(
        "https://skill.svc.halowaypoint.com:443/hi/playlist/playlist_id/csrs",
        params={
            "players": ["xuid(1234567890123456)", "xuid(2345678901234567)"]
        },
    )


@pytest.mark.asyncio
async def test_get_match_count(client: HaloInfiniteClient):
    await client.get_match_count(1234567890123456)
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matches/count"
    )


@pytest.mark.asyncio
async def test_get_service_record(client: HaloInfiniteClient):
    await client.get_service_record(1234567890123456)
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matchmade/servicerecord",
        params={},
    )


@pytest.mark.asyncio
async def test_get_service_record_season_playlist(client: HaloInfiniteClient):
    await client.get_service_record(
        1234567890123456,
        season_id="season_id",
        playlist_asset_id="playlist_asset_id",
    )
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matchmade/servicerecord",
        params={
            "seasonid": "season_id",
            "playlistassetid": "playlist_asset_id",
        },
    )


@pytest.mark.asyncio
async def test_get_service_record_game_variant_category_ranked(
    client: HaloInfiniteClient,
):
    await client.get_service_record(
        1234567890123456, game_variant_category=6, is_ranked=True
    )
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matchmade/servicerecord",
        params={"gamevariantcategory": "6", "isranked": "True"},
    )


@pytest.mark.asyncio
async def test_get_service_record_invalid_match_type(
    client: HaloInfiniteClient,
):
    with pytest.raises(ValueError):
        await client.get_service_record(1234567890123456, match_type="invalid")  # type: ignore


@pytest.mark.asyncio
async def test_get_service_record_invalid_filter_combination(
    client: HaloInfiniteClient,
):
    with pytest.raises(ValueError):
        await client.get_service_record(1234567890123456, playlist_asset_id="")


@pytest.mark.asyncio
async def test_get_service_record_non_matchmade_params_ignored(
    client: HaloInfiniteClient,
):
    await client.get_service_record(
        1234567890123456, match_type="custom", is_ranked=True
    )
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/custom/servicerecord",
        params={},
    )


@pytest.mark.asyncio
async def test_get_match_history(client: HaloInfiniteClient):
    await client.get_match_history(1234567890123456, 0, 10, "all")
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matches",
        params={"start": 0, "count": 10, "type": "all"},
    )


@pytest.mark.asyncio
async def test_get_match_stats(client: HaloInfiniteClient):
    await client.get_match_stats("match_id")
    SESSION.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/matches/match_id/stats"
    )


@pytest.mark.asyncio
async def test_get_users_by_id(client: HaloInfiniteClient):
    await client.get_users_by_id(
        ["xuid(1234567890123456)", "xuid(2345678901234567)"]
    )
    SESSION.get.assert_called_with(
        "https://profile.svc.halowaypoint.com/users",
        params={"xuids": [1234567890123456, 2345678901234567]},
    )


if __name__ == "__main__":
    pytest.main()
