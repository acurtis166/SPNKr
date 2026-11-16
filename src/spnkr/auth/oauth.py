"""Authenticate using OAuth2."""

import urllib.parse
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession

from spnkr.auth.app import AzureApp
from spnkr.errors import OAuth2Error

DEFAULT_SCOPES = ["Xboxlive.signin", "Xboxlive.offline_access"]


@dataclass(frozen=True)
class OAuth2Token:
    """Response resulting from a request for an OAuth2 token.

    This is the root token used to authenticate an application. It is used to
    request an XToken, which is used to authenticate a user for Xbox Live.

    Attributes:
        raw: The raw, deserialized JSON response.
    """

    raw: dict[str, Any]

    @property
    def access_token(self) -> str:
        """The access token."""
        return self.raw["access_token"]

    @property
    def refresh_token(self) -> str:
        """The refresh token used to refresh the access token."""
        return self.raw["refresh_token"]


def generate_authorization_url(app: AzureApp) -> str:
    """Generate Windows Live Authorization URL.

    Args:
        app: The Azure AD application to authenticate.

    Returns:
        The authorization URL.
    """
    params = {
        "client_id": app.client_id,
        "response_type": "code",
        "approval_prompt": "auto",
        "scope": " ".join(DEFAULT_SCOPES),
        "redirect_uri": app.redirect_uri,
    }
    query = urllib.parse.urlencode(params)
    return f"https://login.live.com/oauth20_authorize.srf?{query}"


async def request_oauth_token(
    session: ClientSession, authorization_code: str, app: AzureApp
) -> OAuth2Token:
    """Request an OAuth2 token.

    Args:
        session: The aiohttp session to use.
        authorization_code: The authorization code to use.
        app: The Azure AD application to authenticate.

    Returns:
        The OAuth2 token response.
    """
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "scope": " ".join(DEFAULT_SCOPES),
        "redirect_uri": app.redirect_uri,
    }
    return await _oauth2_token_request(session, data, app)


async def refresh_oauth_token(
    session: ClientSession, refresh_token: str, app: AzureApp
) -> OAuth2Token:
    """Refresh an OAuth2 token.

    Args:
        session: The aiohttp session to use.
        refresh_token: The refresh token to use.
        app: The Azure AD application to authenticate.

    Returns:
        The OAuth2 token response.
    """
    data = {
        "grant_type": "refresh_token",
        "scope": " ".join(DEFAULT_SCOPES),
        "refresh_token": refresh_token,
    }
    return await _oauth2_token_request(session, data, app)


async def _oauth2_token_request(
    session: ClientSession, data: dict[str, str], app: AzureApp
) -> OAuth2Token:
    """Execute an OAuth2 token request."""
    url = "https://login.live.com/oauth20_token.srf"
    request_data = {
        **data,
        "client_id": app.client_id,
        "client_secret": app.client_secret,
    }
    response = await session.post(url, data=request_data)
    if not response.ok:
        raise OAuth2Error(await response.json())
    return OAuth2Token(await response.json())
