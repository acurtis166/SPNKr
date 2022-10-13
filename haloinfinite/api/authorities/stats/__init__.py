"""Endpoints for the "halostats" authority."""

from haloinfinite.api.enums import MatchType
from haloinfinite.api.authorities.base import BaseAuthority
from haloinfinite.api.authorities.stats import models
from haloinfinite import util


class StatsAuthority(BaseAuthority):
    URL = 'https://halostats.svc.halowaypoint.com:443'

    def get_match_count(self, player_xuid: str) -> models.MatchCount:
        """Get match counts across different game experiences for a player.

        The counts returned are for custom matches, matchmade matches, local matches, and
        total matches.

        Args:
            player_xuid (str): Xbox Live ID of the player to get counts for.

        Returns:
            PlayerMatchCount: Match counts.
        """
        xuid = util.wrap_xuid(player_xuid)
        url = self.URL + f'/hi/players/{xuid}/matches/count'
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.MatchCount.parse_json(resp.text)

    def get_match_history(self,
                          player_xuid: str,
                          start: int = 0,
                          count: int = 25,
                          match_type: MatchType = MatchType.All) -> models.MatchHistoryResponse:
        """Request a batch of matches from a player's match history.

        Args:
            player_xuid (str): Xbox Live ID of the player to request matches for.
            start (int, optional): The number of matches to skip (offset). Starts at 0.
            count (int, optional): The number of matches to request. Max is 25.
                Cannot exceed the default value. The service will still return a valid
                response with only the default match count, but the upper limit is
                enforced here to ensure that the offset isn't incremented incorrectly
                when attempting to collect continuous match data for a player.
            match_type (enums.MatchType): The type of matches to return. Defaults to "All".

        Returns:
            MatchHistory: _description_
        """
        xuid = util.wrap_xuid(player_xuid)
        url = self.URL + f'/hi/players/{xuid}/matches'
        params = {
            'start': start,
            'count': count,
            'type': match_type.name,
        }
        resp = self._session.get(url, params=params)
        resp.raise_for_status()
        return models.MatchHistoryResponse.parse_json(resp.text)

    def get_match_stats(self, match_guid: str) -> models.MatchStats:
        """Request match details using the Halo Infinite match GUID.

        Args:
            match_guid (str): Halo Infinite GUID identifying the match.

        Returns:
            MatchStats: Match details.
        """
        url = self.URL + f'/hi/matches/{match_guid}/stats'
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.MatchStats.parse_json(resp.text)

