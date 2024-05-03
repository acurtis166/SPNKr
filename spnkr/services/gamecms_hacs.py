"""Game content management data services."""

from spnkr.models.gamecms_hacs import (
    CareerRewardTrack,
    CsrSeasonCalendar,
    MedalMetadata,
    SeasonCalendar,
)
from spnkr.services.base import BaseService

_HOST = "https://gamecms-hacs.svc.halowaypoint.com"


class GameCmsHacsService(BaseService):
    """Game content management data services."""

    async def get_medal_metadata(self) -> MedalMetadata:
        """Get details for all medals obtainable in the game.

        Returns:
            The medal metadata.
        """
        url = f"{_HOST}/hi/Waypoint/file/medals/metadata.json"
        return MedalMetadata(**await self._get_json(url))

    async def get_csr_season_calendar(self) -> CsrSeasonCalendar:
        """Get IDs and dates for past and current CSR seasons.

        CSR seasons represent the time periods between CSR resets.

        Returns:
            The CSR season calendar.
        """
        url = (
            f"{_HOST}/hi/Progression/file/Csr/Calendars/CsrSeasonCalendar.json"
        )
        return CsrSeasonCalendar(**await self._get_json(url))

    async def get_season_calendar(self) -> SeasonCalendar:
        """Get IDs and dates for past/current reward track events/operations.

        Reward tracks are the progression systems that allow players to earn
        rewards from the XP earned by playing the game.

        Returns:
            The calendar of reward tracks.
        """
        url = (
            f"{_HOST}/hi/progression/file/calendars/seasons/seasoncalendar.json"
        )
        return SeasonCalendar(**await self._get_json(url))

    async def get_career_reward_track(self) -> CareerRewardTrack:
        """Get details for the career rank progression reward track.

        Returns:
            The career rank reward track.
        """
        url = f"{_HOST}/hi/Progression/file/RewardTracks/CareerRanks/careerRank1.json"
        return CareerRewardTrack(**await self._get_json(url))

    async def get_image(self, relative_path: str) -> bytes:
        """Get an image from the game content management service.

        Args:
            relative_path: The relative path to the image, such as
                "career_rank/ProgressWidget/272_Hero.png".

        Returns:
            The image data.
        """
        url = f"{_HOST}/hi/images/file/{relative_path.lstrip('/')}"
        return await self._get_bytes(url)
