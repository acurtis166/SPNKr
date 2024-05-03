"""Information about an authenticated player."""

import datetime as dt
from dataclasses import dataclass

from spnkr.auth.halo import ClearanceToken, SpartanToken


@dataclass(frozen=True)
class AuthenticatedPlayer:
    """Information about an authenticated player.

    Attributes:
        player_id: Xbox Live ID of the player.
        gamertag: The player's gamertag.
        spartan_token: An expirable Spartan token required for all API
            endpoints.
        clearance_token: A clearance token required for some API endpoints.
        xbl_authorization_header_value: The value for the authorization header
            passed when making requests to the Xbox Live API.
    """

    player_id: str
    gamertag: str
    spartan_token: SpartanToken
    clearance_token: ClearanceToken
    xbl_authorization_header_value: str

    @property
    def is_valid(self) -> bool:
        """Whether the player's Spartan token is still valid."""
        return self.spartan_token.expires_at > dt.datetime.now(dt.timezone.utc)
