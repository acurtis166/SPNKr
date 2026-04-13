"""Game content management data services."""

from typing import Any

from spnkr.models.gamecms_hacs import (
    CareerRewardTrack,
    CsrSeasonCalendar,
    MedalMetadata,
    OperationRewardTrack,
    SeasonCalendar,
)
from spnkr.responses import ImageResponse, JsonResponse
from spnkr.services.base import BaseService

_HOST = "https://gamecms-hacs.svc.halowaypoint.com"


class GameCmsHacsService(BaseService):
    """Game content management data services."""

    async def get_progression_file(
        self,
        relative_path: str,
    ) -> JsonResponse[dict[str, Any]]:
        """Get a raw progression file from the GameCMS service.

        Args:
            relative_path: The relative path to the progression file.

        Returns:
            The raw JSON payload for the requested progression file.
        """
        url = f"{_HOST}/hi/Progression/file/{relative_path.lstrip('/')}"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: data)

    async def get_medal_metadata(self) -> JsonResponse[MedalMetadata]:
        """Get details for all medals obtainable in the game.

        Returns:
            The medal metadata.
        """
        url = f"{_HOST}/hi/Waypoint/file/medals/metadata.json"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: MedalMetadata(**data))

    async def get_csr_season_calendar(self) -> JsonResponse[CsrSeasonCalendar]:
        """Get IDs and dates for past and current CSR seasons.

        CSR seasons represent the time periods between CSR resets.

        Returns:
            The CSR season calendar.
        """
        url = f"{_HOST}/hi/Progression/file/Csr/Calendars/CsrSeasonCalendar.json"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: CsrSeasonCalendar(**data))

    async def get_season_calendar(self) -> JsonResponse[SeasonCalendar]:
        """Get IDs and dates for past/current reward track events/operations.

        Reward tracks are the progression systems that allow players to earn
        rewards from the XP earned by playing the game.

        Returns:
            The calendar of reward tracks.
        """
        url = f"{_HOST}/hi/progression/file/calendars/seasons/seasoncalendar.json"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: SeasonCalendar(**data))

    async def get_career_reward_track(self) -> JsonResponse[CareerRewardTrack]:
        """Get details for the career rank progression reward track.

        Returns:
            The career rank reward track.
        """
        url = f"{_HOST}/hi/Progression/file/RewardTracks/CareerRanks/careerRank1.json"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: CareerRewardTrack(**data))

    async def get_operation_reward_track(
        self,
        reward_track_path: str,
    ) -> JsonResponse[OperationRewardTrack]:
        """Get details for a single operation reward track.

        Args:
            reward_track_path: The relative path to the operation reward track
                file, such as "RewardTracks/Operations/S05OpPassM01.json".

        Returns:
            The operation reward track definition.
        """
        url = f"{_HOST}/hi/Progression/file/{reward_track_path.lstrip('/')}"
        resp = await self._get(url)
        return JsonResponse(resp, lambda data: OperationRewardTrack(**data))

    async def get_image(self, relative_path: str) -> ImageResponse:
        """Get an image from the game content management service.

        Args:
            relative_path: The relative path to the image, such as
                "career_rank/ProgressWidget/272_Hero.png".

        Returns:
            The image data.
        """
        url = f"{_HOST}/hi/images/file/{relative_path.lstrip('/')}"
        return ImageResponse(await self._get(url))
