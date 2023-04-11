"""Provides a session for making authenticated requests to the API."""

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
    """Enum for the different authentication methods available."""

    SPARTAN_TOKEN = auto()
    CLEARANCE_TOKEN = auto()
    XBOX_LIVE_V3_HALO_AUDIENCE = auto()


@dataclass(frozen=True, slots=True)
class Response:
    """Represents a data response from the API.

    Attributes:
        data: The data returned from the API.
        status: The status code of the response.
        error: The error returned from the API, if any.
    """

    data: dict[str, Any]
    status: int
    error: aiohttp.ClientResponseError | None

    @classmethod
    async def from_response(cls, resp: aiohttp.ClientResponse) -> Response:
        """Create a Response from an aiohttp response.

        Args:
            resp: The aiohttp response to create the Response from.

        Returns:
            The Response created from the aiohttp response.
        """
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
        """Make a request to the API.

        Args:
            method: The HTTP method to use.
            url: The URL to make the request to.
            auth_method: The authentication method to use.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            The response from the API.
        """
        new_headers = kwargs.pop("headers", {})
        headers = {ACCEPT_HEADER: "application/json", **new_headers}

        if auth_method is not None:
            jar = await self._auth.get_tokens()
            if auth_method is AuthenticationMethod.SPARTAN_TOKEN:
                headers[SPARTAN_HEADER] = jar.spartan_token
            elif auth_method is AuthenticationMethod.CLEARANCE_TOKEN:
                headers[SPARTAN_HEADER] = jar.spartan_token
                headers[CLEARANCE_HEADER] = jar.clearance_token
            elif auth_method is AuthenticationMethod.XBOX_LIVE_V3_HALO_AUDIENCE:
                headers[AUTHORIZATION_HEADER] = jar.xsts_authorization_header
                headers[XBL_CONTRACT_VERSION_HEADER] = XBL_CONTRACT_VERSION

        async with self._session.request(
            method, url, headers=headers, **kwargs
        ) as response:
            return await Response.from_response(response)

    async def get(
        self,
        url: str,
        auth_method: AuthenticationMethod = AuthenticationMethod.SPARTAN_TOKEN,
        **kwargs,
    ) -> Response:
        """Make a GET request to the API.

        Args:
            url: The URL to make the request to.
            auth_method: The authentication method to use. Defaults to
                AuthenticationMethod.SPARTAN_TOKEN.
            **kwargs: Additional keyword arguments to pass to
                `aiohttp.ClientSession.request()` method.

        Returns:
            The response from the API.
        """
        return await self.request("GET", url, auth_method, **kwargs)

    async def post(
        self,
        url: str,
        auth_method: AuthenticationMethod = AuthenticationMethod.SPARTAN_TOKEN,
        **kwargs,
    ) -> Response:
        """Make a POST request to the API.

        Args:
            url: The URL to make the request to.
            auth_method: The authentication method to use. Defaults to
                AuthenticationMethod.SPARTAN_TOKEN.
            **kwargs: Additional keyword arguments to pass to
                `aiohttp.ClientSession.request()` method.

        Returns:
            The response from the API.
        """
        return await self.request("POST", url, auth_method, **kwargs)
