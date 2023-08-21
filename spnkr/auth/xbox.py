"""Xbox Live authentication."""

from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession

from ..xuid import XUID


@dataclass(frozen=True)
class XAUResponse:
    """Represents the response from an Xbox user request."""

    raw: dict[str, Any]

    @property
    def token(self) -> str:
        """The Xbox user token."""
        return self.raw["Token"]


@dataclass(frozen=True)
class XSTSResponse:
    """Represents the response from an XSTS token request."""

    raw: dict[str, Any]

    @property
    def token(self) -> str:
        """The XSTS token."""
        return self.raw["Token"]

    @property
    def xui(self) -> dict[str, str]:
        """The Xbox user information."""
        return self.raw["DisplayClaims"]["xui"][0]

    @property
    def xuid(self) -> XUID:
        """The ID of the authenticated user."""
        # TODO: This isn't always available.
        return XUID(self.xui["xid"])

    @property
    def gamertag(self) -> str:
        """The gamertag of the authenticated user."""
        # TODO: This isn't always available.
        return self.xui["gtg"]


async def request_user_token(
    session: ClientSession,
    access_token: str,
    relying_party: str = "http://auth.xboxlive.com",
) -> XAUResponse:
    """Authenticate via OAuth access token and receive a user token.

    Args:
        session: The aiohttp session to use.
        access_token: The OAuth access token to use.
        relying_party: The relying party to use.

    Returns:
        The user token response.
    """
    url = "https://user.auth.xboxlive.com/user/authenticate"
    headers = {"x-xbl-contract-version": "1"}
    js = {
        "RelyingParty": relying_party,
        "TokenType": "JWT",
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={access_token}",
        },
    }
    async with session.post(url, json=js, headers=headers) as resp:
        return XAUResponse(await resp.json())


async def request_xsts_token(
    session: ClientSession, user_token: str, relying_party: str
) -> XSTSResponse:
    """Authorize via user token and receive final X token.

    Args:
        session: The aiohttp session to use.
        user_token: The user token to use.
        relying_party: The relying party to use.

    Returns:
        The XSTS token response.
    """
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"
    headers = {"x-xbl-contract-version": "1"}
    js = {
        "RelyingParty": relying_party,
        "TokenType": "JWT",
        "Properties": {
            "UserTokens": [user_token],
            "SandboxId": "RETAIL",
        },
    }
    async with session.post(url, json=js, headers=headers) as resp:
        return XSTSResponse(await resp.json())
