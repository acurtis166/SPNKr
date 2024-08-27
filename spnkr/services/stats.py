"""Stats data services."""

import warnings
from typing import Literal
from uuid import UUID

from spnkr.models.refdata import GameVariantCategory
from spnkr.models.stats import (
    MatchCount,
    MatchHistory,
    MatchStats,
    ServiceRecord,
)
from spnkr.responses import JsonResponse
from spnkr.services.base import BaseService
from spnkr.xuid import wrap_xuid_or_gamertag

_HOST = "https://halostats.svc.halowaypoint.com:443"
_VALID_SERVICE_RECORD_FILTER_SETS = [
    {"season_id"},
    {"season_id", "game_variant_category"},
    {"season_id", "game_variant_category", "playlist_asset_id"},
    {"season_id", "game_variant_category", "is_ranked"},
    {"season_id", "playlist_asset_id"},
    {"game_variant_category"},
    {"game_variant_category", "is_ranked"},
]


class StatsService(BaseService):
    """Stats data services."""

    async def get_match_count(self, player: str | int) -> JsonResponse[MatchCount]:
        """Get match counts across different game experiences for a player.

        The counts returned are for custom matches, matchmade matches, local
        matches, and total matches.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".

        Returns:
            The match counts.
        """
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        url = f"{_HOST}/hi/players/{xuid_or_gamertag}/matches/count"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: MatchCount(**data))

    async def get_service_record(
        self,
        player: str | int,
        match_type: Literal["matchmade", "custom", "local"] = "matchmade",
        season_id: str | None = None,
        game_variant_category: GameVariantCategory | int | None = None,
        is_ranked: bool | None = None,
        playlist_asset_id: str | UUID | None = None,
    ) -> JsonResponse[ServiceRecord]:
        """Get a service record for a player. Summarizes player stats.

        Note that filters (`season_id`, `game_variant_category`, `is_ranked`,
        and `playlist_asset_id`) are only applicable to "matchmade"
        `match_type`. A warning is issued and the filters are ignored if they
        are provided for a non-matchmade `match_type`.

        Filters must be combined appropriately. The following are valid:
        - `season_id`
        - `season_id`, `game_variant_category`
        - `season_id`, `game_variant_category`, `playlist_asset_id`
        - `season_id`, `game_variant_category`, `is_ranked`
        - `season_id`, `playlist_asset_id`
        - `game_variant_category`
        - `game_variant_category`, `is_ranked`

        To collect possible values for the filter arguments, look at the
        "subqueries" attribute of an unfiltered service record response.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".
            match_type: The type of games to include in the service record.
                One of "matchmade", "custom", or "local".
            season_id: The season ID to get service record for. Optional.
            game_variant_category: The game variant category to filter service
                record data. See `spnkr.parsers.refdata.GameVariantCategory` for
                human-readable values. Optional.
            is_ranked: Filter for ranked or unranked games. Optional.
            playlist_asset_id: Filter for a specific playlist with its asset ID.
                Optional.

        Returns:
            The service record for the player with the given filters.

        Raises:
            ValueError: If `match_type` is not one of "matchmade", "custom", or
                "local".
            ValueError: If filter arguments are inappropriately combined.
        """
        if match_type.lower() not in ("matchmade", "custom", "local"):
            raise ValueError(f"Invalid match type: {match_type}")
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        endpoint = f"/hi/players/{xuid_or_gamertag}/{match_type}/servicerecord"
        url = f"{_HOST}{endpoint}"
        filters = {
            "season_id": season_id,
            "game_variant_category": game_variant_category,
            "is_ranked": is_ranked,
            "playlist_asset_id": playlist_asset_id,
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        if match_type.lower() != "matchmade" and filters:
            warnings.warn(
                "Service record filters are only applicable to matchmade games."
            )
            filters = {}
        if filters and set(filters) not in _VALID_SERVICE_RECORD_FILTER_SETS:
            valid = "\n".join(str(s) for s in _VALID_SERVICE_RECORD_FILTER_SETS)
            raise ValueError(
                f"Invalid filter combination: {filters}. Options:\n{valid}"
            )
        params = {k.replace("_", ""): str(v) for k, v in filters.items()}
        resp = await self._get(url, params=params)
        return JsonResponse(resp, lambda data: ServiceRecord(**data))

    async def get_match_history(
        self,
        player: str | int,
        start: int = 0,
        count: int = 25,
        match_type: Literal["all", "matchmaking", "custom", "local"] = "all",
    ) -> JsonResponse[MatchHistory]:
        """Request a batch of matches from a player's match history.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".
            start: Index of the first match to request, starting at 0.
            count: The number of matches to request. Maximum number of results
                returned is 25.
            match_type: The type of matches to return. One of "all",
                "matchmaking", "custom", or "local".

        Returns:
            The requested match history "page" of results.
        """
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        url = f"{_HOST}/hi/players/{xuid_or_gamertag}/matches"
        params = {"start": start, "count": count, "type": match_type}
        resp = await self._get(url, params=params)
        return JsonResponse(resp, lambda data: MatchHistory(**data))

    async def get_match_stats(self, match_id: str | UUID) -> JsonResponse[MatchStats]:
        """Request match details using the Halo Infinite match GUID.

        Args:
            match_id: Halo Infinite GUID identifying the match.

        Returns:
            The match details.
        """
        url = f"{_HOST}/hi/matches/{match_id}/stats"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: MatchStats(**data))
