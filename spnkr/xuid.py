"""XUID class for converting XUIDs to and from strings and integers."""

from __future__ import annotations


class XUID:
    """Xbox Live ID."""

    def __init__(self, value: str | int | XUID) -> None:
        xuid_str = str(value)
        if xuid_str[0] == "x":
            self._value = xuid_str
        else:
            self._value = f"xuid({xuid_str})"

    def __str__(self) -> str:
        return self._value

    def as_int(self) -> int:
        return int(self._value[5:-1])
