"""Test SkillService."""

import pytest

from spnkr.services.skill import SkillService, _clean_season_id


@pytest.fixture
def service(session):
    return SkillService(session)


@pytest.mark.asyncio
async def test_get_match_skill(session, service: SkillService):
    session.set_response("get_match_skill.json")
    await service.get_match_skill("match_id", [1234567890123456])
    session.get.assert_called_with(
        "https://skill.svc.halowaypoint.com:443/hi/matches/match_id/skill",
        params={"players": ["xuid(1234567890123456)"]},
    )


@pytest.mark.asyncio
async def test_get_playlist_csr(session, service: SkillService):
    session.set_response("get_playlist_csr.json")
    await service.get_playlist_csr(
        "playlist_id", [1234567890123456, 2345678901234567], "CsrSeason5-1"
    )
    session.get.assert_called_with(
        "https://skill.svc.halowaypoint.com:443/hi/playlist/playlist_id/csrs",
        params={
            "players": ["xuid(1234567890123456)", "xuid(2345678901234567)"],
            "season": "CsrSeason5-1",
        },
    )


def test_clean_season_id():
    assert _clean_season_id("Csr/Seasons/CsrSeason5-1.json") == "CsrSeason5-1"
    assert _clean_season_id(" csr/seasons/csrseason5-1.json ") == "csrseason5-1"
    assert _clean_season_id("CsrseasoN5-1") == "CsrseasoN5-1"
