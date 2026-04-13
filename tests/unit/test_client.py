"""Test the SPNKR API client."""

import asyncio
import time

import pytest

from spnkr.client import HaloInfiniteClient
from spnkr.services import (
    DiscoveryUgcService,
    EconomyService,
    GameCmsHacsService,
    ProfileService,
    SkillService,
    StatsService,
)


@pytest.fixture
def client(session):
    return HaloInfiniteClient(session, "spartan", "clearance", 5)


def test_client_set_tokens(client: HaloInfiniteClient):
    """Test that the client headers are set in the `set_tokens` method."""
    assert client._session.headers == {
        "Accept": "application/json",
        "x-343-authorization-spartan": "spartan",
        "343-clearance": "clearance",
    }
    client.set_tokens("new_spartan", "new_clearance")
    assert client._session.headers == {
        "Accept": "application/json",
        "x-343-authorization-spartan": "new_spartan",
        "343-clearance": "new_clearance",
    }


def test_client_services(client: HaloInfiniteClient):
    """Test that the client services are created as expected."""
    assert isinstance(client.discovery_ugc, DiscoveryUgcService)
    assert isinstance(client.economy, EconomyService)
    assert isinstance(client.gamecms_hacs, GameCmsHacsService)
    assert isinstance(client.profile, ProfileService)
    assert isinstance(client.skill, SkillService)
    assert isinstance(client.stats, StatsService)


@pytest.mark.asyncio
async def test_client_get_active_operation_pass(session, client: HaloInfiniteClient):
    session.set_responses(
        "get_player_reward_track_operations.json",
        "get_operation_reward_track.json",
    )

    operation_pass = await client.get_active_operation_pass("MyGamertag")

    assert operation_pass is not None
    assert operation_pass.is_active
    assert operation_pass.track_id == "S05OpPassM01"
    assert operation_pass.name == "Combined Arms"
    assert operation_pass.last_unlocked_rank == 5
    assert operation_pass.next_rank == 6
    assert operation_pass.progress_fraction == 0.25
    assert operation_pass.status == "in_progress"
    assert [call.args[0] for call in session.get.await_args_list] == [
        "https://economy.svc.halowaypoint.com:443/hi/players/MyGamertag/rewardtracks/operations",
        "https://gamecms-hacs.svc.halowaypoint.com/hi/Progression/file/RewardTracks/Operations/S05OpPassM01.json",
    ]


@pytest.mark.asyncio
async def test_client_get_operation_passes(session, client: HaloInfiniteClient):
    session.set_responses(
        "get_player_reward_track_operations.json",
        "get_operation_reward_track.json",
        "get_operation_reward_track.json",
        "get_operation_reward_track.json",
    )

    operation_passes = await client.get_operation_passes("MyGamertag")

    assert [operation_pass.track_id for operation_pass in operation_passes] == [
        "S05OpPassL01",
        "S05OpPassM01",
        "S05OpPassM02",
    ]
    assert [operation_pass.status for operation_pass in operation_passes] == [
        "completed",
        "in_progress",
        "not_started",
    ]
    assert operation_passes[1].is_active


@pytest.mark.asyncio
async def test_client_requests_per_second_multiple_services(
    client: HaloInfiniteClient,
):
    """Test that requests per second is applied per service."""
    tasks = []
    for _ in range(3):
        tasks.append(client.discovery_ugc._get(""))
        tasks.append(client.gamecms_hacs._get(""))
        tasks.append(client.profile._get(""))
        tasks.append(client.skill._get(""))
        tasks.append(client.stats._get(""))
    t0 = time.time()
    await asyncio.gather(*tasks)
    t1 = time.time()
    assert t1 - t0 <= 1
