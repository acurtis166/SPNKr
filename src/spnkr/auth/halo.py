"""Retrieve Halo Infinite authentication tokens."""

import datetime as dt
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession


@dataclass(frozen=True)
class SpartanToken:
    """Response resulting from a request for a Spartan token.

    This provides the primary means of authenticating with the Halo Infinite
    API. The tokens are valid for 4 hours.

    Attributes:
        raw: The raw, deserialized JSON response.
    """

    raw: dict[str, Any]

    @property
    def token(self) -> str:
        """The spartan token value."""
        return self.raw["SpartanToken"]

    @property
    def expires_at(self) -> dt.datetime:
        """The UTC datetime at which the Spartan token expires."""
        return dt.datetime.fromisoformat(self.raw["ExpiresUtc"]["ISO8601Date"])


@dataclass(frozen=True)
class ClearanceToken:
    """A Halo Infinite clearance token response.

    A clearance token is required for some API endpoints.

    Attributes:
        raw: The raw, deserialized JSON response.
    """

    raw: dict[str, Any]

    @property
    def token(self) -> str:
        """The flight configuration ID."""
        return self.raw["FlightConfigurationId"]


async def request_spartan_token(
    session: ClientSession, halo_xsts_token: str
) -> SpartanToken:
    """Request a spartan token for authentication with Halo Infinite endpoints.

    Args:
        session: The aiohttp session to use.
        halo_xsts_token: An XSTS token scoped to Halo Waypoint.

    Returns:
        The spartan token response.
    """
    url = "https://settings.svc.halowaypoint.com/spartan-token"
    headers = {"Accept": "application/json"}
    js = {
        "Audience": "urn:343:s3:services",
        "MinVersion": "4",
        "Proof": [
            {
                "Token": halo_xsts_token,
                "TokenType": "Xbox_XSTSv3",
            }
        ],
    }
    response = await session.post(url, headers=headers, json=js)
    return SpartanToken(await response.json())


async def request_clearance_token(
    session: ClientSession, spartan_token: str
) -> ClearanceToken:
    """Request a clearance token required for some Halo Infinite endpoints.

    Args:
        session: The aiohttp session to use.
        spartan_token: The spartan token to use.

    Returns:
        The clearance token response.
    """
    url = (
        "https://settings.svc.halowaypoint.com/oban/flight-configurations/"
        "titles/hi/audiences/RETAIL/active"
    )
    headers = {"x-343-authorization-spartan": spartan_token}
    response = await session.get(url, headers=headers)
    return ClearanceToken(await response.json())
