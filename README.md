# Welcome to SPNKr

SPNKr is an async Python SDK for the undocumented Halo Infinite web API.

It is intended for personal analysis workflows (match history, skill/rank data,
metadata, and theater film parsing). The project is unofficial and provided as-is.

- Documentation: https://acurtis166.github.io/SPNKr/
- PyPI: https://pypi.org/project/spnkr/
- GitHub: https://github.com/acurtis166/spnkr

## What You Can Do

- Request player match history, service records, and match stats.
- Retrieve skill/MMR/CSR data by match or playlist.
- Resolve player profile data (XUID <-> gamertag).
- Fetch content metadata (maps, modes, playlists, medals, season data).
- Access economy/customization-related endpoints.
- Download and parse theater film highlight events.

## Install

Requires Python >= 3.11.

```shell
pip install spnkr
```

Optional caching support:

```shell
pip install "spnkr[cache]"
```

## Quickstart

### 1. Get tokens

SPNKr requires these Halo headers:

- `x-343-authorization-spartan` (required for all endpoints)
- `343-clearance` (optional, required only for economy endpoints)

You can get them in two ways:

1. Manual (fastest): copy headers from Halo Waypoint network traffic.
1. Programmatic (recommended): use Azure app registration + refresh flow.

Detailed steps are in the docs:

- https://acurtis166.github.io/SPNKr/getting-started/

### 2. Create the client

```python
import asyncio

from spnkr import HaloInfiniteClient


async def main() -> None:
    async with HaloInfiniteClient(
        spartan_token="SPARTAN_TOKEN",
        clearance_token="CLEARANCE_TOKEN",  # Optional; required for economy endpoints
        requests_per_second=5,
    ) as client:
        # Accepts gamertag, raw XUID, or wrapped xuid(...) formats.
        history = await client.get_match_history("MyGamertag", start=0, count=5)

        if history.results:
            latest = history.results[0].match_info
            print(f"Latest match start: {latest.start_time:%Y-%m-%d %H:%M:%S}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Refresh tokens when needed

Spartan tokens are short-lived. If you already have replacement tokens, update an
existing client without recreating it:

```python
client.spartan_token = "NEW_SPARTAN"
```

For automated token refresh, see auth helpers:

- `authenticate_player`
- `refresh_player_tokens`

Reference: https://acurtis166.github.io/SPNKr/reference/authentication/

# Service Overview

`HaloInfiniteClient` provides direct access to all API endpoints. Methods are grouped logically by their purpose:

| Category | Methods | Requires Clearance? |
| --- | --- | --- |
| **Match Stats** | `get_match_history`, `get_match_count`, `get_match_stats` | No |
| **Skill/CSR** | `get_match_skill`, `get_playlist_csr` | No |
| **Player Profile** | `get_current_user`, `get_user_by_gamertag`, `get_user_by_id`, `get_users_by_id` | No |
| **Service Records** | `get_service_record` | No |
| **Discovery UGC** | `get_map`, `get_playlist`, `get_ugc_game_variant`, `get_map_mode_pair`, `search_assets`, `get_film_by_match_id` | No |
| **Game CMS** | `get_medal_metadata`, `get_csr_season_calendar`, `get_season_calendar`, `get_career_reward_track`, `get_image`, `get_progression_file` | No |
| **Economy** | `get_player_customization`, `get_player_career_rank`, `get_player_reward_track_operations` | **Yes** |
| **Challenge Decks** | `get_challenge_decks` | No |

Reference: https://acurtis166.github.io/SPNKr/reference/client/

## Caching

SPNKr supports `aiohttp-client-cache` as a drop-in session replacement.
This can reduce repeated requests, especially for metadata-heavy workflows.

When caching localized Discovery UGC calls (for example with
`language="fr-FR"`), configure cache keys to account for language and avoid
token-specific duplication.

Full caching guidance: https://acurtis166.github.io/SPNKr/basic-usage/

## Film / Theater Parsing

The `spnkr.film` module includes helpers for downloading film chunks and parsing
timestamped highlight events from theater recordings.

In theater mode, these highlight events appear as timeline markers for key match
moments such as kills, deaths, medals, and mode-specific events.

![Theater timeline highlight-event markers](assets/highlight_events_timeline.png)

Here is a minimal example script to dump highlight events for a match to JSON.
Medal events include both the numeric `medal` value and its `medal_name`.

```python
import asyncio
import json

from spnkr import HaloInfiniteClient, film


async def main():
    async with HaloInfiniteClient(
        spartan_token="SPARTAN_TOKEN", clearance_token="CLEARANCE_TOKEN"
    ) as client:
        events = await film.read_highlight_events(client, match_id="MATCH_GUID")

    with open("highlight_events.json", "w") as fp:
        json.dump([e.model_dump(mode="json") for e in events], fp)


if __name__ == "__main__":
    asyncio.run(main())
```

Reference: https://acurtis166.github.io/SPNKr/reference/film/

## Acknowledgements

- Xbox Live authentication flow: https://github.com/OpenXbox/xbox-webapi-python
- Halo Infinite authentication flow and endpoint research: https://den.dev/blog/halo-api-authentication
- Microsoft/343 Industries

## Disclaimer

This software is not endorsed or supported by Microsoft or 343 Industries.
It is a personal project for Halo Infinite data analysis.

Authentication requires personal credentials and tokens; use at your own risk.

## Contributing

Contributions to fix issues or add endpoint support are welcome.
