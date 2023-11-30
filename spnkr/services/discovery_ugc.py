"""User-generated content discovery data services."""

from uuid import UUID

from aiohttp import ClientResponse

from .base import BaseService

_HOST = "https://discovery-infiniteugc.svc.halowaypoint.com:443"


class DiscoveryUgcService(BaseService):
    """User-generated content discovery data services."""

    async def _get_asset(
        self, asset_type: str, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        url = f"{_HOST}/hi/{asset_type}/{asset_id}/versions/{version_id}"
        return await self._get(url)

    async def get_ugc_game_variant(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a game mode.

        Args:
            asset_id: The asset ID of the game variant.
            version_id: The version ID of the game variant.

        Parsers:
            - [UgcGameVariant][spnkr.parsers.pydantic.ugc_discovery.UgcGameVariant]
            - [parse_asset][spnkr.parsers.records.ugc_discovery.parse_asset]

        Returns:
            The game variant details.
        """
        return await self._get_asset("ugcGameVariants", asset_id, version_id)

    async def get_map_mode_pair(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a map mode pair.

        Args:
            asset_id: The asset ID of the map mode pair.
            version_id: The version ID of the map mode pair.

        Parsers:
            - [MapModePair][spnkr.parsers.pydantic.ugc_discovery.MapModePair]
            - [parse_asset][spnkr.parsers.records.ugc_discovery.parse_asset]

        Returns:
            The map mode pair details.
        """
        return await self._get_asset("mapModePairs", asset_id, version_id)

    async def get_map(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a map.

        Args:
            asset_id: The asset ID of the map.
            version_id: The version ID of the map.

        Parsers:
            - [Map][spnkr.parsers.pydantic.ugc_discovery.Map]
            - [parse_asset][spnkr.parsers.records.ugc_discovery.parse_asset]

        Returns:
            The map details.
        """
        return await self._get_asset("maps", asset_id, version_id)

    async def get_playlist(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a playlist.

        Args:
            asset_id: The asset ID of the playlist.
            version_id: The version ID of the playlist.

        Parsers:
            - [Playlist][spnkr.parsers.pydantic.ugc_discovery.Playlist]
            - [parse_asset][spnkr.parsers.records.ugc_discovery.parse_asset]

        Returns:
            The playlist details.
        """
        return await self._get_asset("playlists", asset_id, version_id)
