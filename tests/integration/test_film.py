"""Test match ID to parsed film data workflow."""

import pytest

from spnkr import HaloInfiniteClient, film


@pytest.mark.asyncio(loop_scope="session")
async def test_read_highlight_events(client: HaloInfiniteClient):
    match_id = "01ee3491-1ca1-4822-b23e-63e836104f32"
    result = await film.read_highlight_events(client, match_id)
    assert len(result) == 6
