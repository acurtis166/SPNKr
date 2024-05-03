"""Logic for obtaining API credentials."""

from spnkr.auth.app import AzureApp
from spnkr.auth.core import authenticate_player, refresh_player_tokens
from spnkr.auth.halo import ClearanceToken, SpartanToken
from spnkr.auth.player import AuthenticatedPlayer

__all__ = [
    "AzureApp",
    "AuthenticatedPlayer",
    "ClearanceToken",
    "SpartanToken",
    "authenticate_player",
    "refresh_player_tokens",
]
