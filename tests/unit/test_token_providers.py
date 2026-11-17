"""Tests for token providers."""

import asyncio
import datetime as dt
from unittest.mock import MagicMock, patch

import pytest

from spnkr.auth import halo
from spnkr.auth.provider import RefreshTokenProvider, StaticTokenProvider, TokenProvider
from spnkr.errors import TokenError


def create_spartan_token(
    token: str, expires_at: str | None = None
) -> halo.SpartanToken:
    """Helper to create a SpartanToken for testing.

    Args:
        token: The token string value.
        expires_at: ISO8601 formatted expiration datetime. Defaults to far future.
    """
    if expires_at is None:
        expires_at = "2099-12-31T23:59:59Z"
    return halo.SpartanToken.model_validate(
        {
            "SpartanToken": token,
            "ExpiresUtc": {"ISO8601Date": expires_at},
            "TokenDuration": "PT3H59M49.4904271S",
        }
    )


class TestStaticTokenProvider:
    @pytest.mark.asyncio
    async def test_get_token(self):
        """Test that StaticTokenProvider returns the same token."""
        token = "test_token_123"
        provider = StaticTokenProvider(token)
        result = await provider.get_token()
        assert isinstance(result, halo.SpartanToken)
        assert result.spartan_token == token

    @pytest.mark.asyncio
    async def test_multiple_calls_same_token(self):
        """Test that multiple calls return the same token."""
        token = "test_token_123"
        provider = StaticTokenProvider(token)
        result1 = await provider.get_token()
        result2 = await provider.get_token()
        assert result1.spartan_token == result2.spartan_token == token

    def test_token_attribute(self):
        """Test accessing token directly."""
        token = "test_token_123"
        provider = StaticTokenProvider(token)
        assert provider.token == token

    @pytest.mark.asyncio
    async def test_implements_protocol(self):
        """Test that StaticTokenProvider implements TokenProvider protocol."""
        provider = StaticTokenProvider("token")
        assert isinstance(provider, TokenProvider)


class TestRefreshTokenProvider:
    @pytest.mark.asyncio
    async def test_get_token_exchanges_access_token(self):
        """Test that RefreshTokenProvider exchanges access token for spartan token."""

        async def get_access_token():
            return "access_token_123"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token") as mock_user,
            patch("spnkr.auth.provider.xbox.request_xsts_token") as mock_xsts,
            patch("spnkr.auth.provider.halo.request_spartan_token") as mock_spartan,
        ):
            mock_user.return_value = MagicMock(token="user_token")
            mock_xsts.return_value = MagicMock(token="xsts_token")
            mock_spartan.return_value = create_spartan_token("spartan_token_result")

            provider = RefreshTokenProvider(get_access_token)
            result = await provider.get_token()

            assert isinstance(result, halo.SpartanToken)
            assert result.spartan_token == "spartan_token_result"
            mock_user.assert_called_once()
            mock_xsts.assert_called_once()
            mock_spartan.assert_called_once()

    @pytest.mark.asyncio
    async def test_caches_spartan_token(self):
        """Test that spartan token is cached after first call."""
        call_count = 0

        async def get_access_token():
            nonlocal call_count
            call_count += 1
            return f"access_token_{call_count}"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token") as mock_user,
            patch("spnkr.auth.provider.xbox.request_xsts_token") as mock_xsts,
            patch("spnkr.auth.provider.halo.request_spartan_token") as mock_spartan,
        ):
            mock_user.return_value = MagicMock(token="user_token")
            mock_xsts.return_value = MagicMock(token="xsts_token")
            mock_spartan.return_value = create_spartan_token("spartan_token_result")

            provider = RefreshTokenProvider(get_access_token)
            result1 = await provider.get_token()
            result2 = await provider.get_token()

            assert (
                result1.spartan_token == result2.spartan_token == "spartan_token_result"
            )
            assert call_count == 1  # Only called once

    @pytest.mark.asyncio
    async def test_refresh_calls_function_again(self):
        """Test that refresh forces a new access token and spartan token exchange."""
        call_count = 0

        async def get_access_token():
            nonlocal call_count
            call_count += 1
            return f"access_token_{call_count}"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token") as mock_user,
            patch("spnkr.auth.provider.xbox.request_xsts_token") as mock_xsts,
            patch("spnkr.auth.provider.halo.request_spartan_token") as mock_spartan,
        ):
            mock_user.return_value = MagicMock(token="user_token")
            mock_xsts.return_value = MagicMock(token="xsts_token")

            call_sequence = 0

            async def mock_spartan_func(session, xsts):
                nonlocal call_sequence
                call_sequence += 1
                return create_spartan_token(f"spartan_token_{call_sequence}")

            mock_spartan.side_effect = mock_spartan_func

            provider = RefreshTokenProvider(get_access_token)
            result1 = await provider.get_token()
            result2 = await provider.refresh()
            result3 = await provider.get_token()

            assert result1.spartan_token == "spartan_token_1"
            assert result2.spartan_token == "spartan_token_2"
            assert result3.spartan_token == "spartan_token_2"
            assert call_count == 2

    def test_non_async_function_raises_type_error(self):
        """Test that providing a non-async function raises TypeError."""

        def sync_func():
            return "token"

        with pytest.raises(
            TypeError, match="must be an async function or async callable class"
        ):
            RefreshTokenProvider(sync_func)

    @pytest.mark.asyncio
    async def test_async_callable_class(self):
        """Test that an async callable class works as get_access_token."""

        class AsyncTokenGetter:
            async def __call__(self):
                return "access_token_from_class"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token") as mock_user,
            patch("spnkr.auth.provider.xbox.request_xsts_token") as mock_xsts,
            patch("spnkr.auth.provider.halo.request_spartan_token") as mock_spartan,
        ):
            mock_user.return_value = MagicMock(token="user_token")
            mock_xsts.return_value = MagicMock(token="xsts_token")
            mock_spartan.return_value = create_spartan_token("spartan_token_from_class")

            getter = AsyncTokenGetter()
            provider = RefreshTokenProvider(getter)
            result = await provider.get_token()

            assert result.spartan_token == "spartan_token_from_class"
            mock_user.assert_called_once_with(
                mock_user.call_args[0][0], "access_token_from_class"
            )

    @pytest.mark.asyncio
    async def test_has_refresh_method(self):
        """Test that RefreshTokenProvider has refresh method."""

        async def get_access_token():
            return "access_token"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token"),
            patch("spnkr.auth.provider.xbox.request_xsts_token"),
            patch("spnkr.auth.provider.halo.request_spartan_token"),
        ):
            provider = RefreshTokenProvider(get_access_token)
            assert hasattr(provider, "refresh")
            assert callable(provider.refresh)

    @pytest.mark.asyncio
    async def test_token_error_on_access_token_failure(self):
        """Test that TokenError is raised when get_access_token fails."""

        async def get_access_token():
            raise ValueError("Access token retrieval failed")

        provider = RefreshTokenProvider(get_access_token)
        with pytest.raises(TokenError, match="Failed to obtain Spartan token"):
            await provider.get_token()

    @pytest.mark.asyncio
    async def test_token_error_on_xbox_failure(self):
        """Test that TokenError is raised when xbox requests fail."""

        async def get_access_token():
            return "access_token_123"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token") as mock_user,
        ):
            mock_user.side_effect = ValueError("Xbox request failed")

            provider = RefreshTokenProvider(get_access_token)
            with pytest.raises(TokenError, match="Failed to obtain Spartan token"):
                await provider.get_token()

    @pytest.mark.asyncio
    async def test_concurrent_calls_use_lock(self):
        """Test that concurrent get_token calls are serialized by the lock."""
        call_count = 0

        async def get_access_token():
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)  # Simulate async work
            return f"access_token_{call_count}"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token") as mock_user,
            patch("spnkr.auth.provider.xbox.request_xsts_token") as mock_xsts,
            patch("spnkr.auth.provider.halo.request_spartan_token") as mock_spartan,
        ):
            mock_user.return_value = MagicMock(token="user_token")
            mock_xsts.return_value = MagicMock(token="xsts_token")
            mock_spartan.return_value = create_spartan_token("spartan_token_result")

            provider = RefreshTokenProvider(get_access_token)

            # Launch multiple concurrent calls
            results = await asyncio.gather(
                provider.get_token(),
                provider.get_token(),
                provider.get_token(),
            )

            # All should return the same token
            assert all(r.spartan_token == "spartan_token_result" for r in results)

            # But the access token function should only be called once
            # because the lock prevents concurrent token fetches
            assert call_count == 1

    @pytest.mark.asyncio
    async def test_expired_token_is_refreshed(self):
        """Test that expired tokens are automatically refreshed on get_token."""
        call_count = 0

        async def get_access_token():
            nonlocal call_count
            call_count += 1
            return f"access_token_{call_count}"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token") as mock_user,
            patch("spnkr.auth.provider.xbox.request_xsts_token") as mock_xsts,
            patch("spnkr.auth.provider.halo.request_spartan_token") as mock_spartan,
        ):
            mock_user.return_value = MagicMock(token="user_token")
            mock_xsts.return_value = MagicMock(token="xsts_token")

            # Create token that expires in the past
            past_expiry = (
                dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=1)
            ).isoformat()
            expired_token = create_spartan_token("expired_spartan_token", past_expiry)

            # Create a future token for the refresh
            future_expiry = (
                dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=4)
            ).isoformat()
            fresh_token = create_spartan_token("fresh_spartan_token", future_expiry)

            mock_spartan.side_effect = [expired_token, fresh_token]

            provider = RefreshTokenProvider(get_access_token)

            # First call gets the expired token
            result1 = await provider.get_token()
            assert result1.spartan_token == "expired_spartan_token"

            # Second call should detect expiry and fetch a new one
            result2 = await provider.get_token()
            assert result2.spartan_token == "fresh_spartan_token"

            # Verify the access token function was called twice
            assert call_count == 2

    @pytest.mark.asyncio
    async def test_token_expiring_soon_is_refreshed(self):
        """Test that tokens expiring within 60 seconds are automatically refreshed."""
        call_count = 0

        async def get_access_token():
            nonlocal call_count
            call_count += 1
            return f"access_token_{call_count}"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token") as mock_user,
            patch("spnkr.auth.provider.xbox.request_xsts_token") as mock_xsts,
            patch("spnkr.auth.provider.halo.request_spartan_token") as mock_spartan,
        ):
            mock_user.return_value = MagicMock(token="user_token")
            mock_xsts.return_value = MagicMock(token="xsts_token")

            # Create token that expires in 30 seconds
            soon_expiry = (
                dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=30)
            ).isoformat()
            soon_expired_token = create_spartan_token(
                "soon_to_expire_token", soon_expiry
            )

            # Create a fresh token for the refresh
            future_expiry = (
                dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=4)
            ).isoformat()
            fresh_token = create_spartan_token(
                "fresh_token_after_refresh", future_expiry
            )

            mock_spartan.side_effect = [soon_expired_token, fresh_token]

            provider = RefreshTokenProvider(get_access_token)

            # First call gets the token expiring soon
            result1 = await provider.get_token()
            assert result1.spartan_token == "soon_to_expire_token"

            # Second call should detect it expires soon and refresh
            result2 = await provider.get_token()
            assert result2.spartan_token == "fresh_token_after_refresh"

            # Verify the access token function was called twice
            assert call_count == 2


class TestTokenProviderProtocol:
    @pytest.mark.asyncio
    async def test_static_provider_protocol_check(self):
        """Test that StaticTokenProvider satisfies TokenProvider protocol."""
        provider = StaticTokenProvider("test_token")
        # Check that the protocol is satisfied
        assert hasattr(provider, "get_token")
        # Call the method to ensure it's callable
        result = await provider.get_token()
        assert result.spartan_token == "test_token"

    @pytest.mark.asyncio
    async def test_refresh_provider_protocol_check(self):
        """Test that RefreshTokenProvider satisfies TokenProvider protocol."""

        async def get_access_token():
            return "access_token"

        with (
            patch("spnkr.auth.provider.xbox.request_user_token"),
            patch("spnkr.auth.provider.xbox.request_xsts_token"),
            patch("spnkr.auth.provider.halo.request_spartan_token") as mock_spartan,
        ):
            mock_spartan.return_value = create_spartan_token("spartan_token")

            provider = RefreshTokenProvider(get_access_token)
            # Check that the protocol is satisfied
            assert hasattr(provider, "get_token")
            # Call the method to ensure it's callable
            result = await provider.get_token()
            assert result.spartan_token == "spartan_token"
