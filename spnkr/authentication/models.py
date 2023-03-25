"""Authentication Models."""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, field

from spnkr import util
from spnkr.models import Date
from spnkr.parsers import parse_iso_datetime, parse_iso_duration


@dataclass(frozen=True)
class XTokenResponse:
    issue_instant: dt.datetime
    not_after: dt.datetime
    token: str

    @classmethod
    def from_dict(cls, data: dict) -> XTokenResponse:
        """Parse an XTokenResponse from a dictionary."""
        return cls(
            issue_instant=parse_iso_datetime(data["IssueInstant"]),
            not_after=parse_iso_datetime(data["NotAfter"]),
            token=data["Token"],
        )

    def is_valid(self) -> bool:
        return self.not_after > util.utc_now()


@dataclass(frozen=True)
class XAUDisplayClaims:
    xui: list[dict[str, str]]

    @classmethod
    def from_dict(cls, data: dict) -> XAUDisplayClaims:
        """Parse an XAUDisplayClaims from a dictionary."""
        return cls(xui=data["xid"])


@dataclass(frozen=True)
class XAUResponse(XTokenResponse):
    display_claims: XAUDisplayClaims

    @classmethod
    def from_dict(cls, data: dict) -> XAUResponse:
        """Parse an XAUResponse from a dictionary."""
        return cls(
            issue_instant=parse_iso_datetime(data["IssueInstant"]),
            not_after=parse_iso_datetime(data["NotAfter"]),
            token=data["Token"],
            display_claims=XAUDisplayClaims.from_dict(data["DisplayClaims"]),
        )


@dataclass(frozen=True)
class XSTSDisplayClaims:
    xui: list[dict[str, str]]

    @classmethod
    def from_dict(cls, data: dict) -> XSTSDisplayClaims:
        """Parse an XSTSDisplayClaims from a dictionary."""
        return cls(xui=data["xui"])


@dataclass(frozen=True)
class XSTSResponse(XTokenResponse):
    display_claims: XSTSDisplayClaims

    @property
    def xuid(self) -> str:
        return self.display_claims.xui[0]["xid"]

    @property
    def userhash(self) -> str:
        return self.display_claims.xui[0]["uhs"]

    @property
    def gamertag(self) -> str:
        return self.display_claims.xui[0]["gtg"]

    @property
    def age_group(self) -> str:
        return self.display_claims.xui[0]["agg"]

    @property
    def privileges(self) -> str:
        return self.display_claims.xui[0]["prv"]

    @property
    def user_privileges(self) -> str:
        return self.display_claims.xui[0]["usr"]

    @property
    def authorization_header_value(self) -> str:
        return f"XBL3.0 x={self.userhash};{self.token}"

    @classmethod
    def from_dict(cls, data: dict) -> XSTSResponse:
        """Parse an XSTSResponse from a dictionary."""
        return cls(
            issue_instant=parse_iso_datetime(data["IssueInstant"]),
            not_after=parse_iso_datetime(data["NotAfter"]),
            token=data["Token"],
            display_claims=XSTSDisplayClaims.from_dict(data["DisplayClaims"]),
        )


@dataclass(frozen=True)
class OAuth2TokenResponse:
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str | None
    user_id: str
    issued: dt.datetime = field(init=False, default_factory=util.utc_now)

    @classmethod
    def from_dict(cls, data: dict) -> OAuth2TokenResponse:
        """Parse an OAuth2TokenResponse from a dictionary."""
        return cls(
            token_type=data["token_type"],
            expires_in=data["expires_in"],
            scope=data["scope"],
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            user_id=data["user_id"],
        )

    @classmethod
    def from_json(cls, data: str) -> OAuth2TokenResponse:
        """Parse an OAuth2TokenResponse from a JSON string."""
        return cls.from_dict(json.loads(data))

    def is_valid(self) -> bool:
        return (
            self.issued + dt.timedelta(seconds=self.expires_in)
        ) > util.utc_now()

    def to_dict(self) -> dict:
        return {
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "scope": self.scope,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "user_id": self.user_id,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass(frozen=True)
class SpartanTokenResponse:
    expires_utc: Date
    spartan_token: str
    token_duration: dt.timedelta

    @classmethod
    def from_dict(cls, data: dict) -> SpartanTokenResponse:
        """Parse a SpartanTokenResponse from a dictionary."""
        return cls(
            expires_utc=Date.from_dict(data["ExpiresOn"]),
            spartan_token=data["Token"],
            token_duration=parse_iso_duration(data["TokenDuration"]),
        )

    def is_valid(self) -> bool:
        return self.expires_utc.iso_8601_date > util.utc_now()


@dataclass(frozen=True)
class ClearanceTokenResponse:
    flight_configuration_id: str

    @classmethod
    def from_dict(cls, data: dict) -> ClearanceTokenResponse:
        """Parse a ClearanceTokenResponse from a dictionary."""
        return cls(flight_configuration_id=data["FlightConfigurationId"])
