"""Wrappers for API responses."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from aiohttp_client_cache.response import CachedResponse

T = TypeVar("T")


@dataclass(frozen=True)
class JsonResponse(Generic[T]):
    """`ClientResponse` wrapper for a JSON HTTP response."""

    response: "ClientResponse | CachedResponse"
    _parser: Callable[[Any], T]

    @property
    def from_cache(self) -> bool:
        """Whether the response is from cache or not."""
        return hasattr(self.response, "from_cache")

    async def parse(self, **kwargs) -> T:
        """Parse the response data into the appropriate response model.

        Keyword arguments are passed to [aiohttp.ClientResponse.json](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.json).
        """
        return self._parser(await self.response.json(**kwargs))


@dataclass(frozen=True)
class ImageResponse:
    """`ClientResponse` wrapper for an image HTTP response."""

    response: "ClientResponse | CachedResponse"

    @property
    def from_cache(self) -> bool:
        """Whether the response is from cache or not."""
        return hasattr(self.response, "from_cache")

    async def read(self) -> bytes:
        """Read the response content."""
        return await self.response.read()
