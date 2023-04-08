from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

import aiohttp
import orjson

from ..authentication.manager import TokenManager

ACCEPT_HEADER = "Accept"
AUTHORIZATION_HEADER = "Authorization"
SPARTAN_HEADER = "x-343-authorization-spartan"
CLEARANCE_HEADER = "343-clearance"
XBL_CONTRACT_VERSION_HEADER = "x-xbl-contract-version"

XBL_CONTRACT_VERSION = "3"


class AuthenticationMethod(Enum):
    SPARTAN_TOKEN = auto()
    CLEARANCE_TOKEN = auto()
    XBOX_LIVE_V3 = auto()


@dataclass(frozen=True, slots=True)
class Response:
    data: dict[str, Any]
    status: int
    error: aiohttp.ClientResponseError | None

    @classmethod
    async def from_response(cls, resp: aiohttp.ClientResponse) -> Response:
        data: dict[str, Any] = await resp.json(loads=orjson.loads)
        status = resp.status
        error = None
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError as e:
            error = e
        return cls(data, status, error)


@dataclass(frozen=True, slots=True)
class Session:
    _session: aiohttp.ClientSession
    _auth: TokenManager

    async def request(
        self,
        method: str,
        url: str,
        auth_method: AuthenticationMethod
        | None = AuthenticationMethod.SPARTAN_TOKEN,
        **kwargs,
    ) -> Response:
        new_headers = kwargs.pop("headers", {})
        headers = {ACCEPT_HEADER: "application/json", **new_headers}

        if auth_method is not None:
            jar = await self._auth.get_tokens()
            if auth_method is AuthenticationMethod.SPARTAN_TOKEN:
                headers[SPARTAN_HEADER] = jar.spartan_token
            elif auth_method is AuthenticationMethod.CLEARANCE_TOKEN:
                headers[SPARTAN_HEADER] = jar.spartan_token
                headers[CLEARANCE_HEADER] = jar.clearance_token
            elif auth_method is AuthenticationMethod.XBOX_LIVE_V3:
                headers[AUTHORIZATION_HEADER] = jar.xsts_authorization_header
                headers[XBL_CONTRACT_VERSION_HEADER] = XBL_CONTRACT_VERSION

        async with self._session.request(
            method, url, headers=headers, **kwargs
        ) as response:
            return await Response.from_response(response)

    async def get(self, url: str, **kwargs) -> Response:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> Response:
        return await self.request("POST", url, **kwargs)
