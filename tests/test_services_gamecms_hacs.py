"""Test GameContentHacsService."""

import pytest

from spnkr.services.gamecms_hacs import GameCmsHacsService


@pytest.fixture
def service(session):
    return GameCmsHacsService(session)


@pytest.mark.asyncio
async def test_get_medal_metadata(session, service: GameCmsHacsService):
    session.set_response("get_medal_metadata.json")
    await service.get_medal_metadata()
    session.get.assert_called_with(
        "https://gamecms-hacs.svc.halowaypoint.com/hi/Waypoint/file/medals/metadata.json"
    )
