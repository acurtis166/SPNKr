"""Base service class."""

from typing import Any

from aiolimiter import AsyncLimiter

try:
    from aiohttp_client_cache.response import CachedResponse
except ImportError:
    CachedResponse = None

from spnkr.session import Response, Session


def _create_limiter(rate_per_second: int) -> AsyncLimiter:
    """Return an AsyncLimiter with the given rate per second."""
    # Setting the max rate to 1 disallows bursts.
    return AsyncLimiter(1, 1 / rate_per_second)


def _is_cached_response(response: Response) -> bool:
    """Return `True` if the response is a cached response."""
    return CachedResponse is not None and isinstance(response, CachedResponse)


class BaseService:
    """Base service class. Handles initialization and rate limiting requests."""

    def __init__(
        self, session: Session, requests_per_second: int | None = 5
    ) -> None:
        """Initialize a service.

        Args:
            session: The authenticated aiohttp session to use.
            requests_per_second: The rate limit to use. Set to None to disable
                rate limiting.
        """
        self._session = session
        self._rate_limiter = None
        if requests_per_second is not None:
            self._rate_limiter = _create_limiter(requests_per_second)

    async def _get(self, url: str, **kwargs) -> Response:
        """Make a GET request to `url` and return the response."""
        response = await self._session.get(url, **kwargs)
        if not _is_cached_response(response) and self._rate_limiter is not None:
            # Only rate limit non-cached responses.
            await self._rate_limiter.acquire()
        response.raise_for_status()
        return response

    async def _get_json(self, url: str, **kwargs) -> Any:
        """Make a GET request to `url` and return the decoded JSON response."""
        response = await self._get(url, **kwargs)
        return await response.json()

    async def _get_bytes(self, url: str, **kwargs) -> bytes:
        """Make a GET request to `url` and return the response content."""
        response = await self._get(url, **kwargs)
        return await response.read()
