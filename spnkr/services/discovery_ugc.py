"""User-generated content discovery data services."""

from typing import Any
from uuid import UUID

from ..models.discovery_ugc import Map, MapModePair, Playlist, UgcGameVariant
from .base import BaseService

_HOST = "https://discovery-infiniteugc.svc.halowaypoint.com:443"


class DiscoveryUgcService(BaseService):
    """User-generated content discovery data services."""

    async def _get_asset(
        self, asset_type: str, asset_id: str | UUID, version_id: str | UUID
    ) -> dict[str, Any]:
        url = f"{_HOST}/hi/{asset_type}/{asset_id}/versions/{version_id}"
        return await self._get(url)

    async def get_ugc_game_variant(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> UgcGameVariant:
        """Get details about a game mode.

        Args:
            asset_id: The asset ID of the game variant.
            version_id: The version ID of the game variant.

        Returns:
            The game variant details.
        """
        data = await self._get_asset("ugcGameVariants", asset_id, version_id)
        return UgcGameVariant(**data)

    async def get_map_mode_pair(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> MapModePair:
        """Get details about a map mode pair.

        Args:
            asset_id: The asset ID of the map mode pair.
            version_id: The version ID of the map mode pair.

        Returns:
            The map mode pair details.
        """
        data = await self._get_asset("mapModePairs", asset_id, version_id)
        return MapModePair(**data)

    async def get_map(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> Map:
        """Get details about a map.

        Args:
            asset_id: The asset ID of the map.
            version_id: The version ID of the map.

        Returns:
            The map details.
        """
        data = await self._get_asset("maps", asset_id, version_id)
        return Map(**data)

    async def get_playlist(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> Playlist:
        """Get details about a playlist.

        Args:
            asset_id: The asset ID of the playlist.
            version_id: The version ID of the playlist.

        Returns:
            The playlist details.
        """
        data = await self._get_asset("playlists", asset_id, version_id)
        return Playlist(**data)
