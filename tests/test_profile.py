
from halo_infinite_api.api import profile

ACURTIS_XUID = '2535445291321133'
ACURTIS_GAMERTAG = 'aCurtis X89'


def test_get_profiles(profile_client: profile.ProfileClient):
    result = profile_client.get_profiles([ACURTIS_XUID])
    assert len(result.profile_users) == 1


def test_get_profile_by_xuid(profile_client: profile.ProfileClient):
    result = profile_client.get_profile_by_xuid(ACURTIS_XUID)
    assert len(result.profile_users) == 1


def test_get_profile_by_gamertag(profile_client: profile.ProfileClient):
    result = profile_client.get_profile_by_gamertag(ACURTIS_GAMERTAG)
    assert len(result.profile_users) == 1
    
