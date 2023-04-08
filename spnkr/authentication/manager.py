"""Authenticate with Windows Live Server and Xbox Live."""

import datetime as dt
from dataclasses import dataclass, field

import aiohttp

from spnkr.authentication.app import AzureApp
from spnkr.authentication.models import (
    ClearanceTokenResponse,
    SpartanTokenResponse,
    XSTSResponse,
)
from spnkr.authentication.request import (
    generate_authorization_url,
    refresh_oauth_token,
    request_clearance_token,
    request_oauth_token,
    request_spartan_token,
    request_user_token,
    request_xsts_token,
)

XSTS_V3_XBOX_AUDIENCE = "http://xboxlive.com"
XSTS_V3_HALO_AUDIENCE = "https://prod.xsts.halowaypoint.com/"


async def authenticate(app: AzureApp) -> str:
    """Initial authentication of the `app` with Windows Live and Xbox Live.

    Request an OAuth token and return its refresh token.

    Args:
        app: The Azure AD application to authenticate.

    Returns:
        The refresh token for the OAuth token.
    """
    auth_code = _get_authorization_code(app)
    async with aiohttp.ClientSession() as session:
        oauth = await request_oauth_token(session, auth_code, app)
    return oauth.refresh_token


def _get_authorization_code(app: AzureApp) -> str:
    """Prompt the user for an authorization code."""
    auth_url = generate_authorization_url(app)
    print(auth_url)
    print(
        'Navigate to the above URL and copy the "code" parameter from the query string.'
    )
    return input("Enter the code...")


class TokenJar:
    """A collection of tokens.

    Attributes:
        xuid: The Xbox Live user ID.
        gamertag: The Xbox Live gamertag.
        xsts_authorization_header: The value of the XSTS authorization header.
        spartan_token: The spartan token.
        clearance_token: The clearance token.
        expires_utc: The expiration time of the tokens.
    """

    def __init__(
        self,
        xsts: XSTSResponse,
        spartan: SpartanTokenResponse,
        clearance: ClearanceTokenResponse,
    ) -> None:
        self.xuid = xsts.xuid
        self.gamertag = xsts.gamertag
        self.xsts_authorization_header = xsts.authorization_header_value
        self.spartan_token = spartan.token
        self.clearance_token = clearance.token
        self.expires_utc = spartan.expires_utc

    def is_valid(self) -> bool:
        """Check if the tokens are valid."""
        return self.expires_utc > dt.datetime.now(dt.timezone.utc)


@dataclass
class TokenManager:
    """Handles token retrieval and refresh.

    This assumes that the initial authentication has already been performed
    using the `authenticate` function.

    Attributes:
        session: The aiohttp session.
        app: The Azure AD application.
        refresh_token: The refresh token for the OAuth token.
        token_jar: The token jar. This is None until the first call to the
            `get_tokens` method.
    """

    session: aiohttp.ClientSession
    app: AzureApp
    refresh_token: str
    token_jar: TokenJar | None = field(init=False, default=None)

    async def get_tokens(self) -> TokenJar:
        """Get the token jar. Refresh the tokens if necessary.

        Returns:
            The relevant token information for making authenticated API calls.
        """
        if self.token_jar is None or not self.token_jar.is_valid():
            self.token_jar = await self._refresh_tokens()
        return self.token_jar

    async def _refresh_tokens(self) -> TokenJar:
        """Refresh all tokens."""
        oauth = await refresh_oauth_token(
            self.session, self.refresh_token, self.app
        )
        user = await request_user_token(self.session, oauth.access_token)
        xsts = await request_xsts_token(
            self.session, user.token, XSTS_V3_XBOX_AUDIENCE
        )
        halo_xsts = await request_xsts_token(
            self.session, user.token, XSTS_V3_HALO_AUDIENCE
        )
        spartan = await request_spartan_token(self.session, halo_xsts.token)
        clearance = await request_clearance_token(self.session, spartan.token)
        return TokenJar(xsts, spartan, clearance)
