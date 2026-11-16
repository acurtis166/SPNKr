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
        self.spartan_token = spartan_token
        self.clearance_token = clearance_token
        self._max_retries = max(0, max_retries)
        self._requests_per_second = requests_per_second

        self._session.headers["Accept"] = "application/json"

    @property
    def session(self) -> "ClientSession | CachedSession":
        return self._session

    @property
    def spartan_token(self) -> str:
        return self._spartan_token

    @spartan_token.setter
    def spartan_token(self, value: str) -> None:
        self._spartan_token = value
        self.session.headers["x-343-authorization-spartan"] = self._spartan_token

    @property
    def clearance_token(self) -> str:
        return self._clearance_token

    @clearance_token.setter
    def clearance_token(self, value: str) -> None:
        self._clearance_token = value
        self.session.headers["343-clearance"] = self._clearance_token

    @cached_property
    def profile(self) -> ProfileService:
        """Profile data service. Get user data, such as XUIDs/gamertags."""
        return ProfileService(
            self._session, self._max_retries, self._requests_per_second
        )

    @cached_property
    def gamecms_hacs(self) -> GameCmsHacsService:
        """Game content management data service (e.g., medal metadata)"""
        return GameCmsHacsService(
            self._session, self._max_retries, self._requests_per_second
        )

    @cached_property
    def skill(self) -> SkillService:
        """Skill data service. Retrieve MMR and CSR data by match or playlist."""
        return SkillService(self._session, self._max_retries, self._requests_per_second)

    @cached_property
    def stats(self) -> StatsService:
        """Stats data service. Retrieve match history and match stats."""
        return StatsService(self._session, self._max_retries, self._requests_per_second)

    @cached_property
    def discovery_ugc(self) -> DiscoveryUgcService:
        """User-generated content discovery data service (maps, modes, etc.)."""
        return DiscoveryUgcService(
            self._session, self._max_retries, self._requests_per_second
        )

    @cached_property
    def economy(self) -> EconomyService:
        """Store and customization data service."""
        return EconomyService(
            self._session, self._max_retries, self._requests_per_second
        )
