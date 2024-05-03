"""Economy/customization data services."""

from typing import Literal

from ..models.economy import PlayerCustomization
from ..xuid import wrap_xuid
from .base import BaseService

_HOST = "https://economy.svc.halowaypoint.com:443"


class EconomyService(BaseService):
    """Economy/customization data services."""

    async def get_player_customization(
        self,
        xuid: str | int,
        view_type: Literal["public", "private"] = "public",
    ) -> PlayerCustomization:
        """Get the customization selections for a player.

        Args:
            xuid: The Xbox Live ID of the player to retrieve data for.
            view_type: Use "public" when requesting customization for players
                other than yourself. The "private" view type only applies to the
                authenticated player making the request and might include data
                not visible using the "public" view type.

        Returns:
            The player's customization selections.
        """
        url = f"{_HOST}/hi/players/{wrap_xuid(xuid)}/customization"
        params = {"view": view_type}
        return PlayerCustomization(**await self._get_json(url, params=params))
