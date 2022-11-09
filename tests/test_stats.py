
from spnkr.api.client import Client

ACURTIS_XUID = '2535445291321133'
ELIMINATION_MATCH = '6ff6af98-5696-413a-a315-afc74e36fdbe'
STRONGHOLDS_MATCH = 'f43ddeda-a308-4305-b485-764f53a35c69'
ODDBALL_MATCH = '32615069-ccbe-4e00-8cc1-2412ff57bddc'
SLAYER_RANKED_MATCH = '8d641322-8553-44f0-b991-89d028377c62'


def test_get_match_count(client: Client):
    result = client.stats.get_match_count(ACURTIS_XUID)
    assert result.matches_played_count > 900


def test_get_match_history(client: Client):
    result = client.stats.get_match_history(ACURTIS_XUID)
    assert result.result_count == 25


def test_get_match_stats_elimination(client: Client):
    result = client.stats.get_match_stats(ELIMINATION_MATCH)
    assert len(result.players) > 0


def test_get_match_stats_strongholds(client: Client):
    result = client.stats.get_match_stats(STRONGHOLDS_MATCH)
    assert len(result.players) > 0


def test_get_match_stats_oddball(client: Client):
    result = client.stats.get_match_stats(ODDBALL_MATCH)
    assert len(result.players) > 0

