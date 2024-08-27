"""User-generated content discovery data services."""

import datetime as dt
from typing import Iterable, Literal
from uuid import UUID

from spnkr.models.discovery_ugc import (
    AssetSearchPage,
    Film,
    Map,
    MapModePair,
    Playlist,
    UgcGameVariant,
)
from spnkr.responses import JsonResponse
from spnkr.services.base import BaseService

_HOST = "https://discovery-infiniteugc.svc.halowaypoint.com:443"
_SortProperty = Literal[
    "name",
    "likes",
    "bookmarks",
    "plays_recent",
    "number_of_objects",
    "date_created_utc",
    "date_modified_utc",
    "date_published_utc",
    "plays_all_time",
    "parent_asset_count",
    "average_rating",
    "number_of_ratings",
]


class DiscoveryUgcService(BaseService):
    """User-generated content discovery data services."""

    async def _get_asset(
        self, asset_type: str, asset_id: str | UUID, version_id: str | UUID
    ):
        url = f"{_HOST}/hi/{asset_type}/{asset_id}/versions/{version_id}"
        return await self._get(url)

    async def get_ugc_game_variant(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> JsonResponse[UgcGameVariant]:
        """Get details about a game mode.

        Args:
            asset_id: The asset ID of the game variant.
            version_id: The version ID of the game variant.

        Returns:
            The game variant details.
        """
        resp = await self._get_asset("ugcGameVariants", asset_id, version_id)
        return JsonResponse(resp, lambda data: UgcGameVariant(**data))

    async def get_map_mode_pair(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> JsonResponse[MapModePair]:
        """Get details about a map mode pair.

        Args:
            asset_id: The asset ID of the map mode pair.
            version_id: The version ID of the map mode pair.

        Returns:
            The map mode pair details.
        """
        resp = await self._get_asset("mapModePairs", asset_id, version_id)
        return JsonResponse(resp, lambda data: MapModePair(**data))

    async def get_map(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> JsonResponse[Map]:
        """Get details about a map.

        Args:
            asset_id: The asset ID of the map.
            version_id: The version ID of the map.

        Returns:
            The map details.
        """
        resp = await self._get_asset("maps", asset_id, version_id)
        return JsonResponse(resp, lambda data: Map(**data))

    async def get_playlist(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> JsonResponse[Playlist]:
        """Get details about a playlist.

        Args:
            asset_id: The asset ID of the playlist.
            version_id: The version ID of the playlist.

        Returns:
            The playlist details.
        """
        resp = await self._get_asset("playlists", asset_id, version_id)
        return JsonResponse(resp, lambda data: Playlist(**data))

    async def search_assets(
        self,
        start: int = 0,
        count: int = 25,
        sort: _SortProperty = "plays_recent",
        order: Literal["asc", "desc"] = "desc",
        asset_kind: Literal["map", "prefab", "ugc_game_variant"] | None = None,
        term: str | None = None,
        tags: Iterable[str] | None = None,
        author: str | None = None,
        average_rating_min: float | None = None,
        from_date_created_utc: dt.datetime | dt.date | None = None,
        to_date_created_utc: dt.datetime | dt.date | None = None,
        from_date_modified_utc: dt.datetime | dt.date | None = None,
        to_date_modified_utc: dt.datetime | dt.date | None = None,
        from_date_published_utc: dt.datetime | dt.date | None = None,
        to_date_published_utc: dt.datetime | dt.date | None = None,
    ) -> JsonResponse[AssetSearchPage]:
        """Search for map, mode, and prefab assets.

        Args:
            start: Index of the first result to return, starting at 0.
            count: Count of results to return. Must be between 1 and 101.
            sort: Property by which to sort the results. Must be one of the
                following: "name", "likes", "bookmarks", "plays_recent",
                "number_of_objects", "date_created_utc", "date_modified_utc",
                "date_published_utc", "plays_all_time", "parent_asset_count",
                "average_rating", "number_of_ratings". Defaults to
                "plays_recent".
            order: Pass "asc" for ascending or "desc" for descending.
            asset_kind: Type of asset to be searched. Optional. If a value is
                provided, it must be be one of the following: "map", "prefab",
                "ugc_game_variant". By default, no filter is applied.
            term: Search term. Optional.
            tags: List of tags. Multiple tags are applied with an OR operator.
                Optional.
            author: Author ID. Valid values would be in one of the following
                formats: "xuid(<xuid>)", "aaid(<aaid>)", or "atui(<atui>)",
                where <xuid> is a 16-digit Xbox user ID, <aaid> is a UUID, and
                <atui> is a pair of UUIDs separated by a period. Optional.
            average_rating_min: Minimum average rating between 0 and 5.
                Optional.
            from_date_created_utc: Minimum date created. Optional.
            to_date_created_utc: Maximum date created. Optional.
            from_date_modified_utc: Minimum date modified. Optional.
            to_date_modified_utc: Maximum date modified. Optional.
            from_date_published_utc: Minimum date published. Optional.
            to_date_published_utc: Maximum date published. Optional.

        Returns:
            A page of up to `count` search results.
        """
        if count < 1 or count > 101:
            raise ValueError("`count` must be between 1 and 101.")
        url = f"{_HOST}/hi/search"
        params = {
            "start": start,
            "count": count,
            "sort": sort.replace("_", ""),
            "order": order,
        }
        if asset_kind is not None:
            params["assetKind"] = asset_kind.replace("_", "")
        if term is not None:
            params["term"] = term
        if tags is not None:
            params["tags"] = [tags] if isinstance(tags, str) else list(tags)
        if author is not None:
            params["author"] = author
        if average_rating_min is not None:
            params["averageRatingMin"] = average_rating_min
        if from_date_created_utc is not None:
            params["fromDateCreatedUtc"] = from_date_created_utc.isoformat()
        if to_date_created_utc is not None:
            params["toDateCreatedUtc"] = to_date_created_utc.isoformat()
        if from_date_modified_utc is not None:
            params["fromDateModifiedUtc"] = from_date_modified_utc.isoformat()
        if to_date_modified_utc is not None:
            params["toDateModifiedUtc"] = to_date_modified_utc.isoformat()
        if from_date_published_utc is not None:
            params["fromDatePublishedUtc"] = from_date_published_utc.isoformat()
        if to_date_published_utc is not None:
            params["toDatePublishedUtc"] = to_date_published_utc.isoformat()
        resp = await self._get(url, params=params)
        return JsonResponse(resp, lambda data: AssetSearchPage(**data))

    async def get_film_by_match_id(self, match_id: str | UUID) -> JsonResponse[Film]:
        """Get metadata and download information for a film.

        Args:
            match_id: The match ID of the film.

        Returns:
            The film details.
        """
        url = f"{_HOST}/hi/films/matches/{match_id}/spectate"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: Film(**data))
