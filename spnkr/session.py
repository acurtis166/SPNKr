"""Protocols for async client session and response."""

from typing import Any, Protocol

from aiohttp.client import _RequestContextManager
from aiohttp.typedefs import DEFAULT_JSON_DECODER, JSONDecoder
from multidict import CIMultiDict


class Response(Protocol):
    """Protocol for async client response based on aiohttp.ClientResponse."""

    async def json(
        self,
        *,
        encoding: str | None = None,
        loads: JSONDecoder = DEFAULT_JSON_DECODER,
        content_type: str | None = "application/json",
    ) -> Any:
        ...

    async def read(self) -> bytes:
        ...

    def raise_for_status(self) -> None:
        ...


class Session(Protocol):
    """Protocol for async client session based on aiohttp.ClientSession."""

    @property
    def headers(self) -> CIMultiDict:
        ...

    def get(self, url: str, **kwargs) -> _RequestContextManager:
        ...
