# Basic Usage

!!! info "Note"
    These steps assume you have obtained a spartan token as described [here](getting-started.md). The clearance token is optional and only required for economy endpoints.

## Initializing the HaloInfiniteClient

There are two ways to use `HaloInfiniteClient`: with an explicit session, or with an internally managed one.

### With an Internal Session (Recommended for Simple Use)

Use the client as an async context manager to automatically manage a session:

```python
import asyncio

from spnkr import HaloInfiniteClient


async def main() -> None:
    async with HaloInfiniteClient("SPARTAN_TOKEN") as client:
        history = await client.get_match_history("MyGamertag")


if __name__ == "__main__":
    asyncio.run(main())
```

!!! tip "Clearance Token Optional"
    If you're not using economy endpoints (`get_player_customization`, `get_player_career_rank`, `get_player_reward_track_operations`), you can omit the `clearance_token` parameter.

### With an Explicit Session

If you need more control over the session, provide one explicitly:

```python
import asyncio

from aiohttp import ClientSession
from spnkr import HaloInfiniteClient


async def main() -> None:
    async with ClientSession() as session:
        client = HaloInfiniteClient("SPARTAN_TOKEN", session=session)
        history = await client.get_match_history("MyGamertag")


if __name__ == "__main__":
    asyncio.run(main())
```

!!! tip "Caching Support"
    If using caching via `aiohttp-client-cache`, provide a `CachedSession` as shown in the [Caching](#caching) section below.

## Requesting Data

Now that we have the [HaloInfiniteClient](reference/client.md) initialized, we can begin retrieving data. A simple example is shown below.

```python
import asyncio

from aiohttp import ClientSession
from spnkr import HaloInfiniteClient

# Any of the following are acceptable for the below request.
PLAYER = "xuid(1234567890123456)"  # AuthenticatedPlayer.player_id
PLAYER = "1234567890123456"
PLAYER = 1234567890123456
PLAYER = "MyGamertag"  # AuthenticatedPlayer.gamertag


async def main() -> None:
    async with HaloInfiniteClient("SPARTAN_TOKEN") as client:
        # Request the 25 most recent matches for the player.
        history = await client.get_match_history(PLAYER)

        # Get the most recent match played and print the start time.
        last_match_info = history.results[0].match_info
        print(f"Last match played on {last_match_info.start_time:%Y-%m-%d}")


if __name__ == "__main__":
    asyncio.run(main())
```

Calls to [HaloInfiniteClient](reference/client.md) methods return [Pydantic](https://docs.pydantic.dev/latest/) models or image bytes. You can browse the information available in those response models [here](reference/models.md).

## Caching

Caching is supported via the `aiohttp-client-cache` [package](https://pypi.org/project/aiohttp-client-cache/), which provides a drop-in replacement for `aiohttp.ClientSession` as `aiohttp_client_cache.CachedSession` and reduces the number of repeat requests. It can be installed as an optional dependency with `pip install spnkr[cache]`. Below is an example backend configuration, which relies on the "Cache-Control" header available on certain responses. A SQLite backend is used here, but any backend should work.

If you want localized Discovery UGC responses to be cached separately per `Accept-Language`, enable `include_headers=True`. When you do that, also exclude the client's authentication headers from the cache key with `ignored_params`; otherwise refreshed Spartan or clearance tokens will create duplicate cache entries for the same resource.

```python
from aiohttp_client_cache import CachedSession, SQLiteBackend
from spnkr import HaloInfiniteClient


async def filter_by_cache_control(response):
    """Only cache responses with a cache-control header."""
    return "Cache-Control" in response.headers


async def main() -> None:
    # Other backends are available; `SQLiteBackend` requires the `aiosqlite` package
    cache = SQLiteBackend(
        "cache.sqlite",
        cache_control=True,
        filter_fn=filter_by_cache_control,
        ignored_params=[
            "x-343-authorization-spartan",
            "343-clearance",
        ],
    )
    async with CachedSession(cache=cache) as session:
        client = HaloInfiniteClient("SPARTAN_TOKEN", session=session)
        history = await client.get_match_history("MyGamertag")

        match_id = history.results[0].match_id
        stats1 = await client.get_match_stats(match_id)
        stats2 = await client.get_match_stats(match_id)  # From cache


if __name__ == "__main__":
    asyncio.run(main())
```

!!! note "Session Ownership"
    When you provide an explicit session to the client (as shown above with `CachedSession`), 
    the client will not close it. You remain responsible for the session lifecycle.
    When no session is provided, the client manages the session automatically.

Add `include_headers=True` to that backend configuration if you plan to call localized Discovery UGC methods such as `get_map(..., language="fr-FR")` and want those language variants cached independently.

Here are the cached response max ages as obtained from sample responses on 1/2/2024:

| Service | Method | Max-Age |
| ------- | ------ | ------------ |
| discovery_ugc | get_map | 5 hours |
| discovery_ugc | get_ugc_game_variant | 5 hours |
| discovery_ugc | get_playlist | 5 hours |
| discovery_ugc | get_map_mode_pair | 5 hours |
| gamecms_hacs | get_medal_metadata | 1 day |
| gamecms_hacs | get_csr_season_calendar | 1 day |
| gamecms_hacs | get_season_calendar | 1 day |
| gamecms_hacs | get_career_reward_track | 1 day |
| gamecms_hacs | get_image | 1 day |
| stats | get_match_stats | 1 day |

[Next: Client](reference/client.md){ .md-button }