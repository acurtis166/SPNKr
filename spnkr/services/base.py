"""Base service class."""

from typing import Any

from aiohttp import ClientSession
from aiolimiter import AsyncLimiter


def _create_limiter(rate_per_second: int) -> AsyncLimiter:
    """Return an AsyncLimiter with the given rate per second."""
    # Setting the max rate to 1 disallows bursts.
    return AsyncLimiter(1, 1 / rate_per_second)


class BaseService:
    """Base service class. Handles initialization and rate limiting requests."""

    def __init__(
        self, session: ClientSession, requests_per_second: int | None = 5
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

    async def _get(self, url: str, **kwargs) -> Any:
        """Make a GET request to `url` and return the decoded JSON response."""
        if self._rate_limiter is None:
            response = await self._session.get(url, **kwargs)
        else:
            async with self._rate_limiter:
                response = await self._session.get(url, **kwargs)
        response.raise_for_status()
        return await response.json()
