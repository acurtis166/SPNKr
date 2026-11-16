"""Authenticate with services necessary for Halo Infinite API access."""

from aiohttp import ClientSession

from spnkr.auth import app, halo, oauth, player, xbox

XSTS_V3_XBOX_AUDIENCE = "http://xboxlive.com"
XSTS_V3_HALO_AUDIENCE = "https://prod.xsts.halowaypoint.com/"


async def authenticate_player(session: ClientSession, app: app.AzureApp) -> str:
    """Initial authentication of the `app` with Windows Live and Xbox Live.

    Request an OAuth token and return its refresh token. Save the refresh token
    for future use.

    Args:
        session: The session to use for requests.
        app: The Azure AD application to authenticate.

    Returns:
        The OAuth refresh token.
    """
    code = _get_authorization_code(app)
    token = await oauth.request_oauth_token(session, code, app)
    return token.refresh_token


def _get_authorization_code(app: app.AzureApp) -> str:
    """Prompt the user for an authorization code.

    Args:
        app: The Azure AD application to authenticate.

    Returns:
        The authorization code.
    """
    authorization_url = oauth.generate_authorization_url(app)
    print(authorization_url)
    print(
        "Navigate to the above URL and copy the 'code' parameter from the "
        "redirect URL query string in the address bar."
    )
    return input("Enter the code...").strip()


async def refresh_player_tokens(
    session: ClientSession, app: app.AzureApp, oauth_refresh_token: str
) -> player.AuthenticatedPlayer:
    """Refresh all tokens and return authenticated player information.

    Args:
        session: The session to use for requests.
        oauth_refresh_token: The OAuth refresh token.
        app: The Azure AD application to authenticate.

    Returns:
        The authenticated player information.
    """
    oauth_token = await oauth.refresh_oauth_token(session, oauth_refresh_token, app)
    user_token = await xbox.request_user_token(session, oauth_token.access_token)
    xsts_token = await xbox.request_xsts_token(
        session, user_token.token, XSTS_V3_XBOX_AUDIENCE
    )
    halo_xsts_token = await xbox.request_xsts_token(
        session, user_token.token, XSTS_V3_HALO_AUDIENCE
    )
    spartan_token = await halo.request_spartan_token(session, halo_xsts_token.token)
    clearance_token = await halo.request_clearance_token(session, spartan_token.token)
    return player.AuthenticatedPlayer(
        player_id=xsts_token.xuid,
        gamertag=xsts_token.gamertag,
        spartan_token=spartan_token,
        clearance_token=clearance_token,
        xbl_authorization_header_value=xsts_token.authorization_header_value,
    )
