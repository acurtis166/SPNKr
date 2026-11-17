"""Test the SPNKr API client."""

import asyncio
import time
from unittest.mock import patch

import pytest

from spnkr.auth.provider import RefreshTokenProvider, StaticTokenProvider
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
        HaloInfiniteClient(spartan_token="spartan", requests_per_second=0)
    with pytest.raises(ValueError):
        HaloInfiniteClient(spartan_token="spartan", requests_per_second=-1)


def test_client_no_session():
    """Test that client can be initialized without a session."""
    client = HaloInfiniteClient(spartan_token="spartan", clearance_token="clearance")
    assert client._session is None


def test_client_session_without_context_manager():
    """Test that accessing session without context manager raises RuntimeError."""
    client = HaloInfiniteClient(spartan_token="spartan", clearance_token="clearance")
    with pytest.raises(RuntimeError):
        _ = client.session


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


class TestTokenProviderIntegration:
    @pytest.mark.asyncio
    async def test_provider_with_client_string_token(self):
        """Test that client accepts string tokens for backward compatibility."""
        client = HaloInfiniteClient(spartan_token="test_token")
        assert client.spartan_token.token == "test_token"  # type: ignore

    @pytest.mark.asyncio
    async def test_provider_with_client_static_provider(self):
        """Test that client accepts StaticTokenProvider."""
        provider = StaticTokenProvider("test_token")
        client = HaloInfiniteClient(spartan_token=provider)
        assert client.spartan_token.token == "test_token"  # type: ignore

    @pytest.mark.asyncio
    async def test_provider_with_client_refresh_provider(self):
        """Test that client accepts RefreshTokenProvider."""

        async def get_access_token():
            return "access_token"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token"),
            patch("spnkr.auth.provider.xbox.request_xsts_token"),
            patch("spnkr.auth.provider.halo.request_spartan_token"),
        ):
            provider = RefreshTokenProvider(get_access_token)
            client = HaloInfiniteClient(spartan_token=provider)
            assert client.spartan_token is provider

    @pytest.mark.asyncio
    async def test_client_converts_string_to_provider(self):
        """Test that string tokens are converted to StaticTokenProvider."""
        client = HaloInfiniteClient(spartan_token="test_token")
        assert isinstance(client.spartan_token, StaticTokenProvider)

    @pytest.mark.asyncio
    async def test_client_preserves_provider(self):
        """Test that TokenProvider instances are preserved."""

        async def get_access_token():
            return "access_token"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token"),
            patch("spnkr.auth.provider.xbox.request_xsts_token"),
            patch("spnkr.auth.provider.halo.request_spartan_token"),
        ):
            provider = RefreshTokenProvider(get_access_token)
            client = HaloInfiniteClient(spartan_token=provider)
            assert client.spartan_token is provider

    @pytest.mark.asyncio
    async def test_client_setter_creates_provider(self):
        """Test that spartan_token setter creates a new provider."""
        client = HaloInfiniteClient(spartan_token="initial_token")
        client.spartan_token = "updated_token"
        assert client.spartan_token.token == "updated_token"  # type: ignore
        assert isinstance(client.spartan_token, StaticTokenProvider)
