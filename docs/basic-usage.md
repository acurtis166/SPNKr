# Basic Usage

!!! info "Note"
    These steps assume you have already performed the initial OAuth2 authentication step outlined [here](getting-started.md#initial-authentication).

## Obtaining Spartan and Clearance Tokens

With your OAuth2 refresh token, you need to perform a series of token requests:

1. Refresh the OAuth2 access token
1. Request an Xbox Live user token
1. Request an Xbox Live XSTS token scoped to Xbox Live services (not strictly necessary, but it returns profile information like your player ID (XUID) and gamertag)
1. Request an Xbox Live XSTS token scoped to Halo services
1. Request a "spartan token", which is required for all endpoints
1. Request a "clearance ID", which is required for some endpoints

However, you will again just make a single [function](reference/authentication.md#spnkr.auth.core.refresh_player_tokens) call to refresh/request tokens and return the needed information. The example script below will look similar to our step above, but now we are retrieving spartan and clearance tokens that will be headers for our API calls.

```python
import asyncio

from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "REDIRECT_URI"
REFRESH_TOKEN = "REFRESH_TOKEN"


async def main() -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    async with ClientSession() as session:
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)

    print(f"Spartan token: {player.spartan_token.token}")  # Valid for 4 hours.
    print(f"Clearance token: {player.clearance_token.token}")
    print(f"Xbox Live player ID (XUID): {player.player_id}")
    print(f"Xbox Live gamertag: {player.gamertag}")
    print(f"Xbox Live authorization: {player.xbl_authorization_header_value}")


if __name__ == "__main__":
    asyncio.run(main())
```

The spartan token and clearance token are the main targets of this step, as they are needed to initialize the client object. However, the [AuthenticatedPlayer](reference/authentication.md#spnkr.auth.player.AuthenticatedPlayer) instance also carries Xbox Live information that you may find useful:

- **Xbox Live player ID (XUID)** - This ID is unique to your Xbox Live account. XUIDs are also the identifying attribute for player-specific data retrieved from the API. Additionally, XUIDs are required for certain endpoints in order to retrieve player-specific data.
- **Xbox Live gamertag** - This is the display name for Xbox Live accounts.
- **Xbox Live authorization header value** - This is a required request header when making requests to the Xbox Live API, if desired.

## Initializing the HaloInfiniteClient

Now that we have the spartan and clearance tokens, we are ready to create a [HaloInfiniteClient](reference/client.md) object. The constructor takes a `aiohttp.ClientSession` instance and the tokens as arguments. An example is shown below.

```python
import asyncio

from aiohttp import ClientSession

from spnkr.client import HaloInfiniteClient


async def main() -> None:
    async with ClientSession() as session:
        client = HaloInfiniteClient(
            session=session,
            spartan_token="SPARTAN_TOKEN",
            clearance_token="CLEARANCE_TOKEN",
            # Optional, default rate is 5. Pass None for no rate-limiting
            requests_per_second=5,
        )


if __name__ == "__main__":
    asyncio.run(main())
```

## Requesting Data

Now that we have the [HaloInfiniteClient](reference/client.md) initialized, we can begin retrieving data. A simple continuation of the above script is shown below.

```python
import asyncio

from aiohttp import ClientSession

from spnkr.client import HaloInfiniteClient

# Any of the following are acceptable for the below request.
PLAYER = "xuid(1234567890123456)"  # AuthenticatedPlayer.player_id
PLAYER = "1234567890123456"
PLAYER = 1234567890123456
PLAYER = "MyGamertag"  # AuthenticatedPlayer.gamertag


async def main() -> None:
    async with ClientSession() as session:
        client = HaloInfiniteClient(...)

        # Request the 25 most recent matches for the player.
        history = await client.stats.get_match_history(PLAYER)

        # Get the most recent match played and print the start time.
        last_match_info = history.results[0].match_info
        print(f"Last match played on {last_match_info.start_time:%Y-%m-%d}")


if __name__ == "__main__":
    asyncio.run(main())
```

Calls to [HaloInfiniteClient](reference/client.md) services return parsed JSON payloads in the form of [Pydantic](https://docs.pydantic.dev/latest/) models. You can browse the information available in those response models [here](reference/models.md).

Of course, there are additional methods for retrieving stats, CSR/MMR, and metadata information.

[Services](reference/services.md){ .md-button }

## Match API

An alternative API for requesting match-related data is available via a client-wrapping [Match](reference/match.md) class. A `Match` instance maintains a reference to the client and a match ID to abstract from some of the details of integrating API calls. A basic example involving a metadata request is shown below.

```python
import asyncio

from aiohttp import ClientSession

from spnkr.client import HaloInfiniteClient
from spnkr.match import Match


async def main() -> None:
    async with ClientSession() as session:
        client = HaloInfiniteClient(...)
        history = await client.stats.get_match_history(...)
        most_recent = history.results[0]

        # Using the `HaloInfiniteClient` directly.
        map_mode_pair = most_recent.playlist_map_mode_pair
        map_mode_pair_model = await client.discovery_ugc.get_map_mode_pair(
            map_mode_pair.asset_id, map_mode_pair.version_id
        )
        print(f"Last match: {map_mode_pair_model.public_name}")

        # Using the `Match` wrapper. Match info argument is optional.
        match_ = Match(client, most_recent.match_id, most_recent.match_info)
        map_mode_pair = await match_.get_map_mode_pair()
        print(f"Last match: {map_mode_pair.public_name}")


if __name__ == "__main__":
    asyncio.run(main())
```

Follow the link below to see all methods available.

[Match](reference/match.md){ .md-button }