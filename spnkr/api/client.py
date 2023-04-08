from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal
from uuid import UUID

import aiohttp

from ..authentication.app import AzureApp
from ..authentication.manager import TokenManager
from .exceptions import ApiRateLimitExceedance
from .models import (
    AssetResponse,
    MatchCountResponse,
    MatchHistoryResponse,
    MatchSkillResponse,
    MatchStatsResponse,
    PlaylistCsrResponse,
    ProfileResponse,
)
from .session import AuthenticationMethod, Session

PROFILES_URL = "https://profile.xboxlive.com:443"
SKILL_URL = "https://skill.svc.halowaypoint.com:443"
STATS_URL = "https://halostats.svc.halowaypoint.com:443"
UGC_DISCOVERY_URL = "https://discovery-infiniteugc.svc.halowaypoint.com:443"

PROFILES_REQUEST_LIMIT = 10
PROFILES_REQUEST_LIMIT_MINUTES = 10


def _unwrap_xuid(xuid: str | int) -> str:
    """Remove the "xuid()" wrapper from a XUID value."""
    xuid = str(xuid)
    return xuid[5:-1] if xuid[0] == "x" else xuid


def _wrap_xuid(xuid: str | int) -> str:
    """Add the "xuid()" wrapper to a XUID value."""
    xuid = str(xuid)
    return xuid if xuid[0] == "x" else f"xuid({xuid})"


@dataclass
class SPNKR:
    """A client for the Halo Infinite API.

    Endpoints are documented at:
    https://settings.svc.halowaypoint.com/settings/hipc/e2a0a7c6-6efe-42af-9283-c2ab73250c48

    Attributes:
        app (AzureApp): The Azure app to use for authentication.
        refresh_token (str): The refresh token to use for authentication.
    """

    app: AzureApp
    refresh_token: str

    async def __aenter__(self) -> SPNKR:
        """Initialize the client session and token manager."""
        self._client_session = aiohttp.ClientSession()
        self._token_manager = TokenManager(
            self._client_session, self.app, self.refresh_token
        )
        self._session = Session(self._client_session, self._token_manager)
        return self

    async def __aexit__(self, ex_type, ex, traceback) -> None:
        """Close the client session."""
        await self._client_session.close()

    async def get_my_xuid(self) -> str:
        """Get the API user's XUID."""
        jar = await self._token_manager.get_tokens()
        return jar.xuid

    async def get_my_gamertag(self) -> str:
        """Get the API user's gamertag."""
        jar = await self._token_manager.get_tokens()
        return jar.gamertag

    async def get_gamertags_by_xuids(
        self, xuids: Iterable[str | int]
    ) -> ProfileResponse:
        """Get Xbox Live profiles for a list of XUIDs.

        This endpoint is rate limited to ? requests per ?.

        Args:
            xuids: A list of XUIDs to get profiles for.

        Returns:
            A profile response containing the gamertags of the players
            requested.
        """
        url = f"{PROFILES_URL}/users/batch/profile/settings"
        data = {
            "settings": ["Gamertag"],
            "userIds": [_unwrap_xuid(x) for x in xuids],
        }
        resp = await self._session.post(
            url, json=data, auth_method=AuthenticationMethod.XBOX_LIVE_V3
        )
        if resp.status == 429:
            raise ApiRateLimitExceedance(
                PROFILES_REQUEST_LIMIT, PROFILES_REQUEST_LIMIT_MINUTES
            )
        elif resp.error is not None:
            raise resp.error
        return ProfileResponse.from_dict(resp.data)

    async def get_gamertag_by_xuid(self, xuid: str | int) -> ProfileResponse:
        """Get an Xbox Live profile for a single player by their XUID.

        This endpoint is rate limited to ? requests per ?.

        Args:
            xuid: The XUID of the player to get the profile for.

        Returns:
            A profile response containing the gamertag of the player.
        """
        url = f"{PROFILES_URL}/users/{_wrap_xuid(xuid)}/profile/settings"
        params = {"settings": "Gamertag"}
        resp = await self._session.get(
            url,
            params=params,
            auth_method=AuthenticationMethod.XBOX_LIVE_V3,
        )
        if resp.status == 429:
            raise ApiRateLimitExceedance(
                PROFILES_REQUEST_LIMIT, PROFILES_REQUEST_LIMIT_MINUTES
            )
        elif resp.error is not None:
            raise resp.error
        return ProfileResponse.from_dict(resp.data)

    async def get_xuid_by_gamertag(
        self,
        gamertag: str,
    ) -> ProfileResponse:
        """Get an Xbox Live profile for a single player by their gamertag.

        This endpoint is rate limited to ? requests per ?.

        Args:
            gamertag (str): The gamertag of the player to get the profile for.

        Returns:
            A profile response containing the XUID of the player.
        """
        url = f"{PROFILES_URL}/users/gt({gamertag})/profile/settings"
        params = {
            "settings": "Gamertag",
        }
        resp = await self._session.get(
            url,
            params=params,
            auth_method=AuthenticationMethod.XBOX_LIVE_V3,
        )
        if resp.status == 429:
            raise ApiRateLimitExceedance(
                PROFILES_REQUEST_LIMIT, PROFILES_REQUEST_LIMIT_MINUTES
            )
        elif resp.error is not None:
            raise resp.error
        return ProfileResponse.from_dict(resp.data)

    async def get_match_skill(
        self, match_id: str | UUID, xuids: Iterable[str | int]
    ) -> MatchSkillResponse:
        """Get player CSR and team MMR values for a given match and player list.

        Args:
            match_id: Halo Infinite match ID.
            xuids: The Xbox Live IDs of the match's players. Only
                players in this list will have their skill data returned.

        Returns:
            The skill data for the match.
        """
        url = f"{SKILL_URL}/hi/matches/{match_id}/skill"
        params = dict(players=[_wrap_xuid(x) for x in xuids])
        resp = await self._session.get(
            url, auth_method=AuthenticationMethod.CLEARANCE_TOKEN, params=params
        )
        if resp.error is not None:
            raise resp.error
        return MatchSkillResponse.from_dict(resp.data)

    async def get_playlist_csr(
        self, playlist_id: str | UUID, xuids: Iterable[str | int]
    ) -> PlaylistCsrResponse:
        """Get player CSR values for a given playlist and player list.

        Args:
            playlist_id: Halo Infinite playlist asset ID.
            xuids: The Xbox Live IDs of the players.

        Returns:
            The summary CSR data for the players in the given playlist.
        """
        url = f"{SKILL_URL}/hi/playlist/{playlist_id}/csrs"
        params = dict(players=[_wrap_xuid(x) for x in xuids])
        resp = await self._session.get(
            url, auth_method=AuthenticationMethod.CLEARANCE_TOKEN, params=params
        )
        if resp.error is not None:
            raise resp.error
        return PlaylistCsrResponse.from_dict(resp.data)

    async def get_match_count(self, xuid: str | int) -> MatchCountResponse:
        """Get match counts across different game experiences for a player.

        The counts returned are for custom matches, matchmade matches, local
        matches, and total matches.

        Args:
            xuid: Xbox Live ID of the player to get counts for.
        """
        xuid = _wrap_xuid(xuid)
        url = f"{STATS_URL}/hi/players/{xuid}/matches/count"
        resp = await self._session.get(url)
        if resp.error is not None:
            raise resp.error
        return MatchCountResponse.from_dict(resp.data)

    async def get_match_history(
        self,
        xuid: str | int,
        start: int = 0,
        count: int = 25,
        match_type: Literal["All", "Matchmaking", "Custom", "Local"] = "All",
    ) -> MatchHistoryResponse:
        """Request a batch of matches from a player's match history.

        Args:
            xuid: Xbox Live ID of the player to request matches
                for.
            start: The number of matches to skip (offset).
                Starts at 0.
            count: The number of matches to request. Max is 25.
                Cannot exceed the default value. The service will still return a
                valid response with only the default match count, but the upper
                limit is enforced here to ensure that the offset isn't
                incremented incorrectly when attempting to collect continuous
                match data for a player.
            match_type: The type of matches to return. One of
                "All", "Matchmaking", "Custom", or "Local". Defaults to "All".
        """
        url = f"{STATS_URL}/hi/players/{_wrap_xuid(xuid)}/matches"
        params = {"start": start, "count": count, "type": match_type}
        resp = await self._session.get(url, params=params)
        if resp.error is not None:
            raise resp.error
        return MatchHistoryResponse.from_dict(resp.data)

    async def get_match_stats(self, match_id: str | UUID) -> MatchStatsResponse:
        """Request match details using the Halo Infinite match GUID.

        Args:
            match_id: Halo Infinite GUID identifying the match.

        Returns:
            The match details.
        """
        url = f"{STATS_URL}/hi/matches/{match_id}/stats"
        resp = await self._session.get(url)
        if resp.error is not None:
            raise resp.error
        return MatchStatsResponse.from_dict(resp.data)

    async def get_ugc_game_variant(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> AssetResponse:
        """Get details about a game mode.

        Args:
            asset_id: The asset ID of the game variant.
            version_id: The version ID of the game variant.

        Returns:
            The game variant details.
        """
        url = f"{UGC_DISCOVERY_URL}/hi/ugcGameVariants/{asset_id}/versions/{version_id}"
        resp = await self._session.get(url)
        if resp.error is not None:
            raise resp.error
        return AssetResponse.from_dict(resp.data)

    async def get_map_mode_pair(
        self,
        asset_id: str | UUID,
        version_id: str | UUID,
        clearance_id: str | None = None,
    ) -> AssetResponse:
        """Get details about a map mode pair.

        Args:
            asset_id: The asset ID of the map mode pair.
            version_id: The version ID of the map mode pair.
            clearance_id: ...

        Returns:
            The map mode pair details.
        """
        url = f"{UGC_DISCOVERY_URL}/hi/mapModePairs/{asset_id}/versions/{version_id}"
        params = (
            {"clearanceId": clearance_id} if clearance_id is not None else None
        )
        resp = await self._session.get(url, params=params)
        if resp.error is not None:
            raise resp.error
        return AssetResponse.from_dict(resp.data)

    async def get_map(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> AssetResponse:
        """Get details about a map.

        Args:
            asset_id: The asset ID of the map.
            version_id: The version ID of the map.

        Returns:
            The map details.
        """
        url = f"{UGC_DISCOVERY_URL}/hi/maps/{asset_id}/versions/{version_id}"
        resp = await self._session.get(url)
        if resp.error is not None:
            raise resp.error
        return AssetResponse.from_dict(resp.data)

    async def get_playlist(
        self,
        asset_id: str | UUID,
        version_id: str | UUID,
        clearance_id: str | None = None,
    ) -> AssetResponse:
        """Get details about a playlist.

        Args:
            asset_id: The asset ID of the playlist.
            version_id: The version ID of the playlist.
            clearance_id: ...

        Returns:
            The playlist details.
        """
        url = (
            f"{UGC_DISCOVERY_URL}/hi/playlists/{asset_id}/versions/{version_id}"
        )
        params = (
            {"clearanceId": clearance_id} if clearance_id is not None else None
        )
        resp = await self._session.get(url, params=params)
        if resp.error is not None:
            raise resp.error
        return AssetResponse.from_dict(resp.data)
