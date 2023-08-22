"""Parsing functions for the "ugc_discovery" authority."""

from typing import Any, NamedTuple


class AssetRecord(NamedTuple):
    """A game asset, such as a map or game mode."""

    name: str
    """The asset's name."""
    description: str
    """The asset's description."""
    asset_id: str
    """The asset's GUID."""
    version_id: str
    """The asset's version GUID."""
    plays_recent: int
    """The number of times the asset has been played recently."""
    plays_all_time: int
    """The number of times the asset has been played in total."""
    average_rating: float
    """The asset's average rating."""
    number_of_ratings: int
    """The number of ratings the asset has received."""


def parse_asset(asset: dict[str, Any]) -> AssetRecord:
    """Parse game asset information from Halo Infinite API responses."""
    stats = asset["AssetStats"]
    return AssetRecord(
        name=asset["PublicName"],
        description=asset["Description"],
        asset_id=asset["AssetId"],
        version_id=asset["VersionId"],
        plays_recent=stats["PlaysRecent"],
        plays_all_time=stats["PlaysAllTime"],
        average_rating=stats["AverageRating"],
        number_of_ratings=stats["NumberOfRatings"],
    )
