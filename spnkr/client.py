"""Provides a client for the Halo Infinite API."""

import asyncio
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aiohttp_client_cache.session import CachedSession

from spnkr.services import (
    DiscoveryUgcService,
    EconomyService,
    GameCmsHacsService,
    ProfileService,
    SkillService,
    StatsService,
)
from spnkr.models.economy import OperationPassSummary

__all__ = ["HaloInfiniteClient"]


class HaloInfiniteClient:
    """A client for the Halo Infinite API."""

    def __init__(
        self,
        session: "ClientSession | CachedSession",
        spartan_token: str,
        clearance_token: str,
        requests_per_second: int = 5,
    ) -> None:
        """Initialize a client for the Halo Infinite API.

        Args:
            session: The `aiohttp.ClientSession` to use. Support for caching is
                available via a `CachedSession` from `aiohttp-client-cache`.
            spartan_token: The spartan token used to authenticate with the API.
            clearance_token: The clearance token used to authenticate with the API.
            requests_per_second: The rate limit to use. Note that this rate
                limit is enforced per service, not globally. Defaults to 5
                requests per second.
        """
        self._session = session
        self._requests_per_second = requests_per_second
        self.set_tokens(spartan_token, clearance_token)

    def set_tokens(self, spartan_token: str, clearance_token: str) -> None:
        """Update the tokens used for authentication.

        This method is called during initialization, but can be used after
        initialization to replace expiring tokens.

        Args:
            spartan_token: The spartan token used to authenticate with the API.
            clearance_token: The clearance token used to authenticate with the API.
        """
        update = {
            "Accept": "application/json",
            "x-343-authorization-spartan": spartan_token,
            "343-clearance": clearance_token,
        }
        self._session.headers.update(update)

    async def get_operation_passes(
        self,
        player: str | int,
        *,
        language: str | None = None,
    ) -> tuple[OperationPassSummary, ...]:
        """Get summarized operation pass progress for a player.

        This helper combines live Economy progress with static GameCMS reward
        track metadata.

        Args:
            player: Xbox Live ID or gamertag of the player to retrieve data
                for.
            language: Optional BCP-47 locale used to select translated names
                and descriptions from the GameCMS metadata when available.

        Returns:
            The player's available operation passes with summarized progress.
        """
        operations = await (await self.economy.get_player_reward_track_operations(player)).parse()
        track_definitions = await asyncio.gather(
            *(
                self._get_operation_reward_track_definition(operation.reward_track_path)
                for operation in operations.operation_reward_tracks
            )
        )
        return tuple(
            OperationPassSummary.from_models(
                operation,
                definition,
                is_active=(
                    operation.reward_track_path == operations.active_operation_reward_track_path
                ),
                language=language,
            )
            for operation, definition in zip(
                operations.operation_reward_tracks,
                track_definitions,
            )
        )

    async def get_active_operation_pass(
        self,
        player: str | int,
        *,
        language: str | None = None,
    ) -> OperationPassSummary | None:
        """Get summarized progress for the player's active operation pass.

        Args:
            player: Xbox Live ID or gamertag of the player to retrieve data
                for.
            language: Optional BCP-47 locale used to select translated names
                and descriptions from the GameCMS metadata when available.

        Returns:
            The active operation pass summary, if one is available.
        """
        operations = await (await self.economy.get_player_reward_track_operations(player)).parse()
        active_operation = operations.active
        if active_operation is None:
            return None
        definition = await self._get_operation_reward_track_definition(
            active_operation.reward_track_path
        )
        return OperationPassSummary.from_models(
            active_operation,
            definition,
            is_active=True,
            language=language,
        )

    async def _get_operation_reward_track_definition(self, reward_track_path: str):
        try:
            return await (
                await self.gamecms_hacs.get_operation_reward_track(reward_track_path)
            ).parse()
        except Exception:
            return None

    @cached_property
    def profile(self) -> ProfileService:
        """Profile data service. Get user data, such as XUIDs/gamertags."""
        return ProfileService(self._session, self._requests_per_second)

    @cached_property
    def gamecms_hacs(self) -> GameCmsHacsService:
        """Game content management data service (e.g., medal metadata)"""
        return GameCmsHacsService(self._session, self._requests_per_second)

    @cached_property
    def skill(self) -> SkillService:
        """Skill data service. Retrieve MMR and CSR data by match or playlist."""
        return SkillService(self._session, self._requests_per_second)

    @cached_property
    def stats(self) -> StatsService:
        """Stats data service. Retrieve match history and match stats."""
        return StatsService(self._session, self._requests_per_second)

    @cached_property
    def discovery_ugc(self) -> DiscoveryUgcService:
        """User-generated content discovery data service (maps, modes, etc.)."""
        return DiscoveryUgcService(self._session, self._requests_per_second)

    @cached_property
    def economy(self) -> EconomyService:
        """Store and customization data service."""
        return EconomyService(self._session, self._requests_per_second)
