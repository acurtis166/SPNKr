"""Test HTTP client logic."""

import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest
from aiohttp import ClientConnectionError, ClientResponseError
from aiolimiter import AsyncLimiter

from spnkr.errors import (
    APIAuthenticationError,
    APIAuthorizationError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
)
from spnkr.http_helpers import get_delay_seconds, handle_api_error, send_api_request


@pytest.fixture
def limiter():
    return AsyncLimiter(max_rate=5, time_period=1)


@pytest.mark.parametrize(
    "error_type,status_code",
    [
        (ClientConnectionError, None),
        (APIServerError, 500),
        (APIRateLimitError, 429),
    ],
)
@pytest.mark.asyncio
async def test_retry_on_retryable_errors(session, limiter, error_type, status_code):
    """Test that send_api_request retries on transient errors."""

    if error_type == ClientConnectionError:
        failures = [
            ClientConnectionError("Connection failed"),
            ClientConnectionError("Connection failed"),
        ]
    else:
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

    success_response = AsyncMock()
    success_response.headers = {}

    def raise_for_status_success():
        pass

    success_response.raise_for_status = raise_for_status_success

    # Mock session.request (not session.get)
    session.request = AsyncMock()
    session.request.side_effect = failures + [success_response]

    with patch("asyncio.sleep", new_callable=AsyncMock):
        result = await send_api_request(
            session,
            "GET",
            "http://authority/endpoint",
            "spartan",
            "clearance",
            max_retries=3,
            limiter=limiter,
        )
        assert result == success_response
        assert session.request.call_count == 3


def test_get_delay_seconds_with_numeric_retry_after():
    """Test that get_delay_seconds parses numeric Retry-After headers correctly."""
    response = AsyncMock()
    response.headers = {"Retry-After": "2"}

    delay = get_delay_seconds(response, attempt=0)
    assert delay == 2


def test_get_delay_seconds_with_date_format_retry_after():
    """Test that get_delay_seconds parses HTTP date Retry-After headers."""
    response = AsyncMock()
    future_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=5)
    date_str = future_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers = {"Retry-After": date_str}

    delay = get_delay_seconds(response, attempt=0)
    assert 4 <= delay <= 6


def test_get_delay_seconds_fallback_to_exponential_backoff():
    """Test that get_delay_seconds falls back to exponential backoff if header is invalid."""
    response = AsyncMock()
    response.headers = {"Retry-After": "invalid-format"}

    delay = get_delay_seconds(response, attempt=2)
    assert 4 <= delay <= 4.4


def test_get_delay_seconds_no_header():
    """Test that get_delay_seconds uses exponential backoff when no header is present."""
    response = AsyncMock()
    response.headers = {}

    delay = get_delay_seconds(response, attempt=1)
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
async def test_no_retry_on_client_errors(session, limiter, status_code, error_class):
    """Test that send_api_request does not retry on permanent client errors (401, 403, 404)."""

    error_response = AsyncMock()
    error_response.status = status_code
    error_response.message = f"Error {status_code}"
    error_response.headers = {}

    def raise_for_status():
        raise ClientResponseError(
            request_info=Mock(),
            history=(),
            status=status_code,
            message=f"Error {status_code}",
        )

    error_response.raise_for_status = raise_for_status

    session.request = AsyncMock(return_value=error_response)

    with pytest.raises(error_class):
        await send_api_request(
            session,
            "GET",
            "http://authority/endpoint",
            "spartan",
            "clearance",
            max_retries=3,
            limiter=limiter,
        )

    assert session.request.call_count == 1


@pytest.mark.asyncio
async def test_exhaust_retries_then_raise(session, limiter):
    """Test that send_api_request raises after exhausting retries."""

    session.request = AsyncMock(side_effect=ClientConnectionError("Connection failed"))

    with patch("asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(ClientConnectionError):
            await send_api_request(
                session,
                "GET",
                "http://authority/endpoint",
                "spartan",
                "clearance",
                max_retries=2,
                limiter=limiter,
            )

        assert session.request.call_count == 3


@pytest.mark.parametrize(
    "status_code,error_class",
    [
        (401, APIAuthenticationError),
        (403, APIAuthorizationError),
        (404, APINotFoundError),
        (429, APIRateLimitError),
        (500, APIServerError),
    ],
)
def test_handle_api_error(status_code, error_class):
    """Test that handle_api_error raises appropriate error classes."""
    error = ClientResponseError(
        request_info=Mock(),
        history=(),
        status=status_code,
        message=f"Error {status_code}",
    )

    with pytest.raises(error_class):
        handle_api_error(error)
