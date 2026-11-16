"""Provides a client for the Halo Infinite API."""

import collections
import datetime as dt
from collections.abc import Iterable
from typing import Any, TypeVar, cast
from uuid import UUID

from aiolimiter import AsyncLimiter
from pydantic import BaseModel

from spnkr.http_helpers import Response, Session, send_api_request
from spnkr.models.discovery_ugc import (
    AssetSearchPage,
    Film,
    Map,
    MapModePair,
    Playlist,
    UgcGameVariant,
)
from spnkr.models.economy import (
    PlayerCareerRank,
    PlayerCustomization,
    PlayerOperationPasses,
)
from spnkr.models.gamecms_hacs import (
    CareerRewardTrack,
    CsrSeasonCalendar,
    MedalMetadata,
    OperationRewardTrack,
    SeasonCalendar,
)
from spnkr.models.profile import User
from spnkr.models.refdata import GameplayInteraction, GameVariantCategory
from spnkr.models.skill import MatchSkill, PlaylistCsr
from spnkr.models.stats import MatchCount, MatchHistory, MatchStats, ServiceRecord
from spnkr.request_helpers import (
    AssetKind,
    HistoryMatchType,
    ServiceRecordMatchType,
    SortOrder,
    SortProperty,
    ViewType,
    clean_season_id,
    get_localized_asset_kwargs,
    prepare_search_asset_params,
    prepare_service_record_params,
    validate_xuids,
)
from spnkr.xuid import unwrap_xuid, wrap_xuid, wrap_xuid_or_gamertag

__all__ = ["HaloInfiniteClient"]

T = TypeVar("T", bound=BaseModel)


class HaloInfiniteClient:
    """A client for the Halo Infinite API."""

    STATS_AUTHORITY = "halostats.svc.halowaypoint.com"
    SKILL_AUTHORITY = "skill.svc.halowaypoint.com"
    PROFILE_AUTHORITY = "profile.svc.halowaypoint.com"
    DISCOVERY_UGC_AUTHORITY = "discovery-infiniteugc.svc.halowaypoint.com"
    ECONOMY_AUTHORITY = "economy.svc.halowaypoint.com"
    GAMECMS_HACS_AUTHORITY = "gamecms-hacs.svc.halowaypoint.com"

    def __init__(
        self,
        session: Session,
        spartan_token: str,
        clearance_token: str,
        max_retries: int = 2,
        requests_per_second: float = 5,
    ) -> None:
        """Initialize a client for the Halo Infinite API.

        Args:
            session: The `aiohttp.ClientSession` to use. Support for caching is
                available via a `CachedSession` from `aiohttp-client-cache`.
            spartan_token: The spartan token used to authenticate with the API.
            clearance_token: The clearance token used to authenticate with the API.
            max_retries: The maximum number of times to retry a request on failure.
            requests_per_second: The rate limit to use. Note that this rate
                limit is enforced per service, not globally. Defaults to 5
                requests per second.
        """
        if requests_per_second <= 0:
            raise ValueError("requests_per_second must be greater than 0")

        self._session = session
        self._spartan_token = spartan_token
        self._clearance_token = clearance_token
        self._max_retries = max(0, max_retries)
        # Setting the max rate to 1 disallows bursts.
        self._rate_limiters = collections.defaultdict(
            lambda: AsyncLimiter(1, 1 / requests_per_second)
        )

    @property
    def session(self) -> Session:
        return self._session

    @property
    def spartan_token(self) -> str:
        return self._spartan_token

    @spartan_token.setter
    def spartan_token(self, value: str) -> None:
        self._spartan_token = value

    @property
    def clearance_token(self) -> str:
        return self._clearance_token

    @clearance_token.setter
    def clearance_token(self, value: str) -> None:
        self._clearance_token = value

    async def _get(self, authority: str, endpoint: str, **kwargs) -> Response:
        """Make a GET request to `url` and return the response."""
        return await send_api_request(
            session=self._session,
            method="GET",
            url=f"https://{authority.rstrip('/')}/{endpoint.lstrip('/')}",
            spartan_token=self._spartan_token,
            clearance_token=self._clearance_token,
            max_retries=self._max_retries,
            limiter=self._rate_limiters[authority],
            **kwargs,
        )

    async def _get_model(
        self, authority: str, endpoint: str, model: type[T], **kwargs
    ) -> T:
        """Make a GET request to `url` and return the response as a `model` instance."""
        response = await self._get(authority, endpoint, **kwargs)
        return model.model_validate_json(await response.read())

    async def _get_model_list(
        self, authority: str, endpoint: str, model: type[T], **kwargs
    ) -> list[T]:
        """Make a GET request to `url` and return the response as a list of `model` instances."""
        response = await self._get(authority, endpoint, **kwargs)
        return [
            model.model_validate(item) for item in cast(list, await response.json())
        ]

    # Stats authority

    async def get_challenge_decks(self, player: str | int) -> dict[str, Any]:
        """Get the current challenge decks assigned to a player.

        Args:
            player: Xbox Live ID or gamertag of the player to retrieve data
                for. Examples of valid inputs include
                "xuid(1234567890123456)", "1234567890123456",
                1234567890123456, and "MyGamertag".

        Returns:
            The raw decks payload returned by the API.
        """
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        resp = await self._get(
            self.STATS_AUTHORITY, f"hi/players/{xuid_or_gamertag}/decks"
        )
        return cast(dict[str, Any], await resp.json())

    async def get_match_count(self, player: str | int) -> MatchCount:
        """Get match counts across different game experiences for a player.

        The counts returned are for custom matches, matchmade matches, local
        matches, and total matches.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".

        Returns:
            The match counts.
        """
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        return await self._get_model(
            self.STATS_AUTHORITY,
            f"hi/players/{xuid_or_gamertag}/matches/count",
            MatchCount,
        )

    async def get_service_record(
        self,
        player: str | int,
        match_type: ServiceRecordMatchType = "matchmade",
        season_id: str | None = None,
        game_variant_category: GameVariantCategory | int | None = None,
        is_ranked: bool | None = None,
        playlist_asset_id: str | UUID | None = None,
        gameplay_interaction: GameplayInteraction | None = None,
    ) -> ServiceRecord:
        """Get a service record for a player. Summarizes player stats.

        Note that filters (`season_id`, `game_variant_category`, `is_ranked`,
        and `playlist_asset_id`) are only applicable to "matchmade"
        `match_type`. A warning is issued and the filters are ignored if they
        are provided for a non-matchmade `match_type`.

        Filters must be combined appropriately. The following are valid:

        - `season_id`
        - `season_id`, `game_variant_category`
        - `season_id`, `game_variant_category`, `playlist_asset_id`
        - `season_id`, `game_variant_category`, `is_ranked`
        - `season_id`, `playlist_asset_id`
        - `season_id`, `gameplay_interaction`
        - `game_variant_category`
        - `game_variant_category`, `is_ranked`

        To collect possible values for the filter arguments, look at the
        "subqueries" attribute of an unfiltered service record response.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".
            match_type: The type of games to include in the service record.
                One of "matchmade", "custom", or "local".
            season_id: The season ID to get service record for. Optional.
            game_variant_category: The game variant category to filter service
                record data. See `spnkr.parsers.refdata.GameVariantCategory` for
                human-readable values. Optional.
            is_ranked: Filter for ranked or unranked games. Optional.
            playlist_asset_id: Filter for a specific playlist with its asset ID.
                Optional.
            gameplay_interaction: Filter for a specific gameplay interaction
                (e.g., PVP).

        Returns:
            The service record for the player with the given filters.

        Raises:
            ValueError: If `match_type` is not one of "matchmade", "custom", or
                "local".
            ValueError: If filter arguments are inappropriately combined.
        """
        if match_type.lower() not in ("matchmade", "custom", "local"):
            raise ValueError(f"Invalid match type: {match_type}")
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        params = prepare_service_record_params(
            match_type=match_type,
            season_id=season_id,
            game_variant_category=game_variant_category,
            is_ranked=is_ranked,
            playlist_asset_id=playlist_asset_id,
            gameplay_interaction=gameplay_interaction,
        )
        return await self._get_model(
            self.STATS_AUTHORITY,
            f"hi/players/{xuid_or_gamertag}/{match_type}/servicerecord",
            ServiceRecord,
            params=params,
        )

    async def get_match_history(
        self,
        player: str | int,
        start: int = 0,
        count: int = 25,
        match_type: HistoryMatchType = "all",
    ) -> MatchHistory:
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

        Returns:
            The requested match history "page" of results.
        """
        xuid_or_gamertag = wrap_xuid_or_gamertag(player)
        params = {"start": start, "count": count, "type": match_type}
        return await self._get_model(
            self.STATS_AUTHORITY,
            f"hi/players/{xuid_or_gamertag}/matches",
            MatchHistory,
            params=params,
        )

    async def get_match_stats(self, match_id: str | UUID) -> MatchStats:
        """Request match details using the Halo Infinite match GUID.

        Args:
            match_id: Halo Infinite GUID identifying the match.

        Returns:
            The match details.
        """
        return await self._get_model(
            self.STATS_AUTHORITY, f"hi/matches/{match_id}/stats", MatchStats
        )

    # Skill authority

    async def get_match_skill(
        self, match_id: str | UUID, xuids: Iterable[str | int]
    ) -> MatchSkill:
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
        params = {"players": [wrap_xuid(x) for x in validate_xuids(xuids)]}
        return await self._get_model(
            self.SKILL_AUTHORITY,
            f"hi/matches/{match_id}/skill",
            MatchSkill,
            params=params,
        )

    async def get_playlist_csr(
        self,
        playlist_id: str | UUID,
        xuids: Iterable[str | int],
        season_id: str | None = None,
    ) -> PlaylistCsr:
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
        params: dict = {"players": [wrap_xuid(x) for x in validate_xuids(xuids)]}
        if season_id:
            params["season"] = clean_season_id(season_id)
        return await self._get_model(
            self.SKILL_AUTHORITY,
            f"hi/playlist/{playlist_id}/csrs",
            PlaylistCsr,
            params=params,
        )

    # Profile authority

    async def _get_user(self, user: str) -> User:
        return await self._get_model(self.PROFILE_AUTHORITY, f"users/{user}", User)

    async def get_current_user(self) -> User:
        """Get the current user profile.

        Returns:
            The user.
        """
        return await self._get_user("me")

    async def get_user_by_gamertag(self, gamertag: str) -> User:
        """Get user profile for the given gamertag.

        Args:
            gamertag: The gamertag of the player.

        Returns:
            The user.
        """
        return await self._get_user(f"gt({gamertag})")

    async def get_user_by_id(self, xuid: str | int) -> User:
        """Get user profile for the given Xbox Live ID.

        Args:
            xuid: The Xbox Live ID of the player.

        Returns:
            The user.
        """
        return await self._get_user(wrap_xuid(xuid))

    async def get_users_by_id(self, xuids: Iterable[str | int]) -> list[User]:
        """Get user profiles for the given list of Xbox Live IDs.

        Args:
            xuids: The Xbox Live IDs of the players.

        Returns:
            A list of users.

        Raises:
            TypeError: If `xuids` is a `str` instead of an iterable of XUIDs.
            ValueError: If `xuids` is empty.
        """
        params = {"xuids": [unwrap_xuid(x) for x in validate_xuids(xuids)]}
        return await self._get_model_list(
            self.PROFILE_AUTHORITY, "users", User, params=params
        )

    # Discovery UGC authority

    async def _get_asset(
        self,
        asset_type: str,
        asset_id: str | UUID,
        version_id: str | UUID,
        model: type[T],
        *,
        language: str | None = None,
    ) -> T:
        return await self._get_model(
            self.DISCOVERY_UGC_AUTHORITY,
            f"hi/{asset_type}/{asset_id}/versions/{version_id}",
            model,
            **get_localized_asset_kwargs(self.session, language),
        )

    async def get_ugc_game_variant(
        self,
        asset_id: str | UUID,
        version_id: str | UUID,
        *,
        language: str | None = None,
    ) -> UgcGameVariant:
        """Get details about a game mode.

        Args:
            asset_id: The asset ID of the game variant.
            version_id: The version ID of the game variant.
            language: Optional BCP-47 locale sent via the Accept-Language
                header. Use this to retrieve localized PublicName and
                Description fields.

        Returns:
            The game variant details.
        """
        return await self._get_asset(
            "ugcGameVariants",
            asset_id,
            version_id,
            UgcGameVariant,
            language=language,
        )

    async def get_map_mode_pair(
        self,
        asset_id: str | UUID,
        version_id: str | UUID,
        *,
        language: str | None = None,
    ) -> MapModePair:
        """Get details about a map mode pair.

        Args:
            asset_id: The asset ID of the map mode pair.
            version_id: The version ID of the map mode pair.
            language: Optional BCP-47 locale sent via the Accept-Language
                header. Use this to retrieve localized PublicName and
                Description fields.

        Returns:
            The map mode pair details.
        """
        return await self._get_asset(
            "mapModePairs",
            asset_id,
            version_id,
            MapModePair,
            language=language,
        )

    async def get_map(
        self,
        asset_id: str | UUID,
        version_id: str | UUID,
        *,
        language: str | None = None,
    ) -> Map:
        """Get details about a map.

        Args:
            asset_id: The asset ID of the map.
            version_id: The version ID of the map.
            language: Optional BCP-47 locale sent via the Accept-Language
                header. Use this to retrieve localized PublicName and
                Description fields.

        Returns:
            The map details.
        """
        return await self._get_asset(
            "maps",
            asset_id,
            version_id,
            Map,
            language=language,
        )

    async def get_playlist(
        self,
        asset_id: str | UUID,
        version_id: str | UUID,
        *,
        language: str | None = None,
    ) -> Playlist:
        """Get details about a playlist.

        Args:
            asset_id: The asset ID of the playlist.
            version_id: The version ID of the playlist.
            language: Optional BCP-47 locale sent via the Accept-Language
                header. Use this to retrieve localized PublicName and
                Description fields.

        Returns:
            The playlist details.
        """
        return await self._get_asset(
            "playlists",
            asset_id,
            version_id,
            Playlist,
            language=language,
        )

    async def search_assets(
        self,
        start: int = 0,
        count: int = 25,
        sort: SortProperty = "plays_recent",
        order: SortOrder = "desc",
        asset_kind: AssetKind | None = None,
        term: str | None = None,
        tags: Iterable[str] | None = None,
        author: str | None = None,
        average_rating_min: float | None = None,
        from_date_created_utc: dt.datetime | dt.date | None = None,
        to_date_created_utc: dt.datetime | dt.date | None = None,
        from_date_modified_utc: dt.datetime | dt.date | None = None,
        to_date_modified_utc: dt.datetime | dt.date | None = None,
        from_date_published_utc: dt.datetime | dt.date | None = None,
        to_date_published_utc: dt.datetime | dt.date | None = None,
    ) -> AssetSearchPage:
        """Search for map, mode, and prefab assets.

        Args:
            start: Index of the first result to return, starting at 0.
            count: Count of results to return. Must be between 1 and 101.
            sort: Property by which to sort the results. Must be one of the
                following: "name", "likes", "bookmarks", "plays_recent",
                "number_of_objects", "date_created_utc", "date_modified_utc",
                "date_published_utc", "plays_all_time", "parent_asset_count",
                "average_rating", "number_of_ratings". Defaults to
                "plays_recent".
            order: Pass "asc" for ascending or "desc" for descending.
            asset_kind: Type of asset to be searched. Optional. If a value is
                provided, it must be be one of the following: "map", "prefab",
                "ugc_game_variant". By default, no filter is applied.
            term: Search term. Optional.
            tags: List of tags. Multiple tags are applied with an OR operator.
                Optional.
            author: Author ID. Valid values would be in one of the following
                formats: "xuid(<xuid>)", "aaid(<aaid>)", or "atui(<atui>)",
                where <xuid> is a 16-digit Xbox user ID, <aaid> is a UUID, and
                <atui> is a pair of UUIDs separated by a period. Optional.
            average_rating_min: Minimum average rating between 0 and 5.
                Optional.
            from_date_created_utc: Minimum date created. Optional.
            to_date_created_utc: Maximum date created. Optional.
            from_date_modified_utc: Minimum date modified. Optional.
            to_date_modified_utc: Maximum date modified. Optional.
            from_date_published_utc: Minimum date published. Optional.
            to_date_published_utc: Maximum date published. Optional.

        Returns:
            A page of up to `count` search results.
        """
        if count < 1 or count > 101:
            raise ValueError("`count` must be between 1 and 101.")
        params = prepare_search_asset_params(
            start=start,
            count=count,
            sort=sort,
            order=order,
            asset_kind=asset_kind,
            term=term,
            tags=tags,
            author=author,
            average_rating_min=average_rating_min,
            from_date_created_utc=from_date_created_utc,
            to_date_created_utc=to_date_created_utc,
            from_date_modified_utc=from_date_modified_utc,
            to_date_modified_utc=to_date_modified_utc,
            from_date_published_utc=from_date_published_utc,
            to_date_published_utc=to_date_published_utc,
        )
        return await self._get_model(
            self.DISCOVERY_UGC_AUTHORITY, "hi/search", AssetSearchPage, params=params
        )

    async def get_film_by_match_id(self, match_id: str | UUID) -> Film:
        """Get metadata and download information for a film.

        Args:
            match_id: The match ID of the film.

        Returns:
            The film details.
        """
        return await self._get_model(
            self.DISCOVERY_UGC_AUTHORITY, f"hi/films/matches/{match_id}/spectate", Film
        )

    # Economy authority

    async def get_player_reward_track_operations(
        self, xuid: str | int
    ) -> PlayerOperationPasses:
        """Get the active and available operation reward tracks for a player.

        Args:
            xuid: The Xbox Live ID of the player to retrieve data for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", and 1234567890123456.

        Returns:
            The player's active and available operation reward tracks.
        """
        return await self._get_model(
            self.ECONOMY_AUTHORITY,
            f"hi/players/{wrap_xuid(xuid)}/rewardtracks/operations",
            PlayerOperationPasses,
        )

    async def get_player_career_rank(
        self, xuid: str | int, reward_track_id: str = "careerrank1"
    ) -> PlayerCareerRank:
        """Get the player's current progress on a career rank reward track.

        Args:
            xuid: The Xbox Live ID of the player to retrieve data for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", and 1234567890123456.
            reward_track_id: The career rank reward track identifier.

        Returns:
            The player's current career rank progress.
        """
        return await self._get_model(
            self.ECONOMY_AUTHORITY,
            f"hi/players/{wrap_xuid(xuid)}/rewardtracks/careerranks/{reward_track_id}",
            PlayerCareerRank,
        )

    async def get_player_customization(
        self, xuid: str | int, view_type: ViewType = "public"
    ) -> PlayerCustomization:
        """Get the customization selections for a player.

        Args:
            xuid: The Xbox Live ID of the player to retrieve data for.
            view_type: Use "public" when requesting customization for players
                other than yourself. The "private" view type only applies to the
                authenticated player making the request and might include data
                not visible using the "public" view type.

        Returns:
            The player's customization selections.
        """
        return await self._get_model(
            self.ECONOMY_AUTHORITY,
            f"hi/players/{wrap_xuid(xuid)}/customization",
            PlayerCustomization,
            params={"view": view_type},
        )

    # GameCMS/HACS authority

    async def get_progression_file(self, relative_path: str) -> dict[str, Any]:
        """Get a raw progression file from the GameCMS service.

        Args:
            relative_path: The relative path to the progression file.

        Returns:
            The raw JSON payload for the requested progression file.
        """
        resp = await self._get(
            self.GAMECMS_HACS_AUTHORITY,
            f"hi/Progression/file/{relative_path.lstrip('/')}",
        )
        return cast(dict[str, Any], await resp.json())

    async def get_medal_metadata(self) -> MedalMetadata:
        """Get details for all medals obtainable in the game.

        Returns:
            The medal metadata.
        """
        return await self._get_model(
            self.GAMECMS_HACS_AUTHORITY,
            "hi/Waypoint/file/medals/metadata.json",
            MedalMetadata,
        )

    async def get_csr_season_calendar(self) -> CsrSeasonCalendar:
        """Get IDs and dates for past and current CSR seasons.

        CSR seasons represent the time periods between CSR resets.

        Returns:
            The CSR season calendar.
        """
        return await self._get_model(
            self.GAMECMS_HACS_AUTHORITY,
            "hi/Progression/file/Csr/Calendars/CsrSeasonCalendar.json",
            CsrSeasonCalendar,
        )

    async def get_season_calendar(self) -> SeasonCalendar:
        """Get IDs and dates for past/current reward track events/operations.

        Reward tracks are the progression systems that allow players to earn
        rewards from the XP earned by playing the game.

        Returns:
            The calendar of reward tracks.
        """
        return await self._get_model(
            self.GAMECMS_HACS_AUTHORITY,
            "hi/progression/file/calendars/seasons/seasoncalendar.json",
            SeasonCalendar,
        )

    async def get_career_reward_track(self) -> CareerRewardTrack:
        """Get details for the career rank progression reward track.

        Returns:
            The career rank reward track.
        """
        return await self._get_model(
            self.GAMECMS_HACS_AUTHORITY,
            "hi/Progression/file/RewardTracks/CareerRanks/careerRank1.json",
            CareerRewardTrack,
        )

    async def get_operation_reward_track(
        self,
        reward_track_path: str,
    ) -> OperationRewardTrack:
        """Get details for a single operation reward track.

        Args:
            reward_track_path: The relative path to the operation reward track
                file, such as "RewardTracks/Operations/S05OpPassM01.json".

        Returns:
            The operation reward track definition.
        """
        return await self._get_model(
            self.GAMECMS_HACS_AUTHORITY,
            f"hi/Progression/file/{reward_track_path.lstrip('/')}",
            OperationRewardTrack,
        )

    async def get_image(self, relative_path: str) -> bytes:
        """Get an image from the game content management service.

        Args:
            relative_path: The relative path to the image, such as
                "career_rank/ProgressWidget/272_Hero.png".

        Returns:
            The image data.
        """
        resp = await self._get(
            self.GAMECMS_HACS_AUTHORITY,
            f"hi/images/file/{relative_path.lstrip('/')}",
            headers={"Accept": "image/*"},
        )
        return await resp.read()
