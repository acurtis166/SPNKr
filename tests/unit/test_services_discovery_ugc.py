"""Test DiscoveryUgcService."""

import datetime as dt

import pytest

from spnkr.services.discovery_ugc import DiscoveryUgcService


@pytest.fixture
def service(session):
    return DiscoveryUgcService(session)


@pytest.mark.asyncio
async def test_get_map_mode_pair(session, service: DiscoveryUgcService):
    session.set_response("get_map_mode_pair.json")
    await service.get_map_mode_pair("asset_id", "version_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/mapModePairs/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_playlist(session, service: DiscoveryUgcService):
    session.set_response("get_playlist.json")
    await service.get_playlist("asset_id", "version_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/playlists/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_map(session, service: DiscoveryUgcService):
    session.set_response("get_map.json")
    await service.get_map("asset_id", "version_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/maps/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_ugc_game_variant(session, service: DiscoveryUgcService):
    session.set_response("get_ugc_game_variant.json")
    await service.get_ugc_game_variant("asset_id", "version_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/ugcGameVariants/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_search_assets_default(session, service: DiscoveryUgcService):
    session.set_response("search_assets.json")
    await service.search_assets(start=0, count=10, sort="plays_recent", order="desc")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/search",
        params={
            "start": 0,
            "count": 10,
            "sort": "playsrecent",
            "order": "desc",
        },
    )


@pytest.mark.asyncio
async def test_search_assets_all(session, service: DiscoveryUgcService):
    session.set_response("search_assets.json")
    await service.search_assets(
        start=0,
        count=10,
        sort="plays_recent",
        order="desc",
        asset_kind="map",
        term="Live Fire",
        tags=["343i"],
        author="aaid(123)",
        average_rating_min=4.0,
        from_date_created_utc=dt.date(2021, 1, 1),
        to_date_created_utc=dt.date(2021, 1, 31),
        from_date_modified_utc=dt.date(2021, 1, 1),
        to_date_modified_utc=dt.date(2021, 1, 31),
        from_date_published_utc=dt.date(2021, 1, 1),
        to_date_published_utc=dt.date(2021, 1, 31),
    )
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/search",
        params={
            "start": 0,
            "count": 10,
            "sort": "playsrecent",
            "order": "desc",
            "assetKind": "map",
            "term": "Live Fire",
            "tags": ["343i"],
            "author": "aaid(123)",
            "averageRatingMin": 4.0,
            "fromDateCreatedUtc": "2021-01-01",
            "toDateCreatedUtc": "2021-01-31",
            "fromDateModifiedUtc": "2021-01-01",
            "toDateModifiedUtc": "2021-01-31",
            "fromDatePublishedUtc": "2021-01-01",
            "toDatePublishedUtc": "2021-01-31",
        },
    )


@pytest.mark.asyncio
async def test_search_assets_invalid_count(service: DiscoveryUgcService):
    with pytest.raises(ValueError):
        await service.search_assets(start=0, count=0)
    with pytest.raises(ValueError):
        await service.search_assets(start=0, count=102)


@pytest.mark.asyncio
async def test_get_film_by_match_id(session, service: DiscoveryUgcService):
    session.set_response("get_film_by_match_id.json")
    await service.get_film_by_match_id("match_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/films/matches/match_id/spectate"
    )
