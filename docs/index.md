# Welcome to SPNKr

## About

[SPNKr](https://www.halopedia.org/M41_SPNKr) is a Python API for retrieving [Halo Infinite](https://www.halowaypoint.com/halo-infinite) multiplayer data. [Halo 5](https://www.halopedia.org/Halo_5:_Guardians), 343 Industries' previous entry in the FPS series, had a [public API](https://developer.haloapi.com/) directly from 343 Industries. It is thorough and has great documentation. It made it incredibly easy to inspect match history, player stats, etc. in a personalized way. Currently, there is no such public API available for Halo Infinite. This project began as an effort to replicate the functionality of the Halo 5 API for Python developers.

### Links

- [Documentation]()
- [PyPI](https://pypi.org/project/spnkr/)
- [GitHub](https://github.com/acurtis166/spnkr)

## Acknowledgements

- Xbox Live authentication flow: [OpenXbox/xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python)
- Halo Infinite authentication flow, endpoints, schema, enumerated data types: [Den Delimarsky](https://den.dev/blog/halo-api-authentication)
- Microsoft/343 Industries

!!! warning "Disclaimer"

    This software is not endorsed or supported by Microsoft or 343 Industries. It is a personal project with the goal of analyzing Halo Infinite match data.

    As the authentication process requires usage of personal credentials, **use at your own risk** of action by Microsoft or 343 Industries.

[Get Started](getting-started.md){ .md-button }