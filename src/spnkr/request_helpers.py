"""Parameter types and helper functions for preparing Halo Infinite API requests."""

import datetime as dt
import warnings
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable
from pathlib import Path
from typing import Any, Literal
from uuid import UUID

from spnkr.models.refdata import GameplayInteraction, GameVariantCategory

SortProperty = Literal[
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
SortOrder = Literal["asc", "desc"]
AssetKind = Literal["map", "prefab", "ugc_game_variant"]
ViewType = Literal["public", "private"]
HistoryMatchType = Literal["all", "matchmaking", "custom", "local"]
ServiceRecordMatchType = Literal["matchmade", "custom", "local"]

_VALID_SERVICE_RECORD_FILTER_SETS = [
    {"season_id"},
    {"season_id", "game_variant_category"},
    {"season_id", "game_variant_category", "playlist_asset_id"},
    {"season_id", "game_variant_category", "is_ranked"},
    {"season_id", "playlist_asset_id"},
    {"season_id", "gameplay_interaction"},
    {"game_variant_category"},
    {"game_variant_category", "is_ranked"},
]


def prepare_service_record_params(
    match_type: ServiceRecordMatchType = "matchmade",
    season_id: str | None = None,
    game_variant_category: GameVariantCategory | int | None = None,
    is_ranked: bool | None = None,
    playlist_asset_id: str | UUID | None = None,
    gameplay_interaction: GameplayInteraction | None = None,
) -> dict[str, Any]:
    filters = {
        "season_id": season_id,
        "game_variant_category": game_variant_category,
        "is_ranked": is_ranked,
        "playlist_asset_id": playlist_asset_id,
        "gameplay_interaction": gameplay_interaction,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    if match_type.lower() != "matchmade" and filters:
        warnings.warn("Service record filters are only applicable to matchmade games.")
        filters = {}
    if filters and set(filters) not in _VALID_SERVICE_RECORD_FILTER_SETS:
        valid = "\n".join(str(s) for s in _VALID_SERVICE_RECORD_FILTER_SETS)
        raise ValueError(f"Invalid filter combination: {filters}. Options:\n{valid}")

    return {k.replace("_", ""): str(v) for k, v in filters.items()}


def validate_xuids(xuids: Iterable[str | int]) -> list[str | int]:
    if isinstance(xuids, str):
        raise TypeError("`xuids` must be an iterable of XUIDs, got `str`")

    xuid_list = list(xuids)
    if not xuid_list:
        raise ValueError("`xuids` cannot be empty")

    return xuid_list


def prepare_search_asset_params(
    start: int = 0,
    count: int = 25,
    sort: SortProperty = "plays_recent",
    order: SortOrder = "desc",
    asset_kind: AssetKind | None = None,
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
) -> dict[str, Any]:
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

    return params


def get_localized_asset_kwargs(session, language: str | None) -> dict[str, Any]:
    """Build request kwargs for localized asset lookups.

    When a cached aiohttp-client-cache session is configured without
    ``include_headers=True``, requests that differ only by
    ``Accept-Language`` would otherwise share the same cache key. In that
    case we disable cache reads and writes for the request. If
    ``include_headers=True`` is enabled to cache localized variants, make
    sure authentication headers are excluded from the cache key via
    ``ignored_params`` so token rotation does not fragment the cache.
    """
    if language is None:
        return {}

    kwargs: dict[str, object] = {"headers": {"Accept-Language": language}}
    cache = getattr(session, "cache", None)
    if cache is not None and not getattr(cache, "include_headers", False):
        warnings.warn(
            "Localized Discovery UGC requests are using a cached session "
            "without include_headers=True. Caching is disabled for this "
            "request; configure aiohttp-client-cache with "
            "include_headers=True to cache Accept-Language variants "
            "safely, and exclude auth headers from the cache key via "
            "ignored_params to avoid duplicate entries when tokens "
            "change.",
            UserWarning,
            stacklevel=4,
        )
        kwargs["expire_after"] = 0
    return kwargs


def clean_season_id(season_id: str) -> str:
    """Remove the path prefix and ".json" extension from a season ID.

    For example, season "Csr/Seasons/CsrSeason5-1.json" is cleaned to
    "CsrSeason5-1".
    """
    return Path(season_id).stem


async def paginate(
    fetcher: Callable[..., Awaitable],
    start: int,
    count: int,
    limit: int | None,
    **kwargs,
) -> AsyncIterator:
    """Paginate through results from a fetcher function with optional limit."""
    current_start = start
    yielded = 0
    while True:
        # Avoid over-fetching if limit is set and remaining limit is less than count
        fetch_count = count
        if limit is not None:
            remaining = limit - yielded
            if remaining <= 0:
                break
            fetch_count = min(count, remaining)

        page = await fetcher(**kwargs, start=current_start, count=fetch_count)
        if not page.results:
            break
        for result in page.results:
            yield result
            yielded += 1
            if limit is not None and yielded >= limit:
                return
        if page.result_count < fetch_count:
            break
        current_start += fetch_count
