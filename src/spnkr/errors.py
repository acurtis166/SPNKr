"""Custom exceptions for spnkr."""


class OAuth2Error(Exception):
    """Error in an OAuth2 token request/response."""

    def __init__(self, response_data: dict) -> None:
        super().__init__(f"Error in OAuth2 reponse: {response_data}")


class InvalidXuidError(ValueError):
    """Raised when an invalid XUID is provided."""

    def __init__(self, xuid: str | int) -> None:
        super().__init__(f"Invalid XUID: {xuid!r}")


class FilmReadError(Exception):
    """Error occurred while reading attributes from a film chunk."""
