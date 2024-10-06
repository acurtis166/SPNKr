"""Test StatsService."""

import pytest

from spnkr.services.stats import StatsService


@pytest.fixture
def service(session):
    return StatsService(session)


@pytest.mark.asyncio
async def test_get_match_count(session, service: StatsService):
    session.set_response("get_match_count.json")
    await service.get_match_count(1234567890123456)
    session.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matches/count"
    )


@pytest.mark.asyncio
async def test_get_service_record(session, service: StatsService):
    session.set_response("get_service_record.json")
    await service.get_service_record(1234567890123456)
    session.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matchmade/servicerecord",
        params={},
    )


@pytest.mark.asyncio
async def test_get_service_record_season_playlist(session, service: StatsService):
    session.set_response("get_service_record.json")
    await service.get_service_record(
        1234567890123456,
        season_id="season_id",
        playlist_asset_id="playlist_asset_id",
    )
    session.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matchmade/servicerecord",
        params={
            "seasonid": "season_id",
            "playlistassetid": "playlist_asset_id",
        },
    )


@pytest.mark.asyncio
async def test_get_service_record_game_variant_category_ranked(
    session, service: StatsService
):
    session.set_response("get_service_record.json")
    await service.get_service_record(
        1234567890123456, game_variant_category=6, is_ranked=True
    )
    session.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matchmade/servicerecord",
        params={"gamevariantcategory": "6", "isranked": "True"},
    )


@pytest.mark.asyncio
async def test_get_service_record_invalid_match_type(service: StatsService):
    with pytest.raises(ValueError):
        await service.get_service_record(1234567890123456, match_type="invalid")  # type: ignore


@pytest.mark.asyncio
async def test_get_service_record_invalid_filter_combination(
    service: StatsService,
):
    with pytest.raises(ValueError):
        await service.get_service_record(1234567890123456, playlist_asset_id="")


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore")
async def test_get_service_record_non_matchmade_params_ignored(
    session, service: StatsService
):
    session.set_response("get_service_record.json")
    await service.get_service_record(
        1234567890123456, match_type="custom", is_ranked=True
    )
    session.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/custom/servicerecord",
        params={},
    )


@pytest.mark.asyncio
async def test_get_match_history(session, service: StatsService):
    session.set_response("get_match_history.json")
    await service.get_match_history(1234567890123456, 0, 10, "all")
    session.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/matches",
        params={"start": 0, "count": 10, "type": "all"},
    )


@pytest.mark.asyncio
async def test_get_match_stats(session, service: StatsService):
    session.set_response("get_match_stats.json")
    await service.get_match_stats("match_id")
    session.get.assert_called_with(
        "https://halostats.svc.halowaypoint.com:443/hi/matches/match_id/stats"
    )
