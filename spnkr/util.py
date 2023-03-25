import datetime as dt


def unwrap_xuid(xuid: str) -> str:
    return xuid[5:-1] if xuid[0] == "x" else xuid


def wrap_xuid(xuid: str) -> str:
    return xuid if xuid[0] == "x" else f"xuid({xuid})"


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)
