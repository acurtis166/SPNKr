"""Test the SPNKr API client."""

import asyncio
import time

import pytest

from spnkr.client import HaloInfiniteClient


@pytest.fixture
def client(session):
    return HaloInfiniteClient(
        session=session,
        spartan_token="spartan",
        clearance_token="clearance",
        max_retries=5,
    )


def test_client_invalid_requests_per_second(session):
    """Test that initializing the client with invalid requests_per_second raises ValueError."""
    with pytest.raises(ValueError):
        HaloInfiniteClient(
            session=session,
            spartan_token="spartan",
            clearance_token="clearance",
            requests_per_second=0,
        )
    with pytest.raises(ValueError):
        HaloInfiniteClient(
            session=session,
            spartan_token="spartan",
            clearance_token="clearance",
            requests_per_second=-1,
        )


def test_client_no_session():
    """Test that client can be initialized without a session."""
    client = HaloInfiniteClient(spartan_token="spartan", clearance_token="clearance")
    assert client._session is None


def test_client_session_without_context_manager():
    """Test that accessing session without context manager raises RuntimeError."""
    client = HaloInfiniteClient(spartan_token="spartan", clearance_token="clearance")
    with pytest.raises(RuntimeError):
        _ = client.session


def test_client_tokens(client: HaloInfiniteClient):
    """Test that the client tokens can be set and retrieved."""
    assert client.spartan_token == "spartan"
    client.spartan_token = "new_spartan"
    assert client.spartan_token == "new_spartan"


@pytest.mark.asyncio
async def test_client_as_context_manager():
    """Test that client can be used as an async context manager."""
    async with HaloInfiniteClient(
        spartan_token="spartan", clearance_token="clearance"
    ) as client:
        assert client.session is not None
        assert not client.session.closed


@pytest.mark.asyncio
async def test_client_as_context_manager_with_external_session(session):
    """Test that external session is not closed when using context manager."""
    async with HaloInfiniteClient(
        session=session, spartan_token="spartan", clearance_token="clearance"
    ) as client:
        assert client.session is session


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
