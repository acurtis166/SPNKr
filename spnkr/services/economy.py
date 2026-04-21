"""Economy/customization data services."""

from typing import Literal

from spnkr.models.economy import PlayerCareerRank, PlayerCustomization, PlayerOperationPasses
from spnkr.responses import JsonResponse
from spnkr.services.base import BaseService
from spnkr.xuid import wrap_xuid

_HOST = "https://economy.svc.halowaypoint.com:443"


class EconomyService(BaseService):
    """Economy/customization data services."""

    async def get_player_reward_track_operations(
        self,
        xuid: str | int,
    ) -> JsonResponse[PlayerOperationPasses]:
        """Get the active and available operation reward tracks for a player.

        Args:
            xuid: The Xbox Live ID of the player to retrieve data for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", and 1234567890123456.

        Returns:
            The player's active and available operation reward tracks.
        """
        url = f"{_HOST}/hi/players/{wrap_xuid(xuid)}/rewardtracks/operations"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: PlayerOperationPasses(**data))

    async def get_player_career_rank(
        self,
        xuid: str | int,
        reward_track_id: str = "careerrank1",
    ) -> JsonResponse[PlayerCareerRank]:
        """Get the player's current progress on a career rank reward track.

        Args:
            xuid: The Xbox Live ID of the player to retrieve data for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", and 1234567890123456.
            reward_track_id: The career rank reward track identifier.

        Returns:
            The player's current career rank progress.
        """
        url = f"{_HOST}/hi/players/{wrap_xuid(xuid)}/rewardtracks/careerranks/{reward_track_id}"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: PlayerCareerRank(**data))

    async def get_player_customization(
        self,
        xuid: str | int,
        view_type: Literal["public", "private"] = "public",
    ) -> JsonResponse[PlayerCustomization]:
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
        resp = await self._get(url, params=params)
        return JsonResponse(resp, lambda data: PlayerCustomization(**data))
