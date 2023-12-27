"""Test the spnkr.match module."""

import json
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from spnkr.client import HaloInfiniteClient
from spnkr.match import Match
from spnkr.models.profile import User
from spnkr.models.refdata import LifecycleMode
from spnkr.models.stats import MatchInfo, MatchStats


def get_match_stats():
    with open("tests/responses/get_match_stats.json", "rb") as f:
        return MatchStats(**json.load(f))


def get_match_info():
    return get_match_stats().match_info


def get_users():
    with open("tests/responses/get_users.json", "rb") as f:
        return [User(**user) for user in json.load(f)]


class MockStatsService:
    def __init__(self) -> None:
        self.get_match_stats = AsyncMock()
        self.get_match_stats.return_value = get_match_stats()


class MockSkillService:
    def __init__(self) -> None:
        self.get_match_skill = AsyncMock()


class MockDiscoveryUgcService:
    def __init__(self) -> None:
        self.get_map_mode_pair = AsyncMock()
        self.get_playlist = AsyncMock()
        self.get_map = AsyncMock()
        self.get_ugc_game_variant = AsyncMock()


class MockProfileService:
    def __init__(self) -> None:
        self.get_users_by_id = AsyncMock()


class MockClient:
    def __init__(self) -> None:
        self.stats = MockStatsService()
        self.skill = MockSkillService()
        self.discovery_ugc = MockDiscoveryUgcService()
        self.profile = MockProfileService()


@pytest.fixture
def client():
    return MockClient()


@pytest.fixture
def match(client):
    return Match(client, "00000000-0000-0000-0000-000000000000")


def test_match_init_str(match: Match):
    assert match.id == UUID("00000000-0000-0000-0000-000000000000")


def test_match_init_uuid(client):
    match = Match(client, uuid4())
    assert isinstance(match.id, UUID)


@pytest.mark.asyncio
async def test_match_get_stats_caching(client, match: Match):
    await match.get_stats()
    await match.get_stats()
    assert client.stats.get_match_stats.call_count == 1


@pytest.mark.asyncio
async def test_match_get_stats(match: Match):
    assert match._stats is None
    stats = await match.get_stats()
    assert str(stats.match_id) == "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    assert isinstance(match._stats, MatchStats)


@pytest.mark.asyncio
async def test_match_get_stats_already_set(match: Match):
    stats_a = await match.get_stats()
    stats_b = await match.get_stats()
    assert id(stats_a) == id(stats_b)


@pytest.mark.asyncio
async def test_match_get_info_already_set(match: Match):
    info_a = await match.get_info()
    info_b = await match.get_info()
    assert id(info_a) == id(info_b)


@pytest.mark.asyncio
async def test_match_get_info(match: Match):
    info = await match.get_info()
    assert info.start_time.date().isoformat() == "2022-07-27"


@pytest.mark.asyncio
async def test_match_get_map(client, match: Match):
    await match.get_map()
    client.discovery_ugc.get_map.assert_called_once_with(
        UUID("e859cf75-9b8a-429a-91be-2376681c8537"),
        UUID("cd1f9a4e-b02f-4eb8-89e7-b61fa1010452"),
    )


@pytest.mark.asyncio
async def test_match_get_map_info_set(client, match: Match):
    match._info = get_match_info()
    await match.get_map()
    client.stats.get_match_stats.assert_not_called()


@pytest.mark.asyncio
async def test_match_get_mode(client, match: Match):
    await match.get_mode()
    client.discovery_ugc.get_ugc_game_variant.assert_called_once_with(
        UUID("507191c6-a492-4331-b2ae-a172101eb23e"),
        UUID("ee8c890b-a95f-4154-bac6-0009992d74f6"),
    )


@pytest.mark.asyncio
async def test_match_get_playlist(client, match: Match):
    await match.get_playlist()
    client.discovery_ugc.get_playlist.assert_called_once_with(
        UUID("edfef3ac-9cbe-4fa2-b949-8f29deafd483"),
        UUID("6c1bb887-628f-4a16-a794-f07adad39a38"),
    )


@pytest.mark.asyncio
async def test_match_get_playlist_non_matchmade(session):
    client = HaloInfiniteClient(session, "", "")
    match = Match(client, uuid4())
    match._info = get_match_info().model_copy(update={"playlist": None})
    playlist = await match.get_playlist()
    assert playlist is None


@pytest.mark.asyncio
async def test_match_get_map_mode_pair(client, match: Match):
    await match.get_map_mode_pair()
    client.discovery_ugc.get_map_mode_pair.assert_called_once_with(
        UUID("69d25f16-bc62-4d58-baf7-6210f65461f3"),
        UUID("91ca22c3-e2a8-4586-8011-a4888f175d3e"),
    )


@pytest.mark.asyncio
async def test_match_get_map_mode_pair_non_matchmade(session):
    client = HaloInfiniteClient(session, "", "")
    match = Match(client, uuid4())
    new_data = {"playlist_map_mode_pair": None}
    match._info = get_match_info().model_copy(update=new_data)
    map_mode_pair = await match.get_map_mode_pair()
    assert map_mode_pair is None


@pytest.mark.asyncio
async def test_match_get_users(client, match: Match):
    await match.get_users()
    expected_ids = [
        "xuid(2533274797283717)",
        "xuid(2533274892674451)",
        "xuid(2533274974206999)",
        "xuid(2535469531821339)",
        "xuid(2535412760927018)",
        "xuid(2533274876924991)",
        "xuid(2535413591152112)",
    ]
    client.profile.get_users_by_id.assert_called_once_with(expected_ids)


@pytest.mark.asyncio
async def test_match_get_users_dict(client, match: Match):
    client.profile.get_users_by_id.return_value = get_users()
    users = await match.get_users()
    assert users["xuid(1234567890123456)"].gamertag == "GAMERTAG"


@pytest.mark.asyncio
async def test_match_get_skill(client, match: Match):
    await match.get_skill()
    expected_ids = [
        "xuid(2533274797283717)",
        "xuid(2533274892674451)",
        "xuid(2533274974206999)",
        "xuid(2535469531821339)",
        "xuid(2535412760927018)",
        "xuid(2533274876924991)",
        "xuid(2535413591152112)",
    ]
    client.skill.get_match_skill.assert_called_once_with(
        UUID("00000000-0000-0000-0000-000000000000"), expected_ids
    )


@pytest.mark.asyncio
async def test_match_get_skill_non_matchmade(session):
    client = HaloInfiniteClient(session, "", "")
    match = Match(client, uuid4())
    info = get_match_info()
    new_data = {"lifecycle_mode": LifecycleMode.CUSTOM}
    match._info = info.model_copy(update=new_data)
    assert await match.get_skill() is None
