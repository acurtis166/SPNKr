"""Provides a simplified API for retrieving match data."""

from uuid import UUID

from .client import HaloInfiniteClient
from .models.discovery_ugc import Map, MapModePair, Playlist, UgcGameVariant
from .models.profile import User
from .models.refdata import LifecycleMode
from .models.skill import MatchSkill
from .models.stats import MatchInfo, MatchStats
from .xuid import wrap_xuid


class Match:
    """A Halo Infinite match reference for simplified retrieval of match data."""

    def __init__(
        self,
        client: HaloInfiniteClient,
        match_id: str | UUID,
        match_info: MatchInfo | None = None,
    ) -> None:
        """Create a match reference for simplified retrieval of match data.

        Args:
            client: The Halo Infinite client to use for requests.
            match: The ID of the match.
            match_info: The match info. If not provided, it will be retrieved
                with a match stats request when needed. Providing this argument
                saves a stats request if the desired information is limited to
                map/mode/playlist. Available from a match history request.
        """
        self._client = client
        self._id = match_id if isinstance(match_id, UUID) else UUID(match_id)
        self._info = match_info
        self._stats = None

    @property
    def id(self) -> UUID:
        """The ID of the match."""
        return self._id

    async def get_stats(self) -> MatchStats:
        """Get the stats for this match."""
        if self._stats is None:
            self._stats = await self._client.stats.get_match_stats(self._id)
        return self._stats

    async def get_info(self) -> MatchInfo:
        """Get the match info for this match."""
        if self._info is None:
            self._info = (await self.get_stats()).match_info
        return self._info

    async def get_map(self) -> Map:
        """Get the map this match was played on."""
        info = await self.get_info()
        return await self._client.discovery_ugc.get_map(
            info.map_variant.asset_id, info.map_variant.version_id
        )

    async def get_mode(self) -> UgcGameVariant:
        """Get the game mode this match was played on."""
        info = await self.get_info()
        return await self._client.discovery_ugc.get_ugc_game_variant(
            info.ugc_game_variant.asset_id, info.ugc_game_variant.version_id
        )

    async def get_playlist(self) -> Playlist | None:
        """Get the playlist this match was found in. Matchmaking only."""
        info = await self.get_info()
        if info.playlist is None:
            return None
        return await self._client.discovery_ugc.get_playlist(
            info.playlist.asset_id, info.playlist.version_id
        )

    async def get_map_mode_pair(self) -> MapModePair | None:
        """Get the map-mode pair selected for this match. Matchmaking only."""
        info = await self.get_info()
        map_mode_pair = info.playlist_map_mode_pair
        if map_mode_pair is None:
            return None
        return await self._client.discovery_ugc.get_map_mode_pair(
            map_mode_pair.asset_id, map_mode_pair.version_id
        )

    async def get_users(self) -> dict[str, User]:
        """Get a mapping of XUIDs to profiles for players in this match."""
        stats = await self.get_stats()
        xuids = [p.player_id for p in stats.players if p.is_human]
        users = await self._client.profile.get_users_by_id(xuids)
        return {wrap_xuid(user.xuid): user for user in users}

    async def get_skill(self) -> MatchSkill | None:
        """Get CSR/MMR information for this match. Matchmaking only."""
        info = await self.get_info()
        if info.lifecycle_mode is not LifecycleMode.MATCHMADE:
            # Skill data is only available for matchmade games.
            return None
        stats = await self.get_stats()
        xuids = [p.player_id for p in stats.players if p.is_human]
        return await self._client.skill.get_match_skill(self._id, xuids)
