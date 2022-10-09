""""""

from halo_infinite_api import util
from halo_infinite_api.api.authorities import base
from halo_infinite_api.api.authorities.iugcfiles import models


class iugcfilesAuthority(base.BaseAuthority):

    URL = 'https://blobs-infiniteugc.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = [None]
    SCHEME = 'Https'

    def getblob(self):
        url = self.URL + ''
        params = ''
        resp = self._session.get(url, params=params)


