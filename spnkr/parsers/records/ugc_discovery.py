"""Parsing functions for the "ugc_discovery" authority."""

from typing import Any, NamedTuple


class AssetRecord(NamedTuple):
    """A game asset, such as a map or game mode.

    Attributes:
        name: The asset's name.
        description: The asset's description.
        asset_id: The asset's GUID.
        version_id: The asset's version GUID.
        plays_recent: The number of times the asset has been played recently.
        plays_all_time: The number of times the asset has been played in total.
        average_rating: The asset's average rating.
        number_of_ratings: The number of ratings the asset has received.
    """

    name: str
    description: str
    asset_id: str
    version_id: str
    plays_recent: int
    plays_all_time: int
    average_rating: float
    number_of_ratings: int


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
