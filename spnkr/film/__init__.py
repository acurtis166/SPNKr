"""Download and read Halo Infinite film chunks to extract match data."""

from spnkr.film.api import read_highlight_events
from spnkr.film.models import EventType, HighlightEvent, Medal

__all__ = ["EventType", "HighlightEvent", "Medal", "read_highlight_events"]
