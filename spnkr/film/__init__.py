"""Download and read Halo Infinite film chunks to extract match data."""

from spnkr.film.api import read_highlight_events
from spnkr.film.highlight_events import HighlightEvent

__all__ = ["read_highlight_events", "HighlightEvent"]
