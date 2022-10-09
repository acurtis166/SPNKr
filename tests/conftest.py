
import contextlib
import sys

import pytest
import requests

from halo_infinite_api.api.content import ContentClient
from halo_infinite_api.api.profile import ProfileClient
from halo_infinite_api.api.skill import SkillClient
from halo_infinite_api.api.stats import StatsClient
from halo_infinite_api.authentication import manager
from halo_infinite_api.authentication import models

try:
    from tests import config
except ImportError:
    print('No module "config" in the "tests" package. Create one that exports strings: '
        '"client_id", "client_secret", "redirect_uri", and "path_to_oauth" (all strings).')
    sys.exit(1)

collect_ignore = ['setup.py']


@contextlib.contextmanager
def _auth_mgr():
    with requests.session() as sess:
        auth_mgr = manager.AuthenticationManager(sess, config.client_id, config.client_secret,
                                                 config.redirect_uri)
        with open(config.path_to_oauth) as fp:
            oauth_json = fp.read()
        auth_mgr.oauth = models.OAuth2TokenResponse.parse_json(oauth_json)
        auth_mgr.refresh_tokens()
        with open(config.path_to_oauth, 'w') as fp:
            fp.write(auth_mgr.oauth.to_json())
        yield auth_mgr


@pytest.fixture(scope='function')
def content_client():
    with _auth_mgr() as auth_mgr:
        yield ContentClient(auth_mgr)


@pytest.fixture(scope='function')
def profile_client():
    with _auth_mgr() as auth_mgr:
        yield ProfileClient(auth_mgr)


@pytest.fixture(scope='function')
def skill_client():
    with _auth_mgr() as auth_mgr:
        yield SkillClient(auth_mgr)


@pytest.fixture(scope='function')
def stats_client():
    with _auth_mgr() as auth_mgr:
        yield StatsClient(auth_mgr)

