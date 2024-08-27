# Welcome to SPNKr

## About

[SPNKr](https://www.halopedia.org/M41_SPNKr) is a Python wrapper around the undocumented Halo Infinite web API. This is a personal project with the goal of analyzing Halo Infinite matchmaking data. It is not in any way official or connected to Microsoft/343 Industries and does not provide any guarantees of completeness or API availability. Use at your own risk. The functionality is available via a public repository on GitHub and as a package published to PyPI.

### Links

- [Documentation](https://acurtis166.github.io/SPNKr/)
- [PyPI](https://pypi.org/project/spnkr/)
- [GitHub](https://github.com/acurtis166/spnkr)

## Acknowledgements

- Xbox Live authentication flow: [OpenXbox/xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python)
- Halo Infinite authentication flow, endpoints, schema, enumerated data types: [Den Delimarsky](https://den.dev/blog/halo-api-authentication)
- Microsoft/343 Industries

## Disclaimer

This software is not endorsed or supported by Microsoft or 343 Industries. It is a personal project with the goal of analyzing Halo Infinite match data.

As the authentication process requires usage of personal credentials, **use at your own risk** of action by Microsoft or 343 Industries.

## Dependencies

- Python >= 3.11
- Required Packages:
    - `aiohttp` for making asyncronous HTTP requests
    - `aiolimiter` for limiting requests per second
    - `pydantic` for parsing responses into Pydantic models
    - `bitstring` for unpacking data from binary film files

## Contributions

Contributions to fix issues or add support for more endpoints are welcomed.
