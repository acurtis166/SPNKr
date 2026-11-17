# Getting Started

Requires Python >=3.11

## Install

```shell
pip install spnkr
```

## Authentication

SPNKr requires a Spartan token for all endpoints. Clearance token is optional and only required for economy endpoints. There are a couple ways to obtain these credentials.

### Option 1 - Static Token

The simplest way is to grab your tokens manually from Halo Waypoint. However, since spartan tokens expire after 4 hours, this approach is best for quick testing or one-off scripts.

See [Option 2 (Azure App Registration)](#option-2---azure-app-registration) below or check out the [Token Providers guide](token-providers.md) for MSAL integration with automatic caching and refresh.

The following instructions are for Google Chrome:

1. Navigate to [Halo Waypoint](https://www.halowaypoint.com/).
1. Click "SIGN IN" at the top right and log in.
1. Click your gamer picture at the top right and select "SERVICE RECORDS" in the dropdown.
1. Under "HALO INFINITE", click "GO TO SERVICE RECORD".
1. Open developer tools (F12 in Google Chrome).
1. Click the "Network" tab
1. Refresh the Waypoint webpage.
1. In developer tools, search the logged network activity for "X-343-Authorization-Spartan" and "343-Clearance" headers. These are your spartan and clearance tokens, respectively. Record them for use in the next step.

!!! note "Clearance Token"
    The clearance token is optional. You only need it if you plan to use economy endpoints like `get_player_customization`, `get_player_career_rank`, or `get_player_reward_track_operations`. All other endpoints work with just the spartan token.

### Option 2 - Azure App Registration

The recommended approach uses Azure AD to automate token refresh, so you don't need to manually grab tokens.

!!! tip "Using MSAL?"
    If you're using Python's [MSAL library](https://github.com/AzureAD/microsoft-authentication-library-for-python) (recommended), check out the [Token Providers guide](token-providers.md) for a complete example. This handles token refresh automatically and securely, though you still need to register an app in Azure.

#### Azure Active Directory Setup

Authentication requires creating an Azure Active Directory (Azure AD) application. Use the account that you play Halo Infinite with, as you will need to be able to acquire Xbox Live and Halo Infinite credentials. These instructions are for creating a confidential client with a secret. You can set up a public client instead, but you will need to use an MSAL token provider instead of the authentication helpers provided.

1. Sign up for a [Microsoft Azure](https://azure.microsoft.com/en-us) account.
1. Register a new application in [Azure AD](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade).
1. Record the client ID, which is available as "Application (client) ID" under the "Overview" tab for your app.
1. Add "https://localhost" as a redirect URI of type "web".
1. Go to "Certificates & secrets" for your app to add a client secret.
1. Record the "Value" of your newly added secret.

#### Initial Authentication

Before initializing the client object and requesting data, you will need to perform the initial OAuth2 authentication step to acquire OAuth access and refresh tokens. This step requires having the client ID, client secret, and redirect URI information from your Azure AD application setup above. Once you have the credentials, you just need to pass the information into a single [function](reference/authentication.md#spnkr.auth.core.authenticate_player) to get your OAuth2 refresh token for future use. Below is an example script to perform this initial authentication. It will involve opening a web page to retrieve an authorization code, but you only need to do this once.

```python
import asyncio

from aiohttp import ClientSession

from spnkr import AzureApp, authenticate_player

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

#### Obtaining Spartan and Clearance Tokens

With your OAuth2 refresh token, you need to perform a series of token requests:

1. Refresh the OAuth2 access token
1. Request an Xbox Live user token
1. Request an Xbox Live XSTS token scoped to Xbox Live services (not strictly necessary, but it returns profile information like your player ID (XUID) and gamertag)
1. Request an Xbox Live XSTS token scoped to Halo services
1. Request a "spartan token", which is required for all endpoints
1. Request a "clearance ID", which is optional but required for some economy endpoints

However, you will again just make a single [function](reference/authentication.md#spnkr.auth.core.refresh_player_tokens) call to refresh/request tokens and return the needed information. The example script below will look similar to our step above, but now we are retrieving spartan and clearance tokens that will be headers for our API calls.

```python
import asyncio

from aiohttp import ClientSession

from spnkr import AzureApp, refresh_player_tokens

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "REDIRECT_URI"
REFRESH_TOKEN = "REFRESH_TOKEN"


async def main() -> None:
    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    async with ClientSession() as session:
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)

    print(f"Spartan token: {player.spartan_token.spartan_token}")  # Valid for 4 hours.
    print(f"Clearance token: {player.clearance_token.flight_configuration_id}")
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

[Next: Basic Usage](basic-usage.md){ .md-button }