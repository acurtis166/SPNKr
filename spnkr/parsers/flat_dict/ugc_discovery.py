from typing import Any


def parse_asset(asset: dict[str, Any]) -> dict[str, Any]:
    """Parse game asset information from Halo Infinite API responses."""
    stats = asset["AssetStats"]
    return {
        "name": asset["PublicName"],
        "description": asset["Description"],
        "asset_id": asset["AssetId"],
        "version_id": asset["VersionId"],
        "plays_recent": stats["PlaysRecent"],
        "plays_all_time": stats["PlaysAllTime"],
        "average_rating": stats["AverageRating"],
        "number_of_ratings": stats["NumberOfRatings"],
    }
