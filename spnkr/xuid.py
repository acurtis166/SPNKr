"""XUID class for converting Xbox Live IDs to and from strings and integers."""

from __future__ import annotations


class XUID:
    """Xbox Live user ID.

    XUIDs are 64-bit integers that uniquely identify an Xbox Live user.

    Attributes:
        value: The XUID value as a wrapped string, e.g., "xuid(<value>)".
    """

    def __init__(self, value: str | int | XUID) -> None:
        """Initialize an XUID.

        Args:
            value: The XUID value as a string, integer, or XUID object.
        """
        self.value = self.wrap(value)

    def __str__(self) -> str:
        return self.value

    def as_int(self) -> int:
        """Return the XUID as an integer."""
        return int(self.value[5:-1])

    @staticmethod
    def wrap(value: str | int | XUID) -> str:
        """Wrap an XUID value in the "xuid()" format."""
        value = str(value)
        if value[0] == "x":
            return value
        return f"xuid({value})"
