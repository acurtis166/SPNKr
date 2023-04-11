"""Authentication response data models."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from dateutil.parser import isoparse


@dataclass(frozen=True, slots=True)
class DisplayClaims:
    """Represents the display claims returned from an X token request.

    Attributes:
        xui: The list of Xbox user information key-value pairs.
    """

    xui: list[dict[str, str]]

    @classmethod
    def from_dict(cls, data: dict) -> DisplayClaims:
        """Parse a DisplayClaims object from a dictionary."""
        return cls(xui=data["xui"])


@dataclass(frozen=True, slots=True)
class XAUResponse:
    """Represents the response from an Xbox user request.

    Attributes:
        raw: The raw response dictionary.
        token: The Xbox user token.
    """

    raw: dict
    token: str

    @classmethod
    def from_dict(cls, data: dict) -> XAUResponse:
        """Parse an XAUResponse from a dictionary."""
        return cls(raw=data, token=data["Token"])


@dataclass(frozen=True, slots=True)
class XSTSResponse:
    """Represents the response from an XSTS token request.

    Attributes:
        raw: The raw response dictionary.
        token: The XSTS token.
        display_claims: The display claims returned from the request. These
            contain information about the authenticated user.
    """

    raw: dict
    token: str
    display_claims: DisplayClaims

    @property
    def xuid(self) -> str:
        """The ID of the authenticated user."""
        return self.display_claims.xui[0]["xid"]

    @property
    def userhash(self) -> str:
        """The user hash of the user. Used for XBL authentication."""
        return self.display_claims.xui[0]["uhs"]

    @property
    def gamertag(self) -> str:
        """The gamertag of the authenticated user."""
        return self.display_claims.xui[0]["gtg"]

    @property
    def authorization_header_value(self) -> str:
        """The value passed in the Authorization header for XBL requests."""
        return f"XBL3.0 x={self.userhash};{self.token}"

    @classmethod
    def from_dict(cls, data: dict) -> XSTSResponse:
        """Parse an XSTSResponse from a dictionary."""
        return cls(
            raw=data,
            token=data["Token"],
            display_claims=DisplayClaims.from_dict(data["DisplayClaims"]),
        )


@dataclass(frozen=True, slots=True)
class OAuth2TokenResponse:
    """Response resulting from a request for an OAuth2 token.

    This is the root token used to authenticate an application. It is used to
    request an XToken, which is used to authenticate a user for Xbox Live.

    Attributes:
        raw: The raw response data.
        access_token: The access token.
        refresh_token: The refresh token.
    """

    raw: dict
    access_token: str
    refresh_token: str

    @classmethod
    def from_dict(cls, data: dict) -> OAuth2TokenResponse:
        """Parse an OAuth2TokenResponse from a dictionary."""
        return cls(
            raw=data,
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
        )


@dataclass(frozen=True, slots=True)
class SpartanTokenResponse:
    """Response resulting from a request for a Spartan token.

    This provides the primary means of authenticating with the Halo Infinite
    API.

    Attributes:
        raw: The raw response data.
        expires_utc: The expiration time of the token.
        token: The Spartan token.
    """

    raw: dict
    expires_utc: dt.datetime
    token: str

    @classmethod
    def from_dict(cls, data: dict) -> SpartanTokenResponse:
        """Parse a SpartanTokenResponse from a dictionary."""
        return cls(
            raw=data,
            expires_utc=isoparse(data["ExpiresUtc"]["ISO8601Date"]),
            token=data["SpartanToken"],
        )


@dataclass(frozen=True, slots=True)
class ClearanceTokenResponse:
    """A Halo Infinite clearance token response.

    A clearance token is required for some API endpoints.

    Attributes:
        raw: The raw response data.
        token: The flight configuration ID. This is described as the
            "clearance token".
    """

    raw: dict
    token: str

    @classmethod
    def from_dict(cls, data: dict) -> ClearanceTokenResponse:
        """Parse a ClearanceTokenResponse from a dictionary."""
        return cls(data, data["FlightConfigurationId"])
