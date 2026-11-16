"""Test the SPNKR API client."""

import asyncio
import time

import pytest

from spnkr.client import HaloInfiniteClient


@pytest.fixture
def client(session):
    return HaloInfiniteClient(session, "spartan", "clearance", 5)


def test_client_invalid_requests_per_second(session):
    """Test that initializing the client with invalid requests_per_second raises ValueError."""
    with pytest.raises(ValueError):
        HaloInfiniteClient(session, "spartan", "clearance", requests_per_second=0)
    with pytest.raises(ValueError):
        HaloInfiniteClient(session, "spartan", "clearance", requests_per_second=-1)


def test_client_tokens(client: HaloInfiniteClient):
    """Test that the client tokens can be set and retrieved."""
    assert client.spartan_token == "spartan"
    assert client.clearance_token == "clearance"
    client.spartan_token = "new_spartan"
    client.clearance_token = "new_clearance"
    assert client.spartan_token == "new_spartan"
    assert client.clearance_token == "new_clearance"


@pytest.mark.asyncio
async def test_client_requests_per_second_multiple_services(
    client: HaloInfiniteClient,
):
    """Test that requests per second is applied per authority."""
    tasks = []
    authorities = [
        "discovery-infiniteugc.svc.halowaypoint.com",
        "economy.svc.halowaypoint.com",
        "gamecms-hacs.svc.halowaypoint.com",
        "profile.svc.halowaypoint.com",
        "skill.svc.halowaypoint.com",
        "stats.svc.halowaypoint.com",
    ]
    for _ in range(3):
        for authority in authorities:
            tasks.append(client._get(authority, ""))

    t0 = time.time()
    await asyncio.gather(*tasks)
    t1 = time.time()
    assert t1 - t0 <= 1
