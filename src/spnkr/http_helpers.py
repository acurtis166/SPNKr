"""HTTP helpers."""

import asyncio
import datetime
import random
from email.utils import parsedate_to_datetime
from typing import TYPE_CHECKING, TypeAlias

from aiohttp import ClientConnectionError, ClientError, ClientResponseError
from aiolimiter import AsyncLimiter

from spnkr.errors import (
    APIAuthenticationError,
    APIAuthorizationError,
    APIError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
)

if TYPE_CHECKING:
    from aiohttp import ClientResponse, ClientSession
    from aiohttp_client_cache.response import CachedResponse
    from aiohttp_client_cache.session import CachedSession

    from spnkr.auth.provider import TokenProvider

Response: TypeAlias = "ClientResponse | CachedResponse"
Session: TypeAlias = "ClientSession | CachedSession"


def handle_api_error(error: ClientResponseError) -> None:
    """Convert aiohttp ClientResponseError to appropriate spnkr error."""
    status = error.status
    message = error.message or str(error)

    if status == 401:
        raise APIAuthenticationError(message, status_code=status)
    elif status == 403:
        raise APIAuthorizationError(message, status_code=status)
    elif status == 404:
        raise APINotFoundError(message, status_code=status)
    elif status == 429:
        raise APIRateLimitError(message, status_code=status)
    elif 500 <= status < 600:
        raise APIServerError(message, status_code=status)
    else:
        raise APIError(message, status_code=status)


def get_delay_seconds(response, attempt: int) -> float:
    base_delay = 2**attempt
    delay = base_delay + random.uniform(0, base_delay * 0.1)

    # If the response has a Retry-After header, use it to override the delay.
    if response is not None and "Retry-After" in response.headers:
        retry_after = response.headers["Retry-After"]
        if retry_after.isdigit():
            # Try parsing as an integer (seconds)
            delay = float(int(retry_after))
        else:
            try:
                # Try parsing as an HTTP date
                retry_time = parsedate_to_datetime(retry_after)
                delay = (
                    retry_time - datetime.datetime.now(datetime.UTC)
                ).total_seconds()
            except (TypeError, ValueError):
                pass

    return max(0, delay)


async def send_api_request(
    session: Session,
    method: str,
    url: str,
    spartan_token: "str | TokenProvider",
    clearance_token: str | None,
    max_retries: int,
    limiter: AsyncLimiter,
    **kwargs,
):
    last_exception: Exception | None = None

    if isinstance(spartan_token, str):
        spartan_token_value = spartan_token
    else:
        spartan_token_value = await spartan_token.get_token()

    headers = kwargs.pop("headers", {})
    headers.setdefault("Accept", "application/json")
    headers.setdefault("x-343-authorization-spartan", spartan_token_value)
    if clearance_token is not None:
        headers.setdefault("343-clearance", clearance_token)
    kwargs["headers"] = headers

    for attempt in range(max_retries + 1):
        response = None
        try:
            response = await session.request(method, url, **kwargs)
            if not hasattr(response, "from_cache"):
                # Only rate limit non-cached responses.
                await limiter.acquire()
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                handle_api_error(e)
            return response
        except (
            ClientConnectionError,
            ClientError,
            APIServerError,
            APIRateLimitError,
        ) as e:
            last_exception = e
            if attempt < max_retries:
                delay = get_delay_seconds(response, attempt)
                await asyncio.sleep(delay)
        except APIError:
            raise

    raise last_exception  # type: ignore
