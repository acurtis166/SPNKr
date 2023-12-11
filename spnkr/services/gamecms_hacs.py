"""Game content management data services."""

from ..models.gamecms_hacs import (
    CsrSeasonCalendar,
    MedalMetadata,
    SeasonCalendar,
)
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

    async def get_csr_season_calendar(self) -> CsrSeasonCalendar:
        """Get IDs and dates for past and current CSR seasons.

        CSR seasons represent the time periods between CSR resets.

        Returns:
            The CSR season calendar.
        """
        url = (
            f"{_HOST}/hi/Progression/file/Csr/Calendars/CsrSeasonCalendar.json"
        )
        return CsrSeasonCalendar(**await self._get(url))

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
        return SeasonCalendar(**await self._get(url))
