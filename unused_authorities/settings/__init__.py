""""""

from spnkr import util
from spnkr.api.authorities import base
from spnkr.api.authorities.settings import models


class settingsAuthority(base.BaseAuthority):

    URL = 'https://settings.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['XSTSv3HaloAudience', 'ClientCertificate']
    SCHEME = 'Https'

    def getfeatureflags(self):
        url = self.URL + '/featureflags/{platform}/{version}'
        params = ''
        resp = self._session.get(url, params=params)


