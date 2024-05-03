"""Test EconomyService."""

import pytest

from spnkr.services.economy import EconomyService


@pytest.fixture
def service(session):
    return EconomyService(session)


@pytest.mark.asyncio
async def test_get_player_customization(session, service: EconomyService):
    session.set_response("get_player_customization.json")
    await service.get_player_customization(1234567890123456)
    session.get.assert_called_with(
        "https://economy.svc.halowaypoint.com:443/hi/players/xuid(1234567890123456)/customization",
        params={"view": "public"},
    )
