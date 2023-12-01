# Getting Started

Requires Python >=3.11

## Install

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

## Azure Active Directory Setup

Authentication requires creating an Azure Active Directory (Azure AD) application. Use the account that you play Halo Infinite with, as you will need to be able to acquire Xbox Live and Halo Infinite credentials.

1. Sign up for a [Microsoft Azure](https://azure.microsoft.com/en-us) account.
1. Register a new application in [Azure AD](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade).
1. Add "https://localhost" as a redirect URI of type "web".
1. Go to "Certificates & secrets" for your app to create a client secret.
1. Save your app's client ID, client secret, and redirect URI information.

## Initial Authentication

Before initializing the client object and requesting data, you will need to perform the initial OAuth2 authentication step to acquire OAuth access and refresh tokens. This step requires having the client ID, client secret, and redirect URI information from your Azure AD application setup above. Once you have the credentials, you just need to pass the information into a single [function](reference/authentication.md#spnkr.auth.core.authenticate_player) to get your OAuth2 refresh token for future use. Below is an example script to perform this initial authentication. It will involve opening a web page to retrieve an authorization code, but you only need to do this once.

!!! info "Note"
    This package depends on [aiohttp](https://docs.aiohttp.org/en/stable/) for making asyncronous requests. You may want to understand the basics of the [ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html#client-session) class.

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

[Next: Basic Usage](basic-usage.md){ .md-button }