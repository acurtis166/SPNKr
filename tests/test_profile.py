
from spnkr.api.client import Client

ACURTIS_XUID = '2535445291321133'
ACURTIS_GAMERTAG = 'aCurtis X89'


def test_get_profiles(client: Client):
    result = client.profile.get_profiles([ACURTIS_XUID])
    assert len(result.profile_users) == 1


def test_get_profile_by_xuid(client: Client):
    result = client.profile.get_profile_by_xuid(ACURTIS_XUID)
    assert len(result.profile_users) == 1


def test_get_profile_by_gamertag(client: Client):
    result = client.profile.get_profile_by_gamertag(ACURTIS_GAMERTAG)
    assert len(result.profile_users) == 1
    
