
import contextlib
import sys

import pytest
import requests

from haloinfinite.api.client import Client
from haloinfinite.authentication import manager
from haloinfinite.authentication import models

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
def client():
    with _auth_mgr() as auth_mgr:
        yield Client(auth_mgr)

