"""Profile data services."""

from typing import Any, Iterable

from ..xuid import unwrap_xuid, wrap_xuid
from .base import BaseService

_HOST = "https://profile.svc.halowaypoint.com"


class ProfileService(BaseService):
    """Profile data services."""

    async def _get_user(self, user: str) -> dict[str, Any]:
        return await self._get(f"{_HOST}/users/{user}")

    async def get_current_user(self) -> dict[str, Any]:
        """Get the current user profile.

        Parsers:
            - [User][spnkr.parsers.pydantic.profile.User]
            - [parse_user][spnkr.parsers.records.profile.parse_user]

        Returns:
            The user.
        """
        return await self._get_user("me")

    async def get_user_by_gamertag(self, gamertag: str) -> dict[str, Any]:
        """Get user profile for the given gamertag.

        Args:
            gamertag: The gamertag of the player.

        Parsers:
            - [User][spnkr.parsers.pydantic.profile.User]
            - [parse_user][spnkr.parsers.records.profile.parse_user]

        Returns:
            The user.
        """
        return await self._get_user(f"gt({gamertag})")

    async def get_user_by_id(self, xuid: str | int) -> dict[str, Any]:
        """Get user profile for the given Xbox Live ID.

        Args:
            xuid: The Xbox Live ID of the player.

        Parsers:
            - [User][spnkr.parsers.pydantic.profile.User]
            - [parse_user][spnkr.parsers.records.profile.parse_user]

        Returns:
            The user.
        """
        return await self._get_user(wrap_xuid(xuid))

    async def get_users_by_id(
        self, xuids: Iterable[str | int]
    ) -> list[dict[str, Any]]:
        """Get user profiles for the given list of Xbox Live IDs.

        Args:
            xuids: The Xbox Live IDs of the players.

        Parsers:
            - [User][spnkr.parsers.pydantic.profile.User]
            - [parse_users][spnkr.parsers.records.profile.parse_users]

        Returns:
            A list of users.
        """
        url = f"{_HOST}/users"
        params = {"xuids": [unwrap_xuid(x) for x in xuids]}
        return await self._get(url, params=params)
