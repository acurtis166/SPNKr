"""Custom exceptions for spnkr."""

from typing import Any


class SPNKrError(Exception):
    """Base exception for all spnkr errors."""


class OAuth2Error(SPNKrError):
    """Error in an OAuth2 token request/response."""

    def __init__(self, response_data: dict[str, Any]) -> None:
        self.response_data = response_data
        message = f"OAuth2 error: {response_data.get('error', 'Unknown error')}"
        if error_desc := response_data.get("error_description"):
            message += f" - {error_desc}"
        super().__init__(message)


class InvalidXuidError(SPNKrError, ValueError):
    """Raised when an invalid XUID is provided."""

    def __init__(self, xuid: str | int) -> None:
        self.xuid = xuid
        super().__init__(f"Invalid XUID: {xuid!r}")


class APIError(SPNKrError):
    """Error from an API request."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: Any = None,
    ) -> None:
        self.status_code = status_code
        self.response_data = response_data

        if status_code:
            message = f"[{status_code}] {message}"

        super().__init__(message)


class APIAuthenticationError(APIError):
    """API returned a 401 Unauthorized error."""


class APIAuthorizationError(APIError):
    """API returned a 403 Forbidden error."""


class APINotFoundError(APIError):
    """API returned a 404 Not Found error."""


class APIRateLimitError(APIError):
    """API returned a 429 Too Many Requests error."""


class APIServerError(APIError):
    """API returned a 5xx server error."""


class FilmReadError(SPNKrError):
    """Error occurred while reading attributes from a film chunk."""
