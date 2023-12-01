"""Skill data services."""

from typing import Any, Iterable
from uuid import UUID

from ..xuid import wrap_xuid
from .base import BaseService

_HOST = "https://skill.svc.halowaypoint.com:443"


class SkillService(BaseService):
    """Skill data services."""

    async def get_match_skill(
        self, match_id: str | UUID, xuids: Iterable[str | int]
    ) -> dict[str, Any]:
        """Get player CSR and team MMR values for a given match and player list.

        Args:
            match_id: Halo Infinite match ID.
            xuids: The Xbox Live IDs of the match's players. Only
                players in this list will have their skill data returned.

        Parsers:
            - [MatchSkill][spnkr.parsers.pydantic.skill.MatchSkill]
            - [parse_match_skill][spnkr.parsers.records.skill.parse_match_skill]

        Returns:
            The skill data for the match.
        """
        url = f"{_HOST}/hi/matches/{match_id}/skill"
        params = {"players": [wrap_xuid(x) for x in xuids]}
        return await self._get(url, params=params)

    async def get_playlist_csr(
        self, playlist_id: str | UUID, xuids: Iterable[str | int]
    ) -> dict[str, Any]:
        """Get player CSR values for a given playlist and player list.

        Args:
            playlist_id: Halo Infinite playlist asset ID.
            xuids: The Xbox Live IDs of the players.

        Parsers:
            - [PlaylistCsr][spnkr.parsers.pydantic.skill.PlaylistCsr]
            - [parse_playlist_csr][spnkr.parsers.records.skill.parse_playlist_csr]

        Returns:
            The summary CSR data for the players in the given playlist.
        """
        url = f"{_HOST}/hi/playlist/{playlist_id}/csrs"
        params = {"players": [wrap_xuid(x) for x in xuids]}
        return await self._get(url, params=params)
