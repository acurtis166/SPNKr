"""API response wrappers."""

import json
from dataclasses import dataclass
from typing import Any, Callable, Protocol

from aiohttp import ClientResponse


@dataclass(frozen=True)
class _DictResponse:
    """Base class for wrapping API responses."""

    response: ClientResponse

    async def json(self, loads: Callable | None = None) -> dict[str, Any]:
        """Return the response as JSON.

        Args:
            loads: A custom JSON decoder to use when parsing responses.
        """
        return await self.response.json(loads=loads or json.loads)


class MapModePairResponse(_DictResponse):
    pass


class MapResponse(_DictResponse):
    pass


class MatchCountResponse(_DictResponse):
    pass


class MatchHistoryResponse(_DictResponse):
    pass


class MatchSkillResponse(_DictResponse):
    pass


class MatchStatsResponse(_DictResponse):
    pass


class PlaylistResponse(_DictResponse):
    pass


class UgcGameVariantResponse(_DictResponse):
    pass


class PlaylistCsrResponse(_DictResponse):
    pass
