from dataclasses import dataclass
from typing import Any, Callable, Protocol, TypeVar

try:
    from pydantic import BaseModel
except ImportError:
    raise ImportError("You must install pydantic to use this parser.")

from ...responses import (
    MapModePairResponse,
    MapResponse,
    MatchCountResponse,
    MatchHistoryResponse,
    MatchSkillResponse,
    MatchStatsResponse,
    PlaylistCsrResponse,
    PlaylistResponse,
    UgcGameVariantResponse,
)
from .skill import MatchSkill, PlaylistCsr
from .stats import MatchCount, MatchHistory, MatchStats
from .ugc_discovery import Map, MapModePair, Playlist, UgcGameVariant

T = TypeVar("T", bound=BaseModel)


class _Response(Protocol):
    async def json(self, loads: Callable | None = None) -> dict[str, Any]:
        ...


async def _parse_response(
    resp: _Response,
    model: type[T],
    validate: bool,
    json_loads: Callable | None = None,
) -> T:
    """Parse a response into a pydantic model."""
    data = await resp.json(json_loads)
    if validate:
        return model(**data)
    return model.model_construct(values=data)


@dataclass(frozen=True)
class PydanticParser:
    """A parser for the Halo Infinite API that uses pydantic models.

    Attributes:
        validate: Whether to validate the parsed data against the model's
            constraints. Defaults to False.
        json_loads: A custom JSON decoder to use when parsing responses. If None
            is passed, the default `json.loads` will be used.
    """

    validate: bool = False
    json_loads: Callable | None = None

    async def parse_match_skill(self, resp: MatchSkillResponse) -> MatchSkill:
        """Parse a "get match skill" response into a pydantic model."""
        return await _parse_response(
            resp, MatchSkill, self.validate, self.json_loads
        )

    async def parse_playlist_csr(
        self, resp: PlaylistCsrResponse
    ) -> PlaylistCsr:
        """Parse a "get playlist CSR" response into a pydantic model."""
        return await _parse_response(
            resp, PlaylistCsr, self.validate, self.json_loads
        )

    async def parse_match_count(self, resp: MatchCountResponse) -> MatchCount:
        """Parse a "get match count" response into a pydantic model."""
        return await _parse_response(
            resp, MatchCount, self.validate, self.json_loads
        )

    async def parse_match_history(
        self, resp: MatchHistoryResponse
    ) -> MatchHistory:
        """Parse a "get match history" response into a pydantic model."""
        return await _parse_response(
            resp, MatchHistory, self.validate, self.json_loads
        )

    async def parse_match_stats(self, resp: MatchStatsResponse) -> MatchStats:
        """Parse a "get match stats" response into a pydantic model."""
        return await _parse_response(
            resp, MatchStats, self.validate, self.json_loads
        )

    async def parse_game_variant(
        self, resp: UgcGameVariantResponse
    ) -> UgcGameVariant:
        """Parse a "get UGC game variant" response into a pydantic model."""
        return await _parse_response(
            resp, UgcGameVariant, self.validate, self.json_loads
        )

    async def parse_map_mode_pair(
        self, resp: MapModePairResponse
    ) -> MapModePair:
        """Parse a "get map mode pair" response into a pydantic model."""
        return await _parse_response(
            resp, MapModePair, self.validate, self.json_loads
        )

    async def parse_map(self, resp: MapResponse) -> Map:
        """Parse a "get map" response into a pydantic model."""
        return await _parse_response(resp, Map, self.validate, self.json_loads)

    async def parse_playlist(self, resp: PlaylistResponse) -> Playlist:
        """Parse a "get playlist" response into a pydantic model."""
        return await _parse_response(
            resp, Playlist, self.validate, self.json_loads
        )
