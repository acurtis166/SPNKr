"""Example usage of the library."""

import pathlib
import requests

from halo_infinite_api.api.client import Client
from halo_infinite_api.api.enums import PlayerType
from halo_infinite_api.authentication.manager import AuthenticationManager
from halo_infinite_api.authentication.models import OAuth2TokenResponse


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

