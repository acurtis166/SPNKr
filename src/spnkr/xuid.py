"""Convert Xbox Live IDs (XUID) to and from strings and integers."""

import math
import re

from spnkr.errors import InvalidXuidError

_XUID_PATTERN = re.compile(r"^xuid\((\d{16})\)$")


def wrap_xuid(xuid: str | int) -> str:
    """Wrap an Xbox Live ID in the "xuid()" format.

    Args:
        xuid: Xbox Live ID. This can be an integer or a string representation of
            the ID. Examples of valid inputs include "xuid(1234567890123456)",
            "1234567890123456", and 1234567890123456.

    Returns:
        A wrapped version of the XUID.

    Raises:
        InvalidXuidError: If the XUID is invalid.
    """
    return f"xuid({unwrap_xuid(xuid)})"


def unwrap_xuid(xuid: str | int) -> int:
    """Get the integer value of an Xbox Live ID.

    Args:
        xuid: Xbox Live ID. This can be an integer or a string representation of
            the ID. Examples of valid inputs include "xuid(1234567890123456)",
            "1234567890123456", and 1234567890123456.

    Returns:
        The integer value of the Xbox Live ID.

    Raises:
        InvalidXuidError: If the XUID is invalid.
    """
    if isinstance(xuid, int):
        if not math.floor(math.log10(xuid)) + 1 == 16:
            # Must be a 16-digit number
            raise InvalidXuidError(xuid)
        return xuid

    xuid = xuid.strip().lower()
    if xuid.isdigit() and len(xuid) == 16:
        return int(xuid)

    match = _XUID_PATTERN.match(xuid)
    if match is None:
        raise InvalidXuidError(xuid)
    return int(match.group(1))


def wrap_xuid_or_gamertag(xuid_or_gamertag: str | int) -> str:
    """Return the value if it is a gamertag. Otherwise, wrap in "xuid()" format.

    Args:
        xuid_or_gamertag: Xbox Live ID or gamertag. This can be an integer, a
            string representation of the ID, or a gamertag. Examples of valid
            inputs include "xuid(1234567890123456)", "1234567890123456",
            1234567890123456, and "MyGamertag".

    Returns:
        A wrapped version of the XUID or the gamertag.

    Raises:
        InvalidXuidError: If the XUID is invalid.
    """
    try:
        return wrap_xuid(xuid_or_gamertag)
    except InvalidXuidError:
        if isinstance(xuid_or_gamertag, int) or not xuid_or_gamertag.strip():
            raise
        return xuid_or_gamertag.strip()  # Can safely assume it's a gamertag
