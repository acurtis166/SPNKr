""""""

from halo_infinite_api import util
from halo_infinite_api.api.authorities import base
from halo_infinite_api.api.authorities.gamecmsorigin import models


class gamecmsoriginAuthority(base.BaseAuthority):

    URL = 'https://gamecms-hacs.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'Https'

    def origin(self):
        url = self.URL + '://{path}'
        params = ''
        resp = self._session.get(url, params=params)


