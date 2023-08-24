This site documents the Python package SPNKr, an API for requesting multiplayer data from Halo Infinite servers.

[PyPI](https://pypi.org/project/spnkr/)

[GitHub](https://github.com/acurtis166/spnkr)

## Getting Started

Requires Python >=3.11

### Install

Basic
```shell
pip install spnkr
```

Include Pydantic parsing functionality
```shell
pip install spnkr[pydantic]
```

Development
```shell
pip install spnkr[dev]
```

### Azure Active Directory Setup

Authentication requires creating an Azure Active Directory (Azure AD) application. Use the account that you play Halo Infinite with, as you will need to be able to acquire Xbox Live and Halo Infinite credentials.

1. Sign up for a Microsoft Azure account.
1. Register a new application in [Azure AD](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade).
1. Add "https://localhost" as a redirect URI of type "web".
1. Go to "Certificates & secrets" for your app to create a client secret.
1. Save your app's client ID, client secret, and redirect URI information.

## Basic Usage

### Initial Authentication

Before initializing the client object, you will need to perform the initial OAuth2 authentication step to acquire OAuth access and refresh tokens. This step requires having the client ID, client secret, and redirect URI information from your Azure AD application setup. Once you have the credentials, you just need to pass the information into a single function to get your OAuth2 refresh token for future use. Below is an example script to perform this initial authentication. It will involve opening a webpage to retrieve an authorization code, but you only need to do this once.

Note that this package depends on [aiohttp](https://docs.aiohttp.org/en/stable/) for asyncronous requests. You may want to understand the basics of the [ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html#client-session) and [ClientResponse](https://docs.aiohttp.org/en/stable/client_reference.html#response-object) classes to get the most out of this package.

```python
import asyncio

from aiohttp import ClientSession

from spnkr.auth import AzureApp, authenticate_player

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "REDIRECT_URI"


async def main() -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    async with ClientSession() as session:
        refresh_token = await authenticate_player(session, app)

    print(f"Your refresh token is:\n{refresh_token}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Obtaining Spartan and Clearance Tokens

The next authentication step is a series of token requests beginning with a refresh of the OAuth2 token obtained above. You need the same information as before along with the refresh token. The example script below will look similar to our step above, but now we are retrieving spartan and clearance tokens that will be headers for our API calls.

```python
# imports

from spnkr.auth import AzureApp, refresh_player_tokens

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "REDIRECT_URI"
REFRESH_TOKEN = "REFRESH_TOKEN"


async def main() -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    async with ClientSession() as session:
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)

    # Primary means of authorization for API calls, valid for 4 hours
    print(f"Spartan token: {player.spartan_token.token}")

    # Required for some endpoints
    print(f"Clearance token: {player.clearance_token.token}")

    # Additional info from the authentication process
    print(f"Xbox Live User ID (XUID): {player.player_id}")
    print(f"Xbox Live Gamertag: {player.gamertag}")
    print(f"Xbox Live Authorization: {player.xbl_authorization_header_value}")


if __name__ == "__main__":
    asyncio.run(main())
```

The spartan token and clearance token are the main targets of this step, as they are needed to initialize the client object. However, the above script also highlights additional info retrieved during authentication.

- **Xbox Live User ID (XUID)** - This ID is unique to your Xbox Live account. XUIDs are also the identifying attribute for player-specific data retrieved from the API. Additionally, XUIDs are required for certain endpoints in order to retrieve player-specific data.
- **Xbox Live Gamertag** - This is the display name for Xbox Live accounts.
- **Xbox Live Authorization** - This is a value required when making requests to the Xbox Live API. While outside the scope of this project, you could use this to request profile information using XUIDs. Here is an example endpoint for obtaining Xbox Live profiles for a batch of XUIDs: [Batch Profile POST](https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/reference/live/rest/uri/profilev2/uri-usersbatchprofilesettingspost). An alternative solution to making these requests yourself is to use a package such as [xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python).

### Initializing the HaloInfiniteClient

Now that we have the spartan and clearance tokens, we are ready to create a client object. The constructor takes a `aiohttp.ClientSession` instance and the tokens as arguments. An example is shown below.

```python
# imports

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

### Requesting Data

Now that we have the HaloInfiniteClient initialized, we can begin making requests. A simple continuation of the above script is shown below.

```python
# imports

# Player XUID obtained earlier (or any other XUID)
PLAYER_ID = "xuid(123)"


async def main() -> None:
    async with ClientSession() as session:
        client = HaloInfiniteClient(...)

        response = await client.get_match_history(
            xuid=PLAYER_ID,
            start=0,  # Optional, indicates the index of the first result to return.
            count=25,  # Optional, indicates the number of results to return.
            match_type="all",  # Optional, potentially filter the matches returned.
        )


if __name__ == "__main__":
    asyncio.run(main())
```

The above example would retrieve information about your 25 most recent matches. Of course, there are more methods for retrieving details statistics or skill information about matches. These are detailed [here](reference.md).

### Parsing Responses

API calls return JSON payloads, but these are not deserialized by the client. Instead, client methods return raw `aiohttp.ClientResponse` objects to be handled by the user. That being said, two built-in parsing strategies are available.

- **Pydantic** - Parse deserialized JSON responses into [Pydantic](https://docs.pydantic.dev/latest/) models.
- **Records** - Parse JSON responses into flat, record-like named tuples with only highlighted information. While not as complete as the Pydantic models, they are likely more convenient to load into a `pandas.DataFrame` or dump to files/databases.

The classes and functions for these parsers are available in the `spnkr.parsers` module. Applicable parsing objects are referenced by client methods and are detailed [here](reference.md).

Below is a continuation of our above script with parsing of the JSON into a `spnkr.parsers.pydantic.stats.MatchHistory` Pydantic model.

```python
# imports

from spnkr.parsers.pydantic import MatchHistory


async def main() -> None:
    async with ClientSession() as session:
        client = HaloInfiniteClient(...)
        response = await client.get_match_history(...)

        # Deserialize the JSON response
        data = await response.json()

        # Initialize the model
        history = MatchHistory(**data)

        # Use it
        last_match_info = history.results[0].match_info
        print(f"Last match played on {last_match_info.start_time:%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Acknowledgements

- Xbox authentication [OpenXbox/xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python)
- Halo Infinite authentication [Den Delimarsky](https://den.dev/blog/halo-api-authentication)
- Halo Infinite endpoints, schema, enumerated data types [OpenSpartan/grunt](https://github.com/OpenSpartan/grunt)
- Microsoft/343 Industries

## Disclaimer

This software is not endorsed or supported by Microsoft or 343 Industries. It is a personal project with the goal of analyzing Halo Infinite match data.

As the authentication process requires usage of personal credentials, **use at your own risk** of action by Microsoft or 343 Industries.