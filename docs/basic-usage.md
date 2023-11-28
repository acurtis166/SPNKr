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
        response = await client.get_match_history(PLAYER)


if __name__ == "__main__":
    asyncio.run(main())
```

## Parsing Responses

API calls return JSON payloads, but these are not deserialized by the client. Instead, client methods return raw `aiohttp.ClientResponse` objects to be handled by the user. That being said, two built-in parsing strategies are available.

- [Pydantic parsing](reference/pydantic-parsing.md) - Parse JSON responses into [Pydantic](https://docs.pydantic.dev/latest/) models.
- [Records parsing](reference/records-parsing.md) - Parse JSON responses into flat, record-like named tuples with only highlighted information. While not as complete as the Pydantic models, they are likely more convenient to load into a `pandas.DataFrame` or dump to files/databases.

The classes and functions for these parsers are available in the `spnkr.parsers` module. Relevant parsing objects are referenced by the [HaloInfiniteClient](reference/client.md) methods.

Below is a continuation of our above script with parsing of the JSON into a [MatchHistory](reference/pydantic-parsing.md#spnkr.parsers.pydantic.stats.MatchHistory) Pydantic model.

```python
import asyncio

from aiohttp import ClientSession

from spnkr.client import HaloInfiniteClient
from spnkr.parsers.pydantic import MatchHistory


async def main() -> None:
    async with ClientSession() as session:
        client = HaloInfiniteClient(...)
        response = await client.get_match_history(...)

        # Deserialize the JSON response
        data = await response.json()

        # Parse the data into a Pydantic model
        history = MatchHistory(**data)

        # Use it
        last_match_info = history.results[0].match_info
        print(f"Last match played on {last_match_info.start_time:%Y-%m-%d}")


if __name__ == "__main__":
    asyncio.run(main())
```

!!! info "Note"

    If you would prefer to parse responses yourself, it may help to look at some [examples](https://github.com/acurtis166/spnkr/tree/master/tests/responses)

Of course, there are additional methods for retrieving statistics or skill information about matches. Click the button below to see them all.

[Next: Client Methods](reference/client.md#spnkr.client.HaloInfiniteClient){ .md-button }