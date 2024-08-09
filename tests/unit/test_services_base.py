"""Test BaseService."""

import time
from unittest.mock import AsyncMock

import pytest

from spnkr.services.base import BaseService


@pytest.fixture
def service(session):
    return BaseService(session)


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
async def test_get_cached_bypass_rate_limiter(
    session, service: BaseService, cached_response
):
    """Test that _get bypasses the rate limiter if the response is from cache."""
    session.get.return_value = cached_response
    service._rate_limiter = AsyncMock()
    await service._get("url")
    assert not service._rate_limiter.acquire.called
