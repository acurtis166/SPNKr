# Welcome to SPNKr

## About

[SPNKr](https://www.halopedia.org/M41_SPNKr) is a Python API for retrieving [Halo Infinite](https://www.halowaypoint.com/halo-infinite) multiplayer data. [Halo 5](https://www.halopedia.org/Halo_5:_Guardians), 343 Industries' previous entry in the FPS series, has a [public API](https://developer.haloapi.com/) available. Currently, there is no such public API available for Halo Infinite. This project began as an effort to replicate the functionality of the Halo 5 API for Python developers.

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
