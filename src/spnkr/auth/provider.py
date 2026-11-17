"""Token provider interface for Spartan token authentication."""

import asyncio
import functools
import inspect
from collections.abc import Awaitable, Callable
from typing import Protocol, runtime_checkable

from aiohttp import ClientSession

from spnkr.auth import halo, xbox
from spnkr.errors import TokenError


@runtime_checkable
class TokenProvider(Protocol):
    """Protocol for providing Spartan authentication tokens.

    A token provider is responsible for supplying Spartan tokens to the client.
    It can be as simple as a static token or as complex as handling
    automatic token refresh via MSAL or other identity providers.
    """

    async def get_token(self) -> str:
        """Get a Spartan authentication token.

        Returns:
            The token string to use for authentication.

        Raises:
            TokenError: If the token cannot be obtained.
        """
        ...


class StaticTokenProvider:
    """A token provider that always returns the same token.

    Attributes:
        token: The static token value.
    """

    def __init__(self, token: str) -> None:
        """Initialize a static token provider.

        Args:
            token: The token value to provide.
        """
        self.token = token

    async def get_token(self) -> str:
        """Get the static token.

        Returns:
            The token string.
        """
        return self.token


def _is_async_callable(obj) -> bool:
    while isinstance(obj, functools.partial):
        obj = obj.func

    return inspect.iscoroutinefunction(obj) or (
        callable(obj) and inspect.iscoroutinefunction(getattr(obj, "__call__", None))  # noqa
    )


class RefreshTokenProvider:
    """A token provider that uses an async callable for OAuth access token refresh.

    This provider accepts an async callable that returns an OAuth access token,
    then handles the full authentication chain internally (OAuth → User token →
    XSTS token → Spartan token). This simplifies the user experience by handling
    Halo-specific auth logic within the provider.

    Token caching is built-in: the spartan token is retrieved once and reused
    until `refresh()` is explicitly called.
    """

    _XSTS_V3_HALO_AUDIENCE = "https://prod.xsts.halowaypoint.com/"

    def __init__(self, get_access_token: Callable[[], "Awaitable[str]"]) -> None:
        """Initialize a refresh token provider.

        Args:
            get_access_token: An async callable that returns an OAuth access token.
                Can be an async function or an async callable class with __call__.
                The provider will exchange this for a Spartan token internally.

        Raises:
            TypeError: If get_access_token is not async callable.
        """
        if not _is_async_callable(get_access_token):
            raise TypeError(
                "get_access_token must be an async function or async callable class"
            )

        self._get_access_token = get_access_token
        self._spartan_token: str | None = None
        self._token_lock = asyncio.Lock()

    async def get_token(self) -> str:
        """Get a Spartan token, using cached value if available.

        The first call invokes the async callable to get an access token,
        then exchanges it for a Spartan token. Subsequent calls return the
        cached Spartan token until `refresh()` is called.

        Returns:
            The Spartan token string.

        Raises:
            TokenError: If the token cannot be obtained.
        """
        async with self._token_lock:
            if self._spartan_token is None:
                self._spartan_token = await self._fetch_spartan_token()
            return self._spartan_token

    async def refresh(self) -> str:
        """Refresh the Spartan token by obtaining a new access token and exchanging it.

        Returns:
            The new Spartan token string.

        Raises:
            TokenError: If the token cannot be obtained.
        """
        async with self._token_lock:
            self._spartan_token = await self._fetch_spartan_token()
            return self._spartan_token

    async def _fetch_spartan_token(self) -> str:
        """Fetch a new Spartan token by exchanging the access token.

        Returns:
            The Spartan token string.

        Raises:
            TokenError: If the token cannot be obtained.
        """
        try:
            access_token = await self._get_access_token()

            # For simplicity, just create a session for each periodic token fetch
            async with ClientSession() as session:
                user_token = await xbox.request_user_token(session, access_token)
                xsts_token = await xbox.request_xsts_token(
                    session, user_token.token, self._XSTS_V3_HALO_AUDIENCE
                )
                spartan_token = await halo.request_spartan_token(
                    session, xsts_token.token
                )
                return spartan_token.token
        except TokenError:
            # Re-raise TokenError as-is
            raise
        except Exception as e:
            # Wrap other exceptions in TokenError
            raise TokenError(f"Failed to obtain Spartan token: {e!s}") from e
