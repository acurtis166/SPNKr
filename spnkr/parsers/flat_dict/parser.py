from dataclasses import dataclass
from typing import Any, Callable

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
from . import skill, stats, ugc_discovery


@dataclass(frozen=True)
class FlatDictParser:
    """Parse Halo Infinite API responses into flattened dict records.

    Args:
        json_loads: Callable to deserialize JSON data into a Python object.
            Defaults to `None`, which uses the default `json.loads` function.
    """

    json_loads: Callable | None = None

    async def parse_match_skill(
        self, resp: MatchSkillResponse
    ) -> list[dict[str, Any]]:
        """Parse a "get match skill" response into flat dict records."""
        data = await resp.json(self.json_loads)
        return skill.parse_match_skill(data)

    async def parse_playlist_csr(
        self, resp: PlaylistCsrResponse
    ) -> list[dict[str, Any]]:
        """Parse a "get playlist csr" response into flat dict records."""
        data = await resp.json(self.json_loads)
        return skill.parse_playlist_csr(data)

    async def parse_match_count(
        self, resp: MatchCountResponse
    ) -> dict[str, Any]:
        """Parse a "get match count" response into a flat dict record."""
        data = await resp.json(self.json_loads)
        return stats.parse_match_count(data)

    async def parse_match_history(
        self, resp: MatchHistoryResponse
    ) -> list[dict[str, Any]]:
        """Parse a "get match history" response into flat dict records."""
        data = await resp.json(self.json_loads)
        return stats.parse_match_history(data)

    async def parse_match_info(
        self, resp: MatchStatsResponse
    ) -> dict[str, Any]:
        """Parse a "get match stats" response to retrieve match information."""
        data = await resp.json(self.json_loads)
        return stats.parse_match_info(data)

    async def parse_team_core_stats(
        self, resp: MatchStatsResponse
    ) -> list[dict[str, Any]]:
        """Parse a "get match stats" response into team core stat records."""
        data = await resp.json(self.json_loads)
        return stats.parse_team_core_stats(data)

    async def parse_player_core_stats(
        self, resp: MatchStatsResponse
    ) -> list[dict[str, Any]]:
        """Parse a "get match stats" response into player core stat records."""
        data = await resp.json(self.json_loads)
        return stats.parse_player_core_stats(data)

    async def parse_player_medals(
        self, resp: MatchStatsResponse
    ) -> list[dict[str, Any]]:
        """Parse a "get match stats" response into player medal records."""
        data = await resp.json(self.json_loads)
        return stats.parse_player_medals(data)

    async def parse_map_mode_pair(
        self, resp: MapModePairResponse
    ) -> dict[str, Any]:
        """Parse a "get map mode pair" response into a flat dict record."""
        data = await resp.json(self.json_loads)
        return ugc_discovery.parse_asset(data)

    async def parse_map(self, resp: MapResponse) -> dict[str, Any]:
        """Parse a "get map" response into a flat dict record."""
        data = await resp.json(self.json_loads)
        return ugc_discovery.parse_asset(data)

    async def parse_playlist(self, resp: PlaylistResponse) -> dict[str, Any]:
        """Parse a "get playlist" response into a flat dict record."""
        data = await resp.json(self.json_loads)
        return ugc_discovery.parse_asset(data)

    async def parse_game_variant(
        self, resp: UgcGameVariantResponse
    ) -> dict[str, Any]:
        """Parse a "get ugc game variant" response into a flat dict record."""
        data = await resp.json(self.json_loads)
        return ugc_discovery.parse_asset(data)
