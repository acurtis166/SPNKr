"""Test the SPNKR API client."""

import json

import pytest

from spnkr.api.client import SPNKR, AzureApp, _unwrap_xuid, _wrap_xuid

ENDPOINT_FILES = {
    "https://ugc-discovery.svc.halowaypoint.com:443/hi/ugcGameVariants/asset_id/versions/version_id": (
        "get_ugc_game_variant.json"
    ),
    "https://ugc-discovery.svc.halowaypoint.com:443/hi/mapModePairs/asset_id/versions/version_id": (
        "get_map_mode_pair.json"
    ),
    "https://ugc-discovery.svc.halowaypoint.com:443/hi/maps/asset_id/versions/version_id": (
        "get_map.json"
    ),
    "https://ugc-discovery.svc.halowaypoint.com:443/hi/playlists/asset_id/versions/version_id": (
        "get_playlist.json"
    ),
    "https://profile.xboxlive.com:443/users/batch/profile/settings": (
        "get_profiles.json"
    ),
    "https://profile.xboxlive.com:443/users/xuid(123)/profile/settings": (
        "get_profiles.json"
    ),
    "https://profile.xboxlive.com:443/users/gt(aCurtis X89)/profile/settings": (
        "get_profiles.json"
    ),
    "https://skill.svc.halowaypoint.com:443/hi/matches/match_id/skill": (
        "get_match_skill.json"
    ),
    "https://skill.svc.halowaypoint.com:443/hi/playlist/playlist_id/csrs": (
        "get_playlist_csr.json"
    ),
    "https://stats.svc.halowaypoint.com:443/hi/players/xuid(123)/matches/count": (
        "get_match_count.json"
    ),
    "https://stats.svc.halowaypoint.com:443/hi/players/xuid(123)/matches": (
        "get_match_history.json"
    ),
    "https://stats.svc.halowaypoint.com:443/hi/matches/match_id/stats": (
        "get_match_stats.json"
    ),
}


class MockResponse:
    def __init__(self, data, status):
        self.data = data
        self.status = status
        self.error = None

    async def json(self, *args, **kwargs):
        return self.data


class MockSession:
    def __init__(self):
        ...

    async def get(self, url, *args, **kwargs):
        file = ENDPOINT_FILES[url]
        with open(f"tests/responses/{file}", "r") as f:
            return MockResponse(json.load(f), 200)

    async def post(self, url, *args, **kwargs):
        file = ENDPOINT_FILES[url]
        with open(f"tests/responses/{file}", "r") as f:
            return MockResponse(json.load(f), 200)


@pytest.fixture
def client():
    app = AzureApp("", "", "")
    spnkr = SPNKR(app, "")
    spnkr._session = MockSession()  # type: ignore
    return spnkr


def test_unwrap_xuid():
    assert _unwrap_xuid(123) == "123"
    assert _unwrap_xuid("123") == "123"
    assert _unwrap_xuid("xuid(123)") == "123"


def test_wrap_xuid():
    assert _wrap_xuid(123) == "xuid(123)"
    assert _wrap_xuid("123") == "xuid(123)"
    assert _wrap_xuid("xuid(123)") == "xuid(123)"


@pytest.mark.asyncio
async def test_get_map_mode_pair(client: SPNKR):
    result = await client.get_map_mode_pair("asset_id", "version_id")
    assert str(result.id) == "95018e68-41fc-4d5f-b627-15590feb7469"
    assert result.name == "Arena:Shotty Snipes Slayer on Catalyst"


@pytest.mark.asyncio
async def test_get_playlist(client: SPNKR):
    result = await client.get_playlist("asset_id", "version_id")
    assert str(result.id) == "edfef3ac-9cbe-4fa2-b949-8f29deafd483"
    assert result.name == "Ranked Arena"


@pytest.mark.asyncio
async def test_get_map(client: SPNKR):
    result = await client.get_map("asset_id", "version_id")
    assert str(result.id) == "76669255-697d-48c9-a802-7ff2ec8257f1"
    assert result.name == "Forge Space"


@pytest.mark.asyncio
async def test_get_ugc_game_variant(client: SPNKR):
    result = await client.get_ugc_game_variant("asset_id", "version_id")
    assert str(result.id) == "aca7bbf8-7a18-4aae-8785-1bd3f58275fd"
    assert result.name == "Fiesta:Slayer"


@pytest.mark.asyncio
async def test_get_gamertags_by_xuids(client: SPNKR):
    result = await client.get_gamertags_by_xuids([123])
    assert result.gamertags == {"2535445291321133": "aCurtis X89"}


@pytest.mark.asyncio
async def test_get_gamertag_by_xuid(client: SPNKR):
    result = await client.get_gamertag_by_xuid(123)
    assert result.gamertags == {"2535445291321133": "aCurtis X89"}


@pytest.mark.asyncio
async def test_get_xuid_by_gamertag(client: SPNKR):
    result = await client.get_xuid_by_gamertag("aCurtis X89")
    assert result.gamertags == {"2535445291321133": "aCurtis X89"}


@pytest.mark.asyncio
async def test_get_match_skill(client: SPNKR):
    result = await client.get_match_skill("match_id", [123])
    assert result.results["xuid(2535445291321133)"].pre_match_csr.value == 1530


@pytest.mark.asyncio
async def test_get_playlist_csr(client: SPNKR):
    result = await client.get_playlist_csr("playlist_id", [123])
    assert result.results["xuid(2535445291321133)"].all_time_max.value == 1549


@pytest.mark.asyncio
async def test_get_match_count(client: SPNKR):
    result = await client.get_match_count(123)
    assert result.total == 731


@pytest.mark.asyncio
async def test_get_match_history(client: SPNKR):
    result = await client.get_match_history(123)
    assert len(result.matches) == 25


@pytest.mark.asyncio
async def test_get_match_stats(client: SPNKR):
    result = await client.get_match_stats("match_id")
    assert len(result.players) == 8


if __name__ == "__main__":
    pytest.main()
