# [SPNKr](https://www.halopedia.org/M41_SPNKr) Halo Infinite API (Python)

This project provides a Python API for requesting multiplayer data from Halo Infinite servers.

Authentication requires some preliminary work:

1. Sign up for a Microsoft Azure account.
1. Register a new application in [Azure AD](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade).
1. Add "http://localhost" as a redirect URI of type "web".
1. Go to "Certificates & secrets" for your app to create a client secret.
1. Save your app's client id, client secret, and redirect URI information.

## Dependencies

- Python >= 3.11
- Required Packages:
    - `aiohttp` for making HTTP requests
    - `aiolimiter` for limiting requests per second
- Optional Packages:
    - `pydantic` for using provided Pydantic models to parse reponses

## Getting Started

### Install

Basic
```
pip install spnkr
```

Include Pydantic parsing functionality
```
pip install spnkr[pydantic]
```

All optional packages
```
pip install spnkr[dev]
```

### Example Usage

See [scripts](https://github.com/acurtis166/spnkr/tree/master/scripts) for authentication and usage examples.

Note that in order to run all scripts without modification, you will need to install additional packages (`pandas`, `python-dotenv`, and `aiofiles`).

1. Create your Azure Active Directory application as described above.
1. Store your client ID, client secret, and redirect URI values for the application. The solution provided in the example scripts uses a `.env` file to store the values and loads them in using [python-dotenv](https://pypi.org/project/python-dotenv/).
1. Retrieve an OAuth2 refresh token by performing the initial authentication (see `scripts/authenticate.py`). Store this with your other configuration values.
1. You can now refresh tokens to obtain a spartan token and clearance token for authorization at the API endpoints.
1. Initialize a `spnkr.client.HaloInfiniteClient` with the tokens and begin making requests as shown in the example scripts.

### Parsing

Client methods return raw [ClientResponse](https://docs.aiohttp.org/en/stable/client_reference.html#response-object) objects. It is up to the user to parse the JSON content. Two parsing strategies are provided in the `spnkr.parsers` module, pydantic and records.

Pydantic parsing provides Pydantic models that can be used to parse the deserialized JSON. The models are mostly complete representations of the source schema. This makes them fully functional for any use case, but the data structure might be cumbersome if you just want to grabs kill and death counts.

```python
# Import the appropriate model
from spnkr.parsers.pydantic import MatchHistory

# Make the client request
response = client.get_match_history("xuid(123)")

# Deserialize the JSON response
data = await response.json()

# Initialize the Pydantic model
history = MatchHistory(**data)

most_recent = history.results[0]
print(f"Last match played on {most_recent.match_info.start_time:%Y-%m-%d %H:%M}")
```

Record parsing uses functions to parse the JSON responses into flat, record-like named tuples. They aren't as complete as the Pydantic models, but they are likely more convenient if you want to load them into a `pandas.DataFrame` or dump them to files/databases.

```python
# Import the appropriate parsing function(s)
from spnkr.parsers.records import parse_match_history

# Make the client request
response = client.get_match_history("xuid(123)")

# Deserialize the JSON response
data = await response.json()

# Parse to records
history = parse_match_history(data)

most_recent = history[0]
print(f"Last match played on {most_recent.start_time:%Y-%m-%d %H:%M}")
```

If you would prefer to parse the responses yourself, check out example responses in the [tests/responses](https://github.com/acurtis166/spnkr/tree/master/tests/responses) folder.

Due to incomplete test data, some enumerated data types may be incomplete. If you encounter one of these, please submit an issue or pull request.

### Profile Information

Note that no functionality is available in this project to look up profile information, such as gamertags, using player ids (XUIDs). This was determined to be outside the scope of the project. However, if you are interested in looking up profile information, check out the following resources:

- [OpenXbox/xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python) is a Python package for interacting with the Xbox Live API.
- [Batch Profile POST](https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/reference/live/rest/uri/profilev2/uri-usersbatchprofilesettingspost) is an Xbox Live API endpoint that allows you to submit a batch of XUIDs and receive profile information. If you would like to make the profile requests yourself, you can grab the Xbox Live API "Authorization" header value from the `AuthenticatedPlayer` object that is returned from the `refresh_player_tokens()` function call. The attribute name is `xbl_authorization_header_value`.

## Credits

- Xbox authentication [OpenXbox/xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python)
- Halo Infinite authentication [Den Delimarsky](https://den.dev/blog/halo-api-authentication)
- Halo Infinite endpoints, schema, enumerated data types [OpenSpartan/grunt](https://github.com/OpenSpartan/grunt)
- Microsoft/343 Industries

## Disclaimer

This software is not endorsed or supported by Microsoft or 343 Industries. It is a personal project with the goal of analyzing Halo Infinite match data.

As the authentication process requires usage of personal credentials, **use at your own risk** of action by Microsoft or 343 Industries.