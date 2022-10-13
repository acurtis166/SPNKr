""""""

from spnkr import util
from spnkr.api.authorities import base
from spnkr.api.authorities.iugcfiles import models


class iugcfilesAuthority(base.BaseAuthority):

    URL = 'https://blobs-infiniteugc.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = [None]
    SCHEME = 'Https'

    def getblob(self):
        url = self.URL + ''
        params = ''
        resp = self._session.get(url, params=params)


