"""Retrieve Halo Infinite authentication tokens."""

import datetime as dt

from aiohttp import ClientSession
from pydantic import BaseModel, Field

from spnkr.models.base import PascalCaseModel


class ExpiresUtc(BaseModel, populate_by_name=True):
    """Expiration time model."""

    iso8601_date: dt.datetime = Field(alias="ISO8601Date")


class SpartanToken(PascalCaseModel):
    """Response resulting from a request for a Spartan token.

    This provides the primary means of authenticating with the Halo Infinite
    API. The tokens are valid for 4 hours.
    """

    spartan_token: str
    expires_utc: ExpiresUtc
    token_duration: dt.timedelta

    @property
    def expires_at(self) -> dt.datetime:
        """The UTC datetime at which the Spartan token expires."""
        return self.expires_utc.iso8601_date


class ClearanceToken(BaseModel, frozen=True):
    """A Halo Infinite clearance token response.

    A clearance token is required for some API endpoints.
    """

    flight_configuration_id: str = Field(alias="FlightConfigurationId")


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
    return SpartanToken.model_validate(await response.json())


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
    return ClearanceToken.model_validate(await response.json())
