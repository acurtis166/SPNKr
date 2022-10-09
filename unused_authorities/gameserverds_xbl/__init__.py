""""""

from halo_infinite_api import util
from halo_infinite_api.api.authorities import base
from halo_infinite_api.api.authorities.gameserverds_xbl import models


class gameserverds_xblAuthority(base.BaseAuthority):

    URL = 'https://gameserverds.xboxlive.com:443'
    AUTHENTICATION_METHODS = ['XSTSv3XboxAudience']
    SCHEME = 'Https'

    def qosendpoints(self):
        url = self.URL + '/xplatqosservers'
        params = ''
        resp = self._session.get(url, params=params)


