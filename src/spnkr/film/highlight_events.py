"""Read highlight event film chunks."""

import zlib
from typing import Any

from bitstring import Bits

from spnkr.errors import FilmReadError
from spnkr.film.models import EventType, HighlightEvent, Medal

_MIN_XUID = int(2e15)
_MAX_XUID = int(3e15)
_XUID_BITS = 64
_MODE = 10
_DEATH = 20
_KILL = 50
_MEDAL_SORTING_WEIGHTS = {
    50,
    51,
    52,
    100,
    101,
    150,
    200,
    205,
    210,
    220,
    225,
    230,
    235,
    240,
    245,
    250,
}


def read(data: bytes, version: int):
    """Iterate events found in highlight event file content.

    Args:
        data: The zlib-compressed or uncompressed file data.
        version: The major version of the film, available from either the film metadata
            or the film header.

    Yields:
        Highlight events.
    """
    if _is_zlib_compressed(data):
        data = zlib.decompress(data)
    bits = Bits(bytes=data)
    for start, _ in _find_xuids(bits):
        yield _parse_event(bits, start, version)


def _is_zlib_compressed(data: bytes) -> bool:
    if len(data) < 2:
        return False
    cmf, flg = data[:2]
    return (cmf & 0x0F) == 8 and (cmf >> 4) <= 7 and ((cmf << 8) | flg) % 31 == 0


def _find_xuids(bits: Bits):
    """Iterate XUID (start, value) tuples found in binary data."""
    # Example:
    # ------xuid------ --marker-
    # 2a5bf9c8f1010900 (2d|25)c0
    for marker_start in bits.findall(Bits(hex="c0")):
        xuid_end = marker_start - 8
        if bits[xuid_end:marker_start].uint not in (0x2D, 0x25):
            continue
        xuid_start = xuid_end - _XUID_BITS
        xuid_bits = bits[xuid_start:xuid_end]
        if len(xuid_bits) < _XUID_BITS:
            continue
        xuid = xuid_bits.uintle
        if _MIN_XUID < xuid < _MAX_XUID:
            yield (xuid_start, xuid)


def _infer_event_type(hint: int, is_medal: bool) -> EventType:
    """Infer the type of an event given information from a couple bytes."""
    if is_medal and hint in _MEDAL_SORTING_WEIGHTS:
        return EventType.MEDAL
    if hint == _MODE:
        return EventType.MODE
    if hint == _DEATH:
        return EventType.DEATH
    if hint == _KILL:
        return EventType.KILL
    raise FilmReadError(f"Unhandled event type args: {hint=}, {is_medal=}")


def _tokens(version: int) -> list[str]:
    """Determine unpacking strategy based on the film major version."""
    if 38 < version < 41:
        return [
            "pad:96",  # Skip (12 bytes)
            "bytes:32",  # 16-character utf-16 gamertag (32 bytes)
            "pad:24",  # Skip (3 bytes)
            "uint:8",  # Type hint (1 byte)
            "uint:32",  # Timestamp in milliseconds (4 bytes)
            "pad:24",  # Skip (3 bytes)
            "uint:8",  # 1 if event is medal, otherwise 0 (1 byte)
            "pad:24",  # Skip (3 bytes)
            "uint:8",  # Medal type (1 byte)
        ]
    return [
        "bytes:32",  # 16-character utf-16 gamertag (32 bytes)
        "pad:120",  # Skip (15 bytes)
        "uint:8",  # Type hint (1 byte)
        "uint:32",  # Timestamp in milliseconds (4 bytes)
        "pad:24",  # Skip (3 bytes)
        "uint:8",  # 1 if event is medal, otherwise 0 (1 byte)
        "pad:24",  # Skip (3 bytes)
        "uint:8",  # Medal type (1 byte)
    ]


def _parse_event(bits: Bits, start: int, version: int) -> HighlightEvent:
    """Parse an event from `bits` starting at `start`."""
    selected = bits[start : start + 20_000]  # 20,000 bits just to capture the event
    # Grab the relevant 60 bytes of event data and unpack the attributes
    end = selected.find(Bits(hex="00002ee0"))[0]  # type: ignore
    event_bits = selected[end - (60 * 8) : end]
    values: list[Any] = event_bits.unpack(fmt=", ".join(_tokens(version)))
    gamertag_bytes, type_hint, time_ms, is_medal, medal_value = values
    event_type = _infer_event_type(type_hint, is_medal == 1)
    try:
        medal = Medal(medal_value) if event_type is EventType.MEDAL else None
    except ValueError as e:
        raise FilmReadError(f"Invalid medal value: {medal_value}, {version=}") from e
    return HighlightEvent(
        xuid=selected[:_XUID_BITS].uintle,
        gamertag=gamertag_bytes.decode("utf-16le").strip("\x00"),
        event_type=event_type,
        time_ms=time_ms,
        medal=medal,
    )
