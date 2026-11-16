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


def test_client_invalid_requests_per_second(session):
    """Test that initializing the client with invalid requests_per_second raises ValueError."""
    with pytest.raises(ValueError):
        HaloInfiniteClient(session, "spartan", "clearance", requests_per_second=0)
    with pytest.raises(ValueError):
        HaloInfiniteClient(session, "spartan", "clearance", requests_per_second=-1)


def test_client_set_tokens(client: HaloInfiniteClient):
    """Test that the client headers are set in the `set_tokens` method."""
    assert client._session.headers == {
        "x-343-authorization-spartan": "spartan",
        "343-clearance": "clearance",
    }
    client.spartan_token = "new_spartan"
    client.clearance_token = "new_clearance"
    assert client._session.headers == {
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
