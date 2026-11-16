"""Game content management data services."""

from typing import Any, cast

from spnkr.models.gamecms_hacs import (
    CareerRewardTrack,
    CsrSeasonCalendar,
    MedalMetadata,
    OperationRewardTrack,
    SeasonCalendar,
)
from spnkr.services.base import BaseService

_HOST = "https://gamecms-hacs.svc.halowaypoint.com"


class GameCmsHacsService(BaseService):
    """Game content management data services."""

    async def get_progression_file(self, relative_path: str) -> dict[str, Any]:
        """Get a raw progression file from the GameCMS service.

        Args:
            relative_path: The relative path to the progression file.

        Returns:
            The raw JSON payload for the requested progression file.
        """
        url = f"{_HOST}/hi/Progression/file/{relative_path.lstrip('/')}"
        resp = await self._get(url)
        return cast(dict[str, Any], await resp.json())

    async def get_medal_metadata(self) -> MedalMetadata:
        """Get details for all medals obtainable in the game.

        Returns:
            The medal metadata.
        """
        url = f"{_HOST}/hi/Waypoint/file/medals/metadata.json"
        return await self._get_model(url, MedalMetadata)

    async def get_csr_season_calendar(self) -> CsrSeasonCalendar:
        """Get IDs and dates for past and current CSR seasons.

        CSR seasons represent the time periods between CSR resets.

        Returns:
            The CSR season calendar.
        """
        url = f"{_HOST}/hi/Progression/file/Csr/Calendars/CsrSeasonCalendar.json"
        return await self._get_model(url, CsrSeasonCalendar)

    async def get_season_calendar(self) -> SeasonCalendar:
        """Get IDs and dates for past/current reward track events/operations.

        Reward tracks are the progression systems that allow players to earn
        rewards from the XP earned by playing the game.

        Returns:
            The calendar of reward tracks.
        """
        url = f"{_HOST}/hi/progression/file/calendars/seasons/seasoncalendar.json"
        return await self._get_model(url, SeasonCalendar)

    async def get_career_reward_track(self) -> CareerRewardTrack:
        """Get details for the career rank progression reward track.

        Returns:
            The career rank reward track.
        """
        url = f"{_HOST}/hi/Progression/file/RewardTracks/CareerRanks/careerRank1.json"
        return await self._get_model(url, CareerRewardTrack)

    async def get_operation_reward_track(
        self,
        reward_track_path: str,
    ) -> OperationRewardTrack:
        """Get details for a single operation reward track.

        Args:
            reward_track_path: The relative path to the operation reward track
                file, such as "RewardTracks/Operations/S05OpPassM01.json".

        Returns:
            The operation reward track definition.
        """
        url = f"{_HOST}/hi/Progression/file/{reward_track_path.lstrip('/')}"
        return await self._get_model(url, OperationRewardTrack)

    async def get_image(self, relative_path: str) -> bytes:
        """Get an image from the game content management service.

        Args:
            relative_path: The relative path to the image, such as
                "career_rank/ProgressWidget/272_Hero.png".

        Returns:
            The image data.
        """
        url = f"{_HOST}/hi/images/file/{relative_path.lstrip('/')}"
        resp = await self._get(url)
        return await resp.read()
