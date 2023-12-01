"""Game content management data services."""

from typing import Any

from .base import BaseService

_HOST = "https://gamecms-hacs.svc.halowaypoint.com"


class GameCmsHacsService(BaseService):
    """Game content management data services."""

    async def get_medal_metadata(self) -> dict[str, Any]:
        """Get details for all medals obtainable in the game.

        Parsers:
            - [MedalMetadata][spnkr.parsers.pydantic.gamecms_hacs.MedalMetadata]
            - [parse_medal_metadata][spnkr.parsers.records.gamecms_hacs.parse_medal_metadata]

        Returns:
            The medal metadata.
        """
        url = f"{_HOST}/hi/Waypoint/file/medals/metadata.json"
        return await self._get(url)
