"""Provides a client for the Halo Infinite API."""

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
