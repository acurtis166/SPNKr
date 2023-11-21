"""Provides a client for the Halo Infinite API.

Endpoints are documented at:
https://settings.svc.halowaypoint.com/settings/hipc/e2a0a7c6-6efe-42af-9283-c2ab73250c48

Additionally inspected the network traffic while navigating Halo Waypoint.
"""

from typing import Iterable, Literal
from uuid import UUID

from aiohttp import ClientResponse, ClientSession
from aiolimiter import AsyncLimiter

from .xuid import wrap_xuid, wrap_xuid_or_gamertag

GAMECMS_HACS_HOST = "https://gamecms-hacs.svc.halowaypoint.com"
SKILL_HOST = "https://skill.svc.halowaypoint.com:443"
STATS_HOST = "https://halostats.svc.halowaypoint.com:443"
UGC_DISCOVERY_HOST = "https://discovery-infiniteugc.svc.halowaypoint.com:443"


def _create_limiter(rate_per_second: int) -> AsyncLimiter:
    """Return an AsyncLimiter with the given rate per second."""
    # Setting the max rate to 1 disallows bursts.
    return AsyncLimiter(1, 1 / rate_per_second)


class HaloInfiniteClient:
    """A client for the Halo Infinite API."""

    def __init__(
        self,
        session: ClientSession,
        spartan_token: str,
        clearance_token: str,
        requests_per_second: int | None = 5,
    ) -> None:
        """Initialize a client for the Halo Infinite API.

        Raw `aiohttp` `ClientResponses` are returned from each method. The
        caller is responsible for handling the response via custom parsing or by
        using one of the provided parsers from the `spnkr.parsers` module.

        Args:
            session: The aiohttp session to use.
            spartan_token: The spartan token used to authenticate with the API.
            clearance_token: The clearance token used to authenticate with the
                API.
            requests_per_second: The rate limit to use. Defaults to 5 requests
                per second. Set to None to disable rate limiting.
        """
        self._session = session
        headers = {
            "Accept": "application/json",
            "x-343-authorization-spartan": spartan_token,
            "343-clearance": clearance_token,
        }
        self._session.headers.update(headers)

        self._rate_limiter = None
        if requests_per_second is not None:
            self._rate_limiter = _create_limiter(requests_per_second)

    async def _get(self, url: str, **kwargs) -> ClientResponse:
        """Make a GET request to the given URL."""
        if self._rate_limiter is None:
            return await self._session.get(url, **kwargs)
        async with self._rate_limiter:
            return await self._session.get(url, **kwargs)

    async def get_medal_metadata(self) -> ClientResponse:
        """Get details for all medals obtainable in the game.

        Parsers:
            - [MedalMetadata][spnkr.parsers.pydantic.gamecms_hacs.MedalMetadata]
            - [parse_medal_metadata][spnkr.parsers.records.gamecms_hacs.parse_medal_metadata]

        Returns:
            The medal metadata.
        """
        url = f"{GAMECMS_HACS_HOST}/hi/Waypoint/file/medals/metadata.json"
        return await self._get(url)

    async def get_match_skill(
        self, match_id: str | UUID, xuids: Iterable[str | int]
    ) -> ClientResponse:
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
        url = f"{SKILL_HOST}/hi/matches/{match_id}/skill"
        params = {"players": [wrap_xuid(x) for x in xuids]}
        return await self._get(url, params=params)

    async def get_playlist_csr(
        self, playlist_id: str | UUID, xuids: Iterable[str | int]
    ) -> ClientResponse:
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
        url = f"{SKILL_HOST}/hi/playlist/{playlist_id}/csrs"
        params = {"players": [wrap_xuid(x) for x in xuids]}
        return await self._get(url, params=params)

    async def get_match_count(self, player: str | int) -> ClientResponse:
        """Get match counts across different game experiences for a player.

        The counts returned are for custom matches, matchmade matches, local
        matches, and total matches.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".

        Parsers:
            - [MatchCount][spnkr.parsers.pydantic.stats.MatchCount]
            - [parse_match_count][spnkr.parsers.records.stats.parse_match_count]

        Returns:
            The match counts.
        """
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        url = f"{STATS_HOST}/hi/players/{xuid_or_gamertag}/matches/count"
        return await self._get(url)

    async def get_match_history(
        self,
        player: str | int,
        start: int = 0,
        count: int = 25,
        match_type: Literal["all", "matchmaking", "custom", "local"] = "all",
    ) -> ClientResponse:
        """Request a batch of matches from a player's match history.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".
            start: Index of the first match to request, starting at 0.
            count: The number of matches to request. Maximum number of results
                returned is 25.
            match_type: The type of matches to return. One of "all",
                "matchmaking", "custom", or "local".

        Parsers:
            - [MatchHistory][spnkr.parsers.pydantic.stats.MatchHistory]
            - [parse_match_history][spnkr.parsers.records.stats.parse_match_history]

        Returns:
            The requested match history "page" of results.
        """
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        url = f"{STATS_HOST}/hi/players/{xuid_or_gamertag}/matches"
        params = {"start": start, "count": count, "type": match_type}
        return await self._get(url, params=params)

    async def get_match_stats(self, match_id: str | UUID) -> ClientResponse:
        """Request match details using the Halo Infinite match GUID.

        Args:
            match_id: Halo Infinite GUID identifying the match.

        Parsers:
            - [MatchStats][spnkr.parsers.pydantic.stats.MatchStats]
            - [parse_match_info][spnkr.parsers.records.stats.parse_match_info]
            - [parse_player_core_stats][spnkr.parsers.records.stats.parse_player_core_stats]
            - [parse_player_medals][spnkr.parsers.records.stats.parse_player_medals]
            - [parse_team_core_stats][spnkr.parsers.records.stats.parse_team_core_stats]

        Returns:
            The match details.
        """
        url = f"{STATS_HOST}/hi/matches/{match_id}/stats"
        return await self._get(url)

    async def get_ugc_game_variant(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a game mode.

        Args:
            asset_id: The asset ID of the game variant.
            version_id: The version ID of the game variant.

        Parsers:
            - [UgcGameVariant][spnkr.parsers.pydantic.ugc_discovery.UgcGameVariant]
            - [parse_asset][spnkr.parsers.records.ugc_discovery.parse_asset]

        Returns:
            The game variant details.
        """
        endpoint = f"/hi/ugcGameVariants/{asset_id}/versions/{version_id}"
        url = f"{UGC_DISCOVERY_HOST}{endpoint}"
        return await self._get(url)

    async def get_map_mode_pair(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a map mode pair.

        Args:
            asset_id: The asset ID of the map mode pair.
            version_id: The version ID of the map mode pair.

        Parsers:
            - [MapModePair][spnkr.parsers.pydantic.ugc_discovery.MapModePair]
            - [parse_asset][spnkr.parsers.records.ugc_discovery.parse_asset]

        Returns:
            The map mode pair details.
        """
        endpoint = f"/hi/mapModePairs/{asset_id}/versions/{version_id}"
        url = f"{UGC_DISCOVERY_HOST}{endpoint}"
        return await self._get(url)

    async def get_map(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a map.

        Args:
            asset_id: The asset ID of the map.
            version_id: The version ID of the map.

        Parsers:
            - [Map][spnkr.parsers.pydantic.ugc_discovery.Map]
            - [parse_asset][spnkr.parsers.records.ugc_discovery.parse_asset]

        Returns:
            The map details.
        """
        endpoint = f"/hi/maps/{asset_id}/versions/{version_id}"
        url = f"{UGC_DISCOVERY_HOST}{endpoint}"
        return await self._get(url)

    async def get_playlist(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a playlist.

        Args:
            asset_id: The asset ID of the playlist.
            version_id: The version ID of the playlist.

        Parsers:
            - [Playlist][spnkr.parsers.pydantic.ugc_discovery.Playlist]
            - [parse_asset][spnkr.parsers.records.ugc_discovery.parse_asset]

        Returns:
            The playlist details.
        """
        endpoint = f"/hi/playlists/{asset_id}/versions/{version_id}"
        url = f"{UGC_DISCOVERY_HOST}{endpoint}"
        return await self._get(url)
