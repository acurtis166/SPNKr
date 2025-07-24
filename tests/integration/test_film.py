"""Test match ID to parsed film data workflow."""

import pytest

from spnkr import HaloInfiniteClient, film


@pytest.mark.asyncio(loop_scope="session")
async def test_read_highlight_events(client: HaloInfiniteClient):
    match_id = "fbf6b19e-2b1d-419e-8d64-756f33fda990"
    result = await film.read_highlight_events(client, match_id)
    assert len(result) > 0
    assert isinstance(result[0], film.HighlightEvent)
