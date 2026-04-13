"""Test EconomyService."""

import pytest

from spnkr.services.economy import EconomyService


@pytest.fixture
def service(session):
    return EconomyService(session)


@pytest.mark.asyncio
async def test_get_player_customization(session, service: EconomyService):
    session.set_response("get_player_customization.json")
    await service.get_player_customization("MyGamertag")
    session.get.assert_called_with(
        "https://economy.svc.halowaypoint.com:443/hi/players/MyGamertag/customization",
        params={"view": "public"},
    )


@pytest.mark.asyncio
async def test_get_player_reward_track_operations(session, service: EconomyService):
    session.set_response("get_player_reward_track_operations.json")
    response = await service.get_player_reward_track_operations("MyGamertag")
    payload = await response.parse()

    assert payload.active is not None
    assert payload.active.track_id == "S05OpPassM01"
    assert [operation.track_id for operation in payload.completed] == ["S05OpPassL01"]
    assert [operation.track_id for operation in payload.in_progress] == ["S05OpPassM01"]
    assert [operation.track_id for operation in payload.not_started] == ["S05OpPassM02"]
    session.get.assert_called_with(
        "https://economy.svc.halowaypoint.com:443/hi/players/MyGamertag/rewardtracks/operations"
    )


@pytest.mark.asyncio
async def test_get_player_career_rank(session, service: EconomyService):
    session.set_response("get_player_career_rank.json")
    response = await service.get_player_career_rank("MyGamertag")
    payload = await response.parse()

    assert payload.current_progress.rank == 271
    assert payload.current_progress.partial_progress == 500
    assert payload.spartan_id == "spartan-1234"
    session.get.assert_called_with(
        "https://economy.svc.halowaypoint.com:443/hi/players/MyGamertag/rewardtracks/careerranks/careerrank1"
    )
