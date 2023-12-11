"""Profile data services."""

from typing import Iterable

from ..models.profile import User
from ..xuid import unwrap_xuid, wrap_xuid
from .base import BaseService

_HOST = "https://profile.svc.halowaypoint.com"


class ProfileService(BaseService):
    """Profile data services."""

    async def _get_user(self, user: str) -> User:
        return User(**await self._get_json(f"{_HOST}/users/{user}"))

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
        """
        if isinstance(xuids, str):
            raise TypeError("`xuids` must be an iterable of XUIDs, got `str`")
        if not xuids:
            return []
        url = f"{_HOST}/users"
        params = {"xuids": [unwrap_xuid(x) for x in xuids]}
        data = await self._get_json(url, params=params)
        return [User(**u) for u in data]
