"""Logic for obtaining API credentials."""

from spnkr.auth.app import AzureApp
from spnkr.auth.core import authenticate_player, refresh_player_tokens
from spnkr.auth.halo import ClearanceToken, SpartanToken
from spnkr.auth.player import AuthenticatedPlayer
from spnkr.auth.provider import RefreshTokenProvider, StaticTokenProvider, TokenProvider

__all__ = [
    "AuthenticatedPlayer",
    "AzureApp",
    "ClearanceToken",
    "RefreshTokenProvider",
    "SpartanToken",
    "StaticTokenProvider",
    "TokenProvider",
    "authenticate_player",
    "refresh_player_tokens",
]
