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


@pytest.mark.asyncio
async def test_get_csr_season_calendar(session, service: GameCmsHacsService):
    session.set_response("get_csr_season_calendar.json")
    await service.get_csr_season_calendar()
    session.get.assert_called_with(
        "https://gamecms-hacs.svc.halowaypoint.com/hi/Progression/file/Csr/Calendars/CsrSeasonCalendar.json"
    )


@pytest.mark.asyncio
async def test_get_season_calendar(session, service: GameCmsHacsService):
    session.set_response("get_season_calendar.json")
    await service.get_season_calendar()
    session.get.assert_called_with(
        "https://gamecms-hacs.svc.halowaypoint.com/hi/progression/file/calendars/seasons/seasoncalendar.json"
    )


@pytest.mark.asyncio
async def test_get_career_reward_track(session, service: GameCmsHacsService):
    session.set_response("get_career_reward_track.json")
    await service.get_career_reward_track()
    session.get.assert_called_with(
        "https://gamecms-hacs.svc.halowaypoint.com/hi/Progression/file/RewardTracks/CareerRanks/careerRank1.json"
    )


@pytest.mark.asyncio
async def test_get_image(session, service: GameCmsHacsService):
    session.set_response("career_rank_corporal_gold_III.png")
    result = await service.get_image("path/to/image.png")
    assert round(len(await result.read()) / 1024) == 15
    session.get.assert_called_with(
        "https://gamecms-hacs.svc.halowaypoint.com/hi/images/file/path/to/image.png"
    )
