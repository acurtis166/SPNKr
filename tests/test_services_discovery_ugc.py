"""Test DiscoveryUgcService."""

import pytest

from spnkr.services.discovery_ugc import DiscoveryUgcService


@pytest.fixture
def service(session):
    return DiscoveryUgcService(session)


@pytest.mark.asyncio
async def test_get_map_mode_pair(session, service: DiscoveryUgcService):
    await service.get_map_mode_pair("asset_id", "version_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/mapModePairs/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_playlist(session, service: DiscoveryUgcService):
    await service.get_playlist("asset_id", "version_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/playlists/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_map(session, service: DiscoveryUgcService):
    await service.get_map("asset_id", "version_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/maps/asset_id/versions/version_id"
    )


@pytest.mark.asyncio
async def test_get_ugc_game_variant(session, service: DiscoveryUgcService):
    await service.get_ugc_game_variant("asset_id", "version_id")
    session.get.assert_called_with(
        "https://discovery-infiniteugc.svc.halowaypoint.com:443/hi/ugcGameVariants/asset_id/versions/version_id"
    )
