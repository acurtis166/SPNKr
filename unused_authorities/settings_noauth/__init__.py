""""""

from spnkr import util
from spnkr.api.authorities import base
from spnkr.api.authorities.settings_noauth import models


class settings_noauthAuthority(base.BaseAuthority):

    URL = 'https://settings.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = [None]
    SCHEME = 'Https'

    def spartantokenv4(self):
        url = self.URL + '/spartan-token'
        params = ''
        resp = self._session.get(url, params=params)


