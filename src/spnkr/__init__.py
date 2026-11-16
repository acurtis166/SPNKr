"""Python SDK for requesting Halo Infinite multiplayer data"""

from spnkr.auth import AzureApp, authenticate_player, refresh_player_tokens
from spnkr.client import HaloInfiniteClient
from spnkr.errors import (
    APIAuthenticationError,
    APIAuthorizationError,
    APIError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
    FilmReadError,
    InvalidXuidError,
    OAuth2Error,
    SPNKrError,
)

__all__ = [
    "APIAuthenticationError",
    "APIAuthorizationError",
    "APIError",
    "APINotFoundError",
    "APIRateLimitError",
    "APIServerError",
    "AzureApp",
    "FilmReadError",
    "HaloInfiniteClient",
    "InvalidXuidError",
    "OAuth2Error",
    "SPNKrError",
    "authenticate_player",
    "refresh_player_tokens",
]
