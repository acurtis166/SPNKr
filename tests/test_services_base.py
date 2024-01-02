"""Test BaseService."""

import time
from unittest.mock import AsyncMock

import pytest
from aiohttp_client_cache.response import CachedResponse

import spnkr.services.base
from spnkr.services.base import BaseService


@pytest.fixture
def service(session):
    return BaseService(session)


@pytest.fixture
def cached_response():
    return CachedResponse(
        method="GET", reason="OK", status=200, url="url", version="1.1"
    )


def test_async_limiter_set(service: BaseService):
    """Test that the async limiter is set as expected."""
    assert service._rate_limiter is not None
    assert (
        service._rate_limiter.max_rate / service._rate_limiter.time_period == 5
    )


@pytest.mark.asyncio
async def test_rate_limiter(service: BaseService):
    """Test that the rate limiter limits requests as expected."""
    t0 = time.time()
    # Use 6 requests due to the default rate of 5 requests per second.
    for _ in range(6):
        await service._get("url")
    t1 = time.time()
    assert t1 - t0 >= 1


@pytest.mark.asyncio
async def test_rate_limiter_none(service: BaseService):
    """Test that the rate limiter does not limit requests if None."""
    service._rate_limiter = None
    t0 = time.time()
    for _ in range(6):
        await service._get("url")
    t1 = time.time()
    assert t1 - t0 < 1


@pytest.mark.asyncio
async def test_get_cached_bypass_rate_limiter(
    session, service: BaseService, cached_response
):
    """Test that _get bypasses the rate limiter if the response is from cache."""
    session.get.return_value = cached_response
    service._rate_limiter = AsyncMock()
    await service._get("url")
    assert not service._rate_limiter.acquire.called


def test_is_cached_response_true(cached_response):
    """Test that _is_cached_response returns True if the response is from cache."""
    assert spnkr.services.base._is_cached_response(cached_response)


def test_is_cached_response_no_import(cached_response, monkeypatch):
    """Test that _is_cached_response returns False if the library isn't installed"""
    monkeypatch.setattr(spnkr.services.base, "CachedResponse", None)
    assert not spnkr.services.base._is_cached_response(cached_response)


def test_is_cached_response_not_cached_response(session):
    """Test that _is_cached_response returns False if the response isn't cached"""
    response = session.get("url")
    assert not spnkr.services.base._is_cached_response(response)
