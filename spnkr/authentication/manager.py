"""
Authentication Manager

Authenticate with Windows Live Server and Xbox Live.
"""

import urllib.parse

import requests

from spnkr.authentication import models as mdl
from spnkr.exceptions import AuthenticationException

DEFAULT_SCOPES = ['Xboxlive.signin', 'Xboxlive.offline_access']
XSTS_V3_XBOX_AUDIENCE = 'http://xboxlive.com'
XSTS_V3_HALO_AUDIENCE = 'https://prod.xsts.halowaypoint.com/'


class AuthenticationManager:
    def __init__(self,
                 client_session: requests.Session,
                 client_id: str,
                 client_secret: str,
                 redirect_uri: str,
                 scopes: list[str] | None = None):
        self.session = client_session
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_uri: str = redirect_uri
        self._scopes: list[str] = scopes or DEFAULT_SCOPES

        self.oauth: mdl.OAuth2TokenResponse | None = None
        self.user_token: mdl.XAUResponse | None = None
        self.xsts_token: mdl.XSTSResponse | None = None
        self.halo_xsts_token: mdl.XSTSResponse | None = None
        self.spartan_token: mdl.SpartanTokenResponse | None = None
        self.clearance_token: mdl.ClearanceTokenResponse | None = None

    def generate_authorization_url(self, state: str | None = None) -> str:
        """Generate Windows Live Authorization URL."""
        params = {
            'client_id': self._client_id,
            'response_type': 'code',
            'approval_prompt': 'auto',
            'scope': ' '.join(self._scopes),
            'redirect_uri': self._redirect_uri,
        }

        if state:
            params['state'] = state

        return 'https://login.live.com/oauth20_authorize.srf?' + urllib.parse.urlencode(params)

    def request_tokens(self, authorization_code: str) -> None:
        """Request all tokens."""
        self.oauth = self.request_oauth_token(authorization_code)
        self.user_token = self.request_user_token()
        self.xsts_token = self.request_xsts_token(XSTS_V3_XBOX_AUDIENCE)
        self.halo_xsts_token = self.request_xsts_token(XSTS_V3_HALO_AUDIENCE)
        self.spartan_token = self.request_spartan_token()
        self.clearance_token = self.request_clearance_token()

    def refresh_tokens(self) -> None:
        """Refresh all tokens."""
        if self.oauth is None or not self.oauth.is_valid():
            self.oauth = self.refresh_oauth_token()
        if self.user_token is None or not self.user_token.is_valid():
            self.user_token = self.request_user_token()
        if self.xsts_token is None or not self.xsts_token.is_valid():
            self.xsts_token = self.request_xsts_token(XSTS_V3_XBOX_AUDIENCE)
        if self.halo_xsts_token is None or not self.halo_xsts_token.is_valid():
            self.halo_xsts_token = self.request_xsts_token(XSTS_V3_HALO_AUDIENCE)
        if self.spartan_token is None or not self.spartan_token.is_valid():
            self.spartan_token = self.request_spartan_token()
        self.clearance_token = self.request_clearance_token()

    def request_oauth_token(self, authorization_code: str) -> mdl.OAuth2TokenResponse:
        """Request OAuth2 token."""
        return self._oauth2_token_request({
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'scope': ' '.join(self._scopes),
            'redirect_uri': self._redirect_uri,
        })

    def refresh_oauth_token(self) -> mdl.OAuth2TokenResponse:
        """Refresh OAuth2 token."""
        return self._oauth2_token_request({
            'grant_type': 'refresh_token',
            'scope': ' '.join(self._scopes),
            'refresh_token': self.oauth.refresh_token,  # type: ignore
        })

    def _oauth2_token_request(self, data: dict[str, str]) -> mdl.OAuth2TokenResponse:
        """Execute token requests."""
        data.update({'client_id': self._client_id, 'client_secret': self._client_secret})
        resp = self.session.post('https://login.live.com/oauth20_token.srf', data=data)
        resp.raise_for_status()
        return mdl.OAuth2TokenResponse.parse_json(resp.text)

    def request_user_token(self,
                           relying_party: str = 'http://auth.xboxlive.com') -> mdl.XAUResponse:
        """Authenticate via access token and receive user token."""
        url = 'https://user.auth.xboxlive.com/user/authenticate'
        headers = {'x-xbl-contract-version': '1'}
        data = {
            'RelyingParty': relying_party,
            'TokenType': 'JWT',
            'Properties': {
                'AuthMethod': 'RPS',
                'SiteName': 'user.auth.xboxlive.com',
                'RpsTicket': f'd={self.oauth.access_token}',  # type: ignore
            },
        }

        resp = self.session.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return mdl.XAUResponse.parse_json(resp.text)

    def request_xsts_token(self, relying_party: str) -> mdl.XSTSResponse:
        """Authorize via user token and receive final X token."""
        url = 'https://xsts.auth.xboxlive.com/xsts/authorize'
        headers = {'x-xbl-contract-version': '1'}
        data = {
            'RelyingParty': relying_party,
            'TokenType': 'JWT',
            'Properties': {
                'UserTokens': [self.user_token.token],  # type: ignore
                'SandboxId': 'RETAIL',
            },
        }

        resp = self.session.post(url, json=data, headers=headers)
        if resp.status_code == 401:
            print('Failed to authorize you! Your password or username may be wrong or you are '
                'trying to use child account (< 18 years old)')
            raise AuthenticationException()
        resp.raise_for_status()
        return mdl.XSTSResponse.parse_json(resp.text)


    def request_spartan_token(self) -> mdl.SpartanTokenResponse:
        url = 'https://settings.svc.halowaypoint.com/spartan-token'
        headers = {'Accept': 'application/json'}
        data = {
            'Audience': 'urn:343:s3:services',
            'MinVersion': '4',
            'Proof': [{
                'Token': self.halo_xsts_token.token,  # type: ignore
                'TokenType': 'Xbox_XSTSv3'
            }]
        }
        resp = self.session.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return mdl.SpartanTokenResponse.parse_json(resp.text)


    def request_clearance_token(self) -> mdl.ClearanceTokenResponse:
        """Request a clearance token, which is required for some endpoints."""
        url = 'https://settings.svc.halowaypoint.com/oban/flight-configurations/titles/hi/audiences/RETAIL/active'
        headers = {
            'x-343-authorization-spartan': self.spartan_token.spartan_token  # type: ignore
        }
        params = {
            'sandbox': 'UNUSED',
            'build': '222249.22.06.08.1730-0'
        }
        resp = self.session.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return mdl.ClearanceTokenResponse.parse_json(resp.text)

