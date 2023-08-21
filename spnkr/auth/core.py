"""Authenticate with services necessary for Halo Infinite API access."""

from aiohttp import ClientSession

from ..xuid import XUID
from . import app, halo, oauth, player, xbox

XSTS_V3_XBOX_AUDIENCE = "http://xboxlive.com"
XSTS_V3_HALO_AUDIENCE = "https://prod.xsts.halowaypoint.com/"


async def authenticate_player(app: app.AzureApp) -> str:
    """Initial authentication of the `app` with Windows Live and Xbox Live.

    Request an OAuth token and return its refresh token.

    Args:
        app: The Azure AD application to authenticate.

    Returns:
        The OAuth refresh token.
    """
    auth_code = _get_authorization_code(app)
    async with ClientSession() as session:
        token = await oauth.request_oauth_token(session, auth_code, app)
    return token.refresh_token


def _get_authorization_code(app: app.AzureApp) -> str:
    """Prompt the user for an authorization code."""
    auth_url = oauth.generate_authorization_url(app)
    print(auth_url)
    print(
        "Navigate to the above URL and copy the 'code' parameter from the "
        "query string."
    )
    return input("Enter the code...")


async def refresh_player_tokens(
    session: ClientSession, oauth_refresh_token: str, app: app.AzureApp
) -> player.AuthenticatedPlayer:
    """Refresh all tokens and return authenticated player information."""
    oauth_token = await oauth.refresh_oauth_token(
        session, oauth_refresh_token, app
    )
    user_token = await xbox.request_user_token(
        session, oauth_token.access_token
    )
    xsts_token = await xbox.request_xsts_token(
        session, user_token.token, XSTS_V3_XBOX_AUDIENCE
    )
    halo_xsts_token = await xbox.request_xsts_token(
        session, user_token.token, XSTS_V3_HALO_AUDIENCE
    )
    spartan_token = await halo.request_spartan_token(
        session, halo_xsts_token.token
    )
    clearance_token = await halo.request_clearance_token(
        session, spartan_token.token
    )
    return player.AuthenticatedPlayer(
        xuid=XUID(xsts_token.xuid),
        gamertag=xsts_token.gamertag,
        spartan_token=spartan_token,
        clearance_token=clearance_token,
    )
