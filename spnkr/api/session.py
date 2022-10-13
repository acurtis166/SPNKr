
from typing import Any

import ms_cv
import requests

from spnkr.api.enums import AuthenticationMethod
from spnkr.authentication.manager import AuthenticationManager


class Session:
    def __init__(self, auth_mgr: AuthenticationManager, validate_tokens: bool = True):
        self._auth_mgr = auth_mgr
        self._cv = ms_cv.CorrelationVector()
        self._validate_tokens = validate_tokens

    def request(self,
                method: str,
                url: str,
                auth_method: AuthenticationMethod | None = AuthenticationMethod.SpartanToken,
                include_cv: bool = True,
                **kwargs: Any) -> requests.Response:
        """Proxy Request and add Auth/CV headers."""
        headers = kwargs.pop('headers', {})

        if 'Accept' not in headers:
            # default to accepting a JSON response
            headers['Accept'] = 'application/json'

        if self._validate_tokens and auth_method is not None:
            self._auth_mgr.refresh_tokens()

        if auth_method == AuthenticationMethod.SpartanToken:
            headers['x-343-authorization-spartan'] = self._auth_mgr.spartan_token.spartan_token  # type: ignore
        elif auth_method == AuthenticationMethod.ClearanceToken:
            headers['x-343-authorization-spartan'] = self._auth_mgr.spartan_token.spartan_token  # type: ignore
            headers['343-clearance'] = self._auth_mgr.clearance_token.flight_configuration_id  # type: ignore
        elif auth_method == AuthenticationMethod.XSTSv3XboxAudience:
            headers['Authorization'] = self._auth_mgr.xsts_token.authorization_header_value  # type: ignore
            headers['x-xbl-contract-version'] = '3'

        if include_cv:
            headers['MS-CV'] = self._cv.increment()

        return self._auth_mgr.session.request(method, url, headers=headers, **kwargs)

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request('GET', url, **kwargs)

    def options(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request('HEAD', url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request('POST', url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request('PUT', url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request('PATCH', url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request('DELETE', url, **kwargs)

        