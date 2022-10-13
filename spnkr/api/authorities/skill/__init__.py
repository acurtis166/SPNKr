"""Endpoints for the "skill" authority."""

from spnkr.api.authorities.base import BaseAuthority
from spnkr.api.authorities.skill import models
from spnkr.api.enums import AuthenticationMethod
from spnkr import util


class SkillAuthority(BaseAuthority):
    URL = 'https://skill.svc.halowaypoint.com:443'

    def get_match_result(self,
                         match_guid: str,
                         player_xuids: list[str]) -> models.MatchSkillInfo:
        """Get player CSR and team MMR values for a given match and player list.

        Args:
            match_guid (str): Halo Infinite match GUID.
            player_xuids (List[str]): The Xbox Live IDs of the match's players.

        Returns:
            MatchResult: The skill data. Top level key is "Value", whose associated
                value is a list of player skill results.
        """

        url = self.URL + f'/hi/matches/{match_guid}/skill'
        params = dict(players=[util.wrap_xuid(x) for x in player_xuids])
        resp = self._session.get(url, auth_method=AuthenticationMethod.ClearanceToken,
                                 params=params)
        resp.raise_for_status()
        return models.MatchSkillInfo.parse_json(resp.text)

    def get_playlist_csr(self,
                         playlist_id: str,
                         player_xuids: list[str]) -> models.PlaylistCsrInfo:
        url = self.URL + f'/hi/playlist/{playlist_id}/csrs'
        params = dict(players=[util.wrap_xuid(x) for x in player_xuids])
        resp = self._session.get(url, auth_method=AuthenticationMethod.ClearanceToken,
                                 params=params)
        resp.raise_for_status()
        return models.PlaylistCsrInfo.parse_json(resp.text)

