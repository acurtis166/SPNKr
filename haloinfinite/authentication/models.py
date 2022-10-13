"""Authentication Models."""

from dataclasses import dataclass, field
import datetime as dt

from haloinfinite.models import SnakeModel, Date, PascalModel
from haloinfinite import util


@dataclass
class XTokenResponse(PascalModel):
    issue_instant: dt.datetime
    not_after: dt.datetime
    token: str

    def is_valid(self) -> bool:
        return self.not_after > util.utc_now()


@dataclass
class XAUDisplayClaims(SnakeModel):
    xui: list[dict[str, str]]


@dataclass
class XAUResponse(XTokenResponse):
    display_claims: XAUDisplayClaims


@dataclass
class XSTSDisplayClaims(SnakeModel):
    xui: list[dict[str, str]]


@dataclass
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


@dataclass
class OAuth2TokenResponse(SnakeModel):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str | None
    user_id: str
    issued: dt.datetime = field(default_factory=util.utc_now)

    def is_valid(self) -> bool:
        return (self.issued + dt.timedelta(seconds=self.expires_in)) > util.utc_now()


@dataclass
class SpartanTokenResponse(PascalModel):
    expires_utc: Date
    spartan_token: str
    token_duration: dt.timedelta

    def is_valid(self) -> bool:
        return self.expires_utc.iso_8601_date > util.utc_now()


@dataclass
class ClearanceTokenResponse(PascalModel):
    flight_configuration_id: str
    
