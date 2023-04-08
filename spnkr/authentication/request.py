import urllib.parse

from aiohttp import ClientSession

import spnkr.authentication.models as mdl
from spnkr.authentication.app import AzureApp

DEFAULT_SCOPES = ["Xboxlive.signin", "Xboxlive.offline_access"]


def generate_authorization_url(app: AzureApp) -> str:
    """Generate Windows Live Authorization URL."""
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
) -> mdl.OAuth2TokenResponse:
    """Request OAuth2 token."""
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "scope": " ".join(DEFAULT_SCOPES),
        "redirect_uri": app.redirect_uri,
    }
    return await _oauth2_token_request(session, data, app)


async def refresh_oauth_token(
    session: ClientSession, refresh_token: str, app: AzureApp
) -> mdl.OAuth2TokenResponse:
    """Refresh OAuth2 token."""
    data = {
        "grant_type": "refresh_token",
        "scope": " ".join(DEFAULT_SCOPES),
        "refresh_token": refresh_token,
    }
    return await _oauth2_token_request(session, data, app)


async def _oauth2_token_request(
    session: ClientSession, data: dict[str, str], app: AzureApp
) -> mdl.OAuth2TokenResponse:
    """Execute token requests."""
    url = "https://login.live.com/oauth20_token.srf"
    request_data = {
        **data,
        "client_id": app.client_id,
        "client_secret": app.client_secret,
    }
    async with session.post(url, data=request_data) as resp:
        return mdl.OAuth2TokenResponse.from_dict(await resp.json())


async def request_user_token(
    session: ClientSession,
    access_token: str,
    relying_party: str = "http://auth.xboxlive.com",
) -> mdl.XAUResponse:
    """Authenticate via OAuth access token and receive user token."""
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
        return mdl.XAUResponse.from_dict(await resp.json())


async def request_xsts_token(
    session: ClientSession, user_token: str, relying_party: str
) -> mdl.XSTSResponse:
    """Authorize via user token and receive final X token."""
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
        return mdl.XSTSResponse.from_dict(await resp.json())


async def request_spartan_token(
    session: ClientSession, halo_xsts_token: str
) -> mdl.SpartanTokenResponse:
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
    async with session.post(url, headers=headers, json=js) as resp:
        return mdl.SpartanTokenResponse.from_dict(await resp.json())


async def request_clearance_token(
    session: ClientSession, spartan_token: str
) -> mdl.ClearanceTokenResponse:
    """Request a clearance token, which is required for some endpoints."""
    url = "https://settings.svc.halowaypoint.com/oban/flight-configurations/titles/hi/audiences/RETAIL/active"
    hdrs = {"x-343-authorization-spartan": spartan_token}
    params = {"sandbox": "UNUSED", "build": "222249.22.06.08.1730-0"}
    async with session.get(url, params=params, headers=hdrs) as resp:
        return mdl.ClearanceTokenResponse.from_dict(await resp.json())
