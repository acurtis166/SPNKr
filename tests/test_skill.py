
from halo_infinite_api.api import skill

ACURTIS_XUID = '2535445291321133'
ELIMINATION_MATCH = '6ff6af98-5696-413a-a315-afc74e36fdbe'
SLAYER_RANKED_MATCH = '8d641322-8553-44f0-b991-89d028377c62'
SLAYER_RANKED_PLAYLIST = 'edfef3ac-9cbe-4fa2-b949-8f29deafd483'


def test_get_match_result(skill_client: skill.SkillClient):
    result = skill_client.get_match_result(SLAYER_RANKED_MATCH, [ACURTIS_XUID])
    assert len(result.value) == 1


def test_get_playlist_csr(skill_client: skill.SkillClient):
    result = skill_client.get_playlist_csr(SLAYER_RANKED_PLAYLIST, [ACURTIS_XUID])
    assert len(result.value) == 1

