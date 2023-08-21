"""Provides a client for the Halo Infinite API.

Endpoints are documented at:
https://settings.svc.halowaypoint.com/settings/hipc/e2a0a7c6-6efe-42af-9283-c2ab73250c48

Additionally inspected the network traffic while navigating Halo Waypoint.
"""

from dataclasses import dataclass
from typing import Iterable, Literal
from uuid import UUID

from aiohttp import ClientResponse, ClientSession

from .xuid import XUID

GAMECMS_HACS_HOST = "https://gamecms-hacs.svc.halowaypoint.com"
SKILL_HOST = "https://skill.svc.halowaypoint.com:443"
STATS_HOST = "https://halostats.svc.halowaypoint.com:443"
UGC_DISCOVERY_HOST = "https://discovery-infiniteugc.svc.halowaypoint.com:443"


@dataclass(frozen=True)
class HaloInfiniteClient:
    """A client for the Halo Infinite API.

    Raw `aiohttp` `ClientResponses` are returned from each method. The caller is
    responsible for handling the response via custom parsing or by using one of
    the provided parsers from the `spnkr.parsers` module.

    Attributes:
        session: The aiohttp session to use.
        spartan_token: The Spartan token used to authenticate with the API.
        clearance_token: The clearance token used to authenticate with the API.
    """

    session: ClientSession
    spartan_token: str
    clearance_token: str

    def __post_init__(self) -> None:
        """Set the authorization headers on the session."""
        self.session.headers.update(
            {
                "Accept": "application/json",
                "x-343-authorization-spartan": self.spartan_token,
                "343-clearance": self.clearance_token,
            }
        )

    async def get_medal_metadata(self) -> ClientResponse:
        """Get details for all medals obtainable in the game.

        Returns:
            The medal metadata.
        """
        url = f"{GAMECMS_HACS_HOST}/hi/Waypoint/file/medals/metadata.json"
        return await self.session.get(url)

    async def get_match_skill(
        self, match_id: str | UUID, xuids: Iterable[str | int | XUID]
    ) -> ClientResponse:
        """Get player CSR and team MMR values for a given match and player list.

        Args:
            match_id: Halo Infinite match ID.
            xuids: The Xbox Live IDs of the match's players. Only
                players in this list will have their skill data returned.

        Returns:
            The skill data for the match.
        """
        url = f"{SKILL_HOST}/hi/matches/{match_id}/skill"
        params = {"players": [XUID.wrap(x) for x in xuids]}
        return await self.session.get(url, params=params)

    async def get_playlist_csr(
        self, playlist_id: str | UUID, xuids: Iterable[str | int | XUID]
    ) -> ClientResponse:
        """Get player CSR values for a given playlist and player list.

        Args:
            playlist_id: Halo Infinite playlist asset ID.
            xuids: The Xbox Live IDs of the players.

        Returns:
            The summary CSR data for the players in the given playlist.
        """
        url = f"{SKILL_HOST}/hi/playlist/{playlist_id}/csrs"
        params = {"players": [XUID.wrap(x) for x in xuids]}
        return await self.session.get(url, params=params)

    async def get_match_count(self, xuid: str | int | XUID) -> ClientResponse:
        """Get match counts across different game experiences for a player.

        The counts returned are for custom matches, matchmade matches, local
        matches, and total matches.

        Args:
            xuid: Xbox Live ID of the player to get counts for.

        Returns:
            The match counts.
        """
        url = f"{STATS_HOST}/hi/players/{XUID(xuid)}/matches/count"
        return await self.session.get(url)

    async def get_match_history(
        self,
        xuid: str | int | XUID,
        start: int = 0,
        count: int = 25,
        match_type: Literal["all", "matchmaking", "custom", "local"] = "all",
    ) -> ClientResponse:
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
                "all", "matchmaking", "custom", or "local". Defaults to "all".

        Returns:
            The requested match history "page" of results.
        """
        url = f"{STATS_HOST}/hi/players/{XUID(xuid)}/matches"
        params = {"start": start, "count": count, "type": match_type}
        return await self.session.get(url, params=params)

    async def get_match_stats(self, match_id: str | UUID) -> ClientResponse:
        """Request match details using the Halo Infinite match GUID.

        Args:
            match_id: Halo Infinite GUID identifying the match.

        Returns:
            The match details.
        """
        url = f"{STATS_HOST}/hi/matches/{match_id}/stats"
        return await self.session.get(url)

    async def get_ugc_game_variant(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a game mode.

        Args:
            asset_id: The asset ID of the game variant.
            version_id: The version ID of the game variant.

        Returns:
            The game variant details.
        """
        endpoint = f"/hi/ugcGameVariants/{asset_id}/versions/{version_id}"
        url = f"{UGC_DISCOVERY_HOST}{endpoint}"
        return await self.session.get(url)

    async def get_map_mode_pair(
        self,
        asset_id: str | UUID,
        version_id: str | UUID,
    ) -> ClientResponse:
        """Get details about a map mode pair.

        Args:
            asset_id: The asset ID of the map mode pair.
            version_id: The version ID of the map mode pair.

        Returns:
            The map mode pair details.
        """
        endpoint = f"/hi/mapModePairs/{asset_id}/versions/{version_id}"
        url = f"{UGC_DISCOVERY_HOST}{endpoint}"
        return await self.session.get(url)

    async def get_map(
        self, asset_id: str | UUID, version_id: str | UUID
    ) -> ClientResponse:
        """Get details about a map.

        Args:
            asset_id: The asset ID of the map.
            version_id: The version ID of the map.

        Returns:
            The map details.
        """
        endpoint = f"/hi/maps/{asset_id}/versions/{version_id}"
        url = f"{UGC_DISCOVERY_HOST}{endpoint}"
        return await self.session.get(url)

    async def get_playlist(
        self,
        asset_id: str | UUID,
        version_id: str | UUID,
    ) -> ClientResponse:
        """Get details about a playlist.

        Args:
            asset_id: The asset ID of the playlist.
            version_id: The version ID of the playlist.

        Returns:
            The playlist details.
        """
        endpoint = f"/hi/playlists/{asset_id}/versions/{version_id}"
        url = f"{UGC_DISCOVERY_HOST}{endpoint}"
        return await self.session.get(url)
