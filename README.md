# [SPNKr](https://www.halopedia.org/M41_SPNKr) Halo Infinite API (Python)

This project provides a Python API for requesting multiplayer data from Halo Infinite servers.

Authentication requires some preliminary work:

1. Sign up for a Microsoft Azure account.
1. Register a new application in [Azure AD](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade).
1. Add "http://localhost" as a redirect URI of type "web".
1. Go to "Certificates & secrets" for your app to create a client secret.
1. Save your app's client id, client secret, and redirect URI information.


## Dependencies

- Python >= 3.10
- Libraries:
    - requests for making HTTP requests
    - ms_cv for including a correlation vector header for requests to Microsoft
    - orjson for speedy JSON deserialization
    - pytest for unit testing
    - python-dateutil for parsing isoformat datetime strings


## Getting Started

Install
```
pip install spnkr
```

Example Usage
```python
"""Example usage of the library."""

import pathlib
import requests

from spnkr.api.client import Client
from spnkr.api.enums import PlayerType
from spnkr.authentication.manager import AuthenticationManager
from spnkr.authentication.models import OAuth2TokenResponse


def main():
    # Where the OAuth token should be/is saved
    oauth_token_file = pathlib.Path('path/to/token.json')

    # Azure AD app information
    client_id = 'YOUR CLIENT ID'
    client_secret = 'YOUR CLIENT SECRET'
    redirect_uri = 'http://localhost'

    with requests.session() as sess:
        auth_mgr = AuthenticationManager(sess, client_id, client_secret, redirect_uri)
        client = Client(auth_mgr)

        if oauth_token_file.exists():
            print('Refreshing tokens')
            auth_mgr.oauth = OAuth2TokenResponse.parse_json(oauth_token_file.read_text())
            auth_mgr.refresh_tokens()
        else:
            print('Requesting tokens')
            auth_url = auth_mgr.generate_authorization_url()
            print(auth_url)
            print('Navigate to the above URL and copy the "code" parameter from the query string.')
            code = input('Enter the code...')
            auth_mgr.request_tokens(code)
            oauth_token_file.mkdir(parents=True)

        # Save the token for later
        with oauth_token_file.open('w') as fp:
            fp.write(auth_mgr.oauth.to_json())

        # Get your Xbox Live ID (xuid)
        your_xbox_live_id = auth_mgr.xsts_token.xuid

        # Get your most recent 25 match summaries
        matches = client.stats.get_match_history(your_xbox_live_id)
        match = matches.results[0]  # most recent

        # Get match map/playlist/game variant
        map_variant = client.ugc_discovery.get_map(match.match_info.map_variant.asset_id,
                                                   match.match_info.map_variant.version_id)
        playlist = client.ugc_discovery.get_playlist(match.match_info.playlist.asset_id,
                                                     match.match_info.playlist.version_id)
        game_variant = client.ugc_discovery.get_ugc_game_variant(
            match.match_info.ugc_game_variant.asset_id,
            match.match_info.ugc_game_variant.version_id
        )
        print('Map | Game Type | Playlist')
        print(map_variant.public_name, '|', game_variant.public_name, '|', playlist.public_name)

        # Get match stats
        stats = client.stats.get_match_stats(match.match_id)
        print('Player | Kills | Deaths')
        for player in stats.players:
            core_stats = player.player_team_stats[0].stats.core_stats
            print(player.player_id, '|', core_stats.kills, '|', core_stats.deaths)

        # Get all the human players from the match
        player_ids = [p.player_id for p in stats.players if p.player_type == PlayerType.Human]

        # Get skill info (if applicable)
        try:
            skill = client.skill.get_match_result(match.match_id, player_ids)
        except requests.HTTPError:
            print(f'No skill info available for match {match.match_id}')
            exit()

        # Print out CSRs
        print('Player | Pre-Match CSR | Post-Match CSR')
        for entry in skill.value:
            print(entry.id, '|', entry.result.rank_recap.pre_match_csr, '|',
                  entry.result.rank_recap.post_match_csr)


if __name__ == '__main__':
    main()
```


## Contribute

- Implement/update authorities/endpoints
    - [Source (no auth needed)](https://settings.svc.halowaypoint.com/settings/hipc/e2a0a7c6-6efe-42af-9283-c2ab73250c48)
    - [Endpoints (JSON)](https://github.com/acurtis166/spnkr/blob/master/api_examples/json/endpoints.json)
    - [Endpoints (XML)](https://github.com/acurtis166/spnkr/blob/master/api_examples/xml/endpoints.xml)
    - [Script-generated code files](https://github.com/acurtis166/spnkr/tree/master/unused_authorities)
- Documentation
- Enumerated data type completion/confirmation


## Credits

- Xbox authentication, profile endpoints: [OpenXbox/xbox-webapi-python](https://github.com/OpenXbox/xbox-webapi-python)
- Halo Infinite authentication [Den Delimarsky](https://den.dev/blog/halo-api-authentication)
- Halo Infinite endpoints, schema, enumerated data types [OpenSpartan/grunt](https://github.com/OpenSpartan/grunt)
- Microsoft/343 Industries


## Disclaimer

This software is not endorsed or supported by Microsoft or 343 Industries. It is a personal project with a goal of analyzing Halo Infinite match data.

As the authentication process requires usage of personal credentials, **use at your own risk** of action by Microsoft or 343 Industries.