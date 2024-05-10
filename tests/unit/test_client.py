"""Test the SPNKR API client."""

import asyncio
import time

import pytest

from spnkr.client import HaloInfiniteClient
from spnkr.services import (
    DiscoveryUgcService,
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
    assert isinstance(client.gamecms_hacs, GameCmsHacsService)
    assert isinstance(client.profile, ProfileService)
    assert isinstance(client.skill, SkillService)
    assert isinstance(client.stats, StatsService)


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
