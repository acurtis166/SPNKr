"""Base Models."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from spnkr.parsers import parse_iso_datetime


@dataclass(frozen=True)
class Date:
    iso_8601_date: dt.datetime

    @classmethod
    def from_dict(cls, data: dict) -> Date:
        """Parse a Date from a dictionary."""
        return cls(
            iso_8601_date=parse_iso_datetime(data["ISO8601Date"]),
        )
