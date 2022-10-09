
import datetime as dt


def unwrap_xuid(xuid: str) -> str:
    return xuid[5:-1] if xuid[0] == 'x' else xuid


def wrap_xuid(xuid: str) -> str:
    return xuid if xuid[0] == 'x' else f'xuid({xuid})'


def parse_iso_duration(iso_duration: str) -> dt.timedelta:
    """Assume element no larger than weeks."""
    assert iso_duration.startswith('PT')
    kwargs = {}
    search = iso_duration[2:]
    seps = {'W': 'weeks', 'D': 'days', 'H': 'hours', 'M': 'minutes', 'S': 'seconds'}
    for sep, attr in seps.items():
        parts = search.split(sep)
        if len(parts) > 1:
            kwargs[attr] = float(parts[0])
            search = parts[1]
    return dt.timedelta(**kwargs)


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)

    