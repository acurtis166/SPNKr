""""""

from halo_infinite_api import util
from halo_infinite_api.api.authorities import base
from halo_infinite_api.api.authorities.settings import models


class settingsAuthority(base.BaseAuthority):

    URL = 'https://settings.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['XSTSv3HaloAudience', 'ClientCertificate']
    SCHEME = 'Https'

    def getfeatureflags(self):
        url = self.URL + '/featureflags/{platform}/{version}'
        params = ''
        resp = self._session.get(url, params=params)


