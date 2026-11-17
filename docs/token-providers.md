# Token Providers

The SPNKr library provides a simple token provider interface for Spartan token authentication. The callable returns an OAuth access token, and the provider handles the full authentication chain internally (OAuth → User token → XSTS token → Spartan token).

## Static Token

For simple cases where you already have a Spartan token:

```python
from spnkr import HaloInfiniteClient

# Option 1: Pass token directly (simplest)
client = HaloInfiniteClient(spartan_token="your_spartan_token_here")

# Option 2: Use StaticTokenProvider explicitly
from spnkr import StaticTokenProvider

provider = StaticTokenProvider("your_spartan_token_here")
client = HaloInfiniteClient(spartan_token=provider)
```

## MSAL Integration with Caching

For OAuth-based authentication with Azure AD / Microsoft identity, with token caching:

```python
import asyncio
from msal import PublicClientApplication
from msal_extensions import PersistedTokenCache, build_encrypted_persistence
from spnkr import HaloInfiniteClient, RefreshTokenProvider

CLIENT_ID = "your_client_id"
OAUTH_CACHE_PATH = "oauth_cache.bin"
AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = ["Xboxlive.signin", "Xboxlive.offline_access"]


async def get_access_token() -> str:
    """Get access token from MSAL with encrypted token caching."""
    # Use encrypted local cache to persist tokens across runs
    persistence = build_encrypted_persistence(OAUTH_CACHE_PATH)
    cache = PersistedTokenCache(persistence)
    app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

    # Try to get token silently from cache first
    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    # Fall back to interactive auth if needed
    if not result:
        result = app.acquire_token_interactive(SCOPES)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Authentication failed: {result.get('error_description')}")


async def main():
    # Create provider with the token function
    provider = RefreshTokenProvider(get_access_token)

    # Use the client - both MSAL caching and RefreshTokenProvider caching work together
    async with HaloInfiniteClient(spartan_token=provider) as client:
        user = await client.get_current_user()
        matches = await client.get_match_history(user.xuid)


asyncio.run(main())
```


## Token Refresh

The token is cached after first retrieval. To explicitly refresh:

```python
# Refresh the cached token
new_token = await provider.refresh()
```

The token will automatically be refreshed if it is about to expire.

## Custom Provider

Implement the `TokenProvider` protocol for custom behavior:

```python
class CustomTokenProvider:
    async def get_token(self) -> SpartanToken: ...


provider = CustomTokenProvider()
client = HaloInfiniteClient(spartan_token=provider)
```
