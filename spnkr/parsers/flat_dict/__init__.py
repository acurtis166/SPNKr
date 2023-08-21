"""Parse highlight information from Halo Infinite API responses."""

from .skill import parse_match_skill, parse_playlist_csr
from .stats import (
    parse_match_count,
    parse_match_history,
    parse_match_info,
    parse_player_core_stats,
    parse_player_medals,
    parse_team_core_stats,
)
from .ugc_discovery import parse_asset
