"""Game content management data services."""

from ..models.gamecms_hacs import MedalMetadata
from .base import BaseService

_HOST = "https://gamecms-hacs.svc.halowaypoint.com"


class GameCmsHacsService(BaseService):
    """Game content management data services."""

    async def get_medal_metadata(self) -> MedalMetadata:
        """Get details for all medals obtainable in the game.

        Returns:
            The medal metadata.
        """
        data = await self._get(f"{_HOST}/hi/Waypoint/file/medals/metadata.json")
        return MedalMetadata(**data)
