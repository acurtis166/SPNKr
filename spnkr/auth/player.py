"""Information about an authenticated player."""

import datetime as dt
from dataclasses import dataclass

from .halo import ClearanceToken, SpartanToken


@dataclass(frozen=True)
class AuthenticatedPlayer:
    """Information about an authenticated player.

    Attributes:
        player_id: Xbox Live ID of the player.
        gamertag: The player's gamertag.
        spartan_token: An expirable Spartan token required for all API
            endpoints.
        clearance_token: A clearance token required for some API endpoints.
    """

    player_id: str
    """Xbox Live ID of the player."""
    gamertag: str
    """The player's gamertag."""
    spartan_token: SpartanToken
    """An expirable Spartan token required for all API endpoints."""
    clearance_token: ClearanceToken
    """A clearance token required for some API endpoints."""
    xbl_authorization_header_value: str
    """The value to pass when making requests to the Xbox Live API."""

    @property
    def is_valid(self) -> bool:
        """Whether the player's Spartan token is still valid."""
        return self.spartan_token.expires_at > dt.datetime.now(dt.timezone.utc)
