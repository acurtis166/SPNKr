"""Convert Xbox Live IDs (XUID) to and from strings and integers."""

import re

_PATTERN = re.compile(r"^xuid\((\d+)\)$")


def wrap_xuid(value: str | int) -> str:
    """Wrap a XUID value in the "xuid()" format.

    Args:
        value: The XUID value to wrap.

    Returns:
        The wrapped XUID value as a string.
    """
    value = str(value)
    if value[0] == "x":
        return value
    return f"xuid({value})"


def unwrap_xuid(value: str | int) -> int:
    """Unwrap a XUID value from the "xuid()" format.

    Args:
        value: The XUID value to unwrap.

    Raises:
        ValueError: If the XUID value is invalid.

    Returns:
        The unwrapped XUID value as an integer.
    """
    if isinstance(value, int) or value.isdigit():
        return int(value)

    match = _PATTERN.match(value)
    if not match:
        raise ValueError(f"Invalid XUID: {value!r}")
    return int(match.group(1))
