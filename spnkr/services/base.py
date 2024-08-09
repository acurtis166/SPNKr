"""Base service class."""

from typing import TYPE_CHECKING, TypeAlias

from aiolimiter import AsyncLimiter

if TYPE_CHECKING:
    from aiohttp import ClientResponse, ClientSession
    from aiohttp_client_cache.response import CachedResponse
    from aiohttp_client_cache.session import CachedSession

Response: TypeAlias = "ClientResponse | CachedResponse"
Session: TypeAlias = "ClientSession | CachedSession"


class BaseService:
    """Base service class. Handles initialization and rate limiting requests."""

    def __init__(self, session: Session, requests_per_second: int = 5) -> None:
        """Initialize a service.

        Args:
            session: The authenticated aiohttp session to use.
            requests_per_second: The rate limit to use.
        """
        self._session = session
        # Setting the max rate to 1 disallows bursts.
        self._rate_limiter = AsyncLimiter(1, 1 / requests_per_second)

    async def _get(self, url: str, **kwargs) -> Response:
        """Make a GET request to `url` and return the response."""
        response = await self._session.get(url, **kwargs)
        if not hasattr(response, "from_cache"):
            # Only rate limit non-cached responses.
            await self._rate_limiter.acquire()
        response.raise_for_status()
        return response
