"""Custom exceptions for spnkr."""


class InvalidXuidError(ValueError):
    """Raised when an invalid XUID is provided."""

    def __init__(self, xuid: str | int) -> None:
        super().__init__(f"Invalid XUID: {xuid!r}")
