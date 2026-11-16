"""Test BaseService."""

import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest
from aiohttp import ClientConnectionError, ClientResponseError

from spnkr.errors import (
    APIAuthenticationError,
    APIAuthorizationError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
)
from spnkr.services.base import BaseService, _get_delay_seconds


@pytest.fixture
def service(session):
    return BaseService(session, max_retries=3)


@pytest.mark.asyncio
async def test_rate_limiter(service: BaseService):
    """Test that the rate limiter limits requests as expected."""
    import time

    t0 = time.time()
    # Use 6 requests due to the default rate of 5 requests per second.
    for _ in range(6):
        await service._get("url")
    t1 = time.time()
    assert t1 - t0 >= 1


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.asyncio
async def test_get_cached_bypass_rate_limiter(
    session, service: BaseService, cached_response
):
    """Test that _get bypasses the rate limiter if the response is from cache."""
    session.get.return_value = cached_response
    service._rate_limiter = AsyncMock()
    await service._get("url")
    assert not service._rate_limiter.acquire.called


@pytest.mark.parametrize(
    "error_type,status_code",
    [
        (ClientConnectionError, None),
        (APIServerError, 500),
        (APIRateLimitError, 429),
    ],
)
@pytest.mark.asyncio
async def test_retry_on_retryable_errors(session, error_type, status_code):
    """Test that _get retries on transient errors."""
    service = BaseService(session, max_retries=3)

    # For network errors, we pass exceptions directly
    if error_type == ClientConnectionError:
        failures = [
            ClientConnectionError("Connection failed"),
            ClientConnectionError("Connection failed"),
        ]
    else:
        # For API errors, create mock responses that raise
        error_response = AsyncMock()
        error_response.status = status_code
        error_response.message = f"Error {status_code}"
        error_response.headers = {}

        def create_error_raiser(status):
            def raise_error():
                raise ClientResponseError(
                    request_info=Mock(),
                    history=(),
                    status=status,
                    message=f"Error {status}",
                )

            return raise_error

        error_response.raise_for_status = create_error_raiser(status_code)
        failures = [error_response, error_response]

    # Create success response
    success_response = AsyncMock()
    success_response.headers = {}

    def raise_for_status_success():
        pass

    success_response.raise_for_status = raise_for_status_success

    # Set up side effects: fail twice, succeed on third attempt
    session.get.side_effect = failures + [success_response]

    with patch("asyncio.sleep", new_callable=AsyncMock):
        result = await service._get("url")
        assert result == success_response
        assert session.get.call_count == 3


def test_get_delay_seconds_with_numeric_retry_after():
    """Test that _get_delay_seconds parses numeric Retry-After headers correctly."""
    response = AsyncMock()
    response.headers = {"Retry-After": "2"}

    delay = _get_delay_seconds(response, attempt=0)
    assert delay == 2


def test_get_delay_seconds_with_date_format_retry_after():
    """Test that _get_delay_seconds parses HTTP date Retry-After headers."""
    response = AsyncMock()
    # Create a time 5 seconds in the future
    future_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=5)
    # Format as RFC 7231 date
    date_str = future_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers = {"Retry-After": date_str}

    delay = _get_delay_seconds(response, attempt=0)
    # Should be approximately 5 seconds (allow 1 second tolerance)
    assert 4 <= delay <= 6


def test_get_delay_seconds_fallback_to_exponential_backoff():
    """Test that _get_delay_seconds falls back to exponential backoff if header is invalid."""
    response = AsyncMock()
    response.headers = {"Retry-After": "invalid-format"}

    delay = _get_delay_seconds(response, attempt=2)
    # Should use exponential backoff: 2^2 = 4 seconds (with jitter)
    assert 4 <= delay <= 4.4


def test_get_delay_seconds_no_header():
    """Test that _get_delay_seconds uses exponential backoff when no header is present."""
    from spnkr.services.base import _get_delay_seconds

    response = AsyncMock()
    response.headers = {}

    delay = _get_delay_seconds(response, attempt=1)
    # Should use exponential backoff: 2^1 = 2 seconds (with jitter)
    assert 2 <= delay <= 2.2


@pytest.mark.parametrize(
    "status_code,error_class",
    [
        (401, APIAuthenticationError),
        (403, APIAuthorizationError),
        (404, APINotFoundError),
    ],
)
@pytest.mark.asyncio
async def test_no_retry_on_client_errors(session, status_code, error_class):
    """Test that _get does not retry on permanent client errors (401, 403, 404)."""
    service = BaseService(session, max_retries=3)

    # Create mock response that raises client error
    error_response = AsyncMock()
    error_response.status = status_code
    error_response.message = f"Error {status_code}"
    error_response.headers = {}

    session.get.return_value = error_response

    # Mock raise_for_status to raise on client errors
    def raise_for_status():
        raise ClientResponseError(
            request_info=Mock(),
            history=(),
            status=status_code,
            message=f"Error {status_code}",
        )

    error_response.raise_for_status = raise_for_status

    with pytest.raises(error_class):
        await service._get("url")

    # Should only try once, no retries
    assert session.get.call_count == 1


@pytest.mark.asyncio
async def test_exhaust_retries_then_raise(session):
    """Test that _get raises after exhausting retries."""
    service = BaseService(session, max_retries=2)

    # Fail all attempts
    session.get.side_effect = ClientConnectionError("Connection failed")

    with patch("asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(ClientConnectionError):
            await service._get("url")

        # Should attempt 1 + max_retries times
        assert session.get.call_count == 3
