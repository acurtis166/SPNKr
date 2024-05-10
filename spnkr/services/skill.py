"""Skill data services."""

from pathlib import Path
from typing import Iterable
from uuid import UUID

from spnkr.models.skill import MatchSkill, PlaylistCsr
from spnkr.responses import JsonResponse
from spnkr.services.base import BaseService
from spnkr.xuid import wrap_xuid

_HOST = "https://skill.svc.halowaypoint.com:443"


class SkillService(BaseService):
    """Skill data services."""

    async def get_match_skill(
        self, match_id: str | UUID, xuids: Iterable[str | int]
    ) -> JsonResponse[MatchSkill]:
        """Get player CSR and team MMR values for a given match and player list.

        Args:
            match_id: Halo Infinite match ID.
            xuids: The Xbox Live IDs of the match's players. Only
                players in this list will have their skill data returned.

        Returns:
            The skill data for the match.

        Raises:
            TypeError: If `xuids` is a `str` instead of an iterable of XUIDs.
            ValueError: If `xuids` is empty.
        """
        if isinstance(xuids, str):
            raise TypeError("`xuids` must be an iterable of XUIDs, got `str`")
        if not xuids:
            raise ValueError("`xuids` cannot be empty")
        url = f"{_HOST}/hi/matches/{match_id}/skill"
        params = {"players": [wrap_xuid(x) for x in xuids]}
        resp = await self._get(url, params=params)
        return JsonResponse(resp, lambda data: MatchSkill(**data))

    async def get_playlist_csr(
        self,
        playlist_id: str | UUID,
        xuids: Iterable[str | int],
        season_id: str | None = None,
    ) -> JsonResponse[PlaylistCsr]:
        """Get player CSR values for a given playlist and player list.

        Args:
            playlist_id: Halo Infinite playlist asset ID.
            xuids: The Xbox Live IDs of the players.
            season_id: Halo Infinite season ID. If not provided, the
                current season will be used. Value can be provided as a path,
                e.g. "Csr/Seasons/CsrSeason5-1.json", or as a bare ID,
                e.g. "CsrSeason5-1". If provided as a path, the path prefix
                and ".json" extension will be removed. Case is not important.

        Returns:
            The summary CSR data for the players in the given playlist.

        Raises:
            TypeError: If `xuids` is a `str` instead of an iterable of XUIDs.
            ValueError: If `xuids` is empty.
        """
        if isinstance(xuids, str):
            raise TypeError("`xuids` must be an iterable of XUIDs, got `str`")
        if not xuids:
            raise ValueError("`xuids` cannot be empty")
        url = f"{_HOST}/hi/playlist/{playlist_id}/csrs"
        params: dict = {"players": [wrap_xuid(x) for x in xuids]}
        if season_id:
            params["season"] = _clean_season_id(season_id)
        resp = await self._get(url, params=params)
        return JsonResponse(resp, lambda data: PlaylistCsr(**data))


def _clean_season_id(season_id: str) -> str:
    """Remove the path prefix and ".json" extension from a season ID.

    For example, season "Csr/Seasons/CsrSeason5-1.json" is cleaned to
    "CsrSeason5-1".
    """
    return Path(season_id).stem
