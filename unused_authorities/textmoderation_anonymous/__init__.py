""""""

from haloinfinite import util
from haloinfinite.api.authorities import base
from haloinfinite.api.authorities.textmoderation_anonymous import models


class textmoderation_anonymousAuthority(base.BaseAuthority):

    URL = 'https://text.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = [None]
    SCHEME = 'Https'

    def getsigningkey(self):
        url = self.URL + '/hi/moderation-proof-keys//{keyId}'
        params = ''
        resp = self._session.get(url, params=params)


    def getsigningkeys(self):
        url = self.URL + '/hi/moderation-proof-keys'
        params = ''
        resp = self._session.get(url, params=params)


