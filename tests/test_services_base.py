"""Test BaseService."""

import time

import pytest

from spnkr.services.base import BaseService


@pytest.fixture
def service(session):
    return BaseService(session)


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
