"""Base service class."""

import asyncio
import datetime
import random
from email.utils import parsedate_to_datetime
from typing import TYPE_CHECKING, TypeAlias, TypeVar, cast

from aiohttp import ClientConnectionError, ClientError, ClientResponseError
from aiolimiter import AsyncLimiter
from pydantic import BaseModel

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

Response: TypeAlias = "ClientResponse | CachedResponse"
Session: TypeAlias = "ClientSession | CachedSession"

T = TypeVar("T", bound=BaseModel)


def _handle_api_error(error: ClientResponseError) -> None:
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


def _get_delay_seconds(response, attempt: int) -> float:
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


class BaseService:
    """Base service class. Handles initialization and rate limiting requests."""

    def __init__(
        self, session: Session, max_retries: int = 2, requests_per_second: int = 5
    ) -> None:
        """Initialize a service.

        Args:
            session: The authenticated aiohttp session to use.
            max_retries: The maximum number of times to retry a request on failure.
            requests_per_second: The rate limit to use.
        """
        self._session = session
        self._max_retries = max(0, max_retries)
        # Setting the max rate to 1 disallows bursts.
        self._rate_limiter = AsyncLimiter(1, 1 / requests_per_second)

    async def _get(self, url: str, **kwargs) -> Response:
        """Make a GET request to `url` and return the response."""
        last_exception: Exception | None = None

        for attempt in range(self._max_retries + 1):
            response = None
            try:
                response = await self._session.get(url, **kwargs)
                if not hasattr(response, "from_cache"):
                    # Only rate limit non-cached responses.
                    await self._rate_limiter.acquire()
                try:
                    response.raise_for_status()
                except ClientResponseError as e:
                    _handle_api_error(e)
                return response
            except (
                ClientConnectionError,
                ClientError,
                APIServerError,
                APIRateLimitError,
            ) as e:
                last_exception = e
                if attempt < self._max_retries:
                    delay = _get_delay_seconds(response, attempt)
                    await asyncio.sleep(delay)
            except APIError:
                raise

        raise last_exception  # type: ignore

    async def _get_model(self, url: str, model: type[T], **kwargs) -> T:
        """Make a GET request to `url` and return the response as a `model` instance."""
        response = await self._get(url, **kwargs)
        return model.model_validate_json(await response.read())

    async def _get_model_list(self, url: str, model: type[T], **kwargs) -> list[T]:
        """Make a GET request to `url` and return the response as a list of `model` instances."""
        response = await self._get(url, **kwargs)
        return [
            model.model_validate(item) for item in cast(list, await response.json())
        ]
