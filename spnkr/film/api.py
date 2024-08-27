"""Film-reading API"""

from uuid import UUID

from aiohttp import ClientResponseError

from spnkr.client import HaloInfiniteClient
from spnkr.errors import FilmReadError
from spnkr.film import highlight_events


async def read_highlight_events(client: HaloInfiniteClient, match_id: str | UUID):
    """Download and parse the highlight events chunk from a film asset for a given match.

    Only human (not bot) players have events available. Bot data is unlikely to be
    available in the highlight events chunk as they are not observable in theater
    mode.

    Team IDs for the players are not yet available, so it is necessary to join up
    to match stats data for the information.

    Mode-specific details are not available yet, such as a to distinguish a flag capture
    from a flag return.

    Killing AI opponents (such as in Firefight game modes) does not record a highlight
    event.

    There are infrequent cases where not all kill/death events are captured as
    expected. See `spnkr.film.highlight_events.check` for a method of checking
    outcomes against match stats.

    Args:
        client: A client for requesting film metadata and downloading film data.
        match_id: The UUID of the match to read film data for.

    Returns:
        A list of HighlightEvent instances extracted from the downloaded data.

    Raises:
        spnkr.errors.FilmReadError when film data can't be retrieved or read.
    """
    try:
        film_response = await client.discovery_ugc.get_film_by_match_id(match_id)
    except ClientResponseError as ex:
        raise FilmReadError(
            f"Error getting highlight events film metadata: {ex}"
        ) from ex
    film = await film_response.parse()
    url = film.highlight_events_url
    if url is None:
        raise FilmReadError("Film doesn't have a highlight events chunk")

    response = await client._session.get(url)
    try:
        response.raise_for_status()
    except ClientResponseError as ex:
        raise FilmReadError(
            f"Error downloading highlight events film chunk: {ex}"
        ) from ex
    return list(highlight_events.read(await response.read()))
