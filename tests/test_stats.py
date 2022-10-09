
from halo_infinite_api.api import stats

ACURTIS_XUID = '2535445291321133'
ELIMINATION_MATCH = '6ff6af98-5696-413a-a315-afc74e36fdbe'
SLAYER_RANKED_MATCH = '8d641322-8553-44f0-b991-89d028377c62'


def test_get_match_count(stats_client: stats.StatsClient):
    result = stats_client.get_match_count(ACURTIS_XUID)
    assert result.matches_played_count > 900


def test_get_match_history(stats_client: stats.StatsClient):
    result = stats_client.get_match_history(ACURTIS_XUID)
    assert result.result_count == 25


def test_get_match_stats(stats_client: stats.StatsClient):
    result = stats_client.get_match_stats(ELIMINATION_MATCH)
    assert len(result.players) > 0

