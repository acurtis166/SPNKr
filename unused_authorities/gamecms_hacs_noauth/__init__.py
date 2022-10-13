""""""

from spnkr import util
from spnkr.api.authorities import base
from spnkr.api.authorities.gamecms_hacs_noauth import models


class gamecms_hacs_noauthAuthority(base.BaseAuthority):

    URL = 'https://gamecms-hacs.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = [None]
    SCHEME = 'Https'

    def getnotallowedintitlemessage(self):
        url = self.URL + '/branches/hi/OEConfiguration/data/authfail/Default.json'
        params = ''
        resp = self._session.get(url, params=params)


