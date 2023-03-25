import datetime as dt

import dateutil.parser


def parse_iso_datetime(iso_datetime: str) -> dt.datetime:
    return dateutil.parser.isoparse(iso_datetime)


def parse_iso_duration(iso_duration: str) -> dt.timedelta:
    """Assume element no larger than weeks."""
    assert iso_duration.startswith("PT")
    kwargs = {}
    search = iso_duration[2:]
    seps = {
        "W": "weeks",
        "D": "days",
        "H": "hours",
        "M": "minutes",
        "S": "seconds",
    }
    for sep, attr in seps.items():
        parts = search.split(sep)
        if len(parts) > 1:
            kwargs[attr] = float(parts[0])
            search = parts[1]
    return dt.timedelta(**kwargs)
