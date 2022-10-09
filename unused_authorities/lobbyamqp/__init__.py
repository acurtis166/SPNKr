""""""

from halo_infinite_api import util
from halo_infinite_api.api.authorities import base
from halo_infinite_api.api.authorities.lobbyamqp import models


class lobbyamqpAuthority(base.BaseAuthority):

    URL = 'https://lobby-hi.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'SecureAmqpWebSocket'

    def gameconnection(self):
        url = self.URL + '/'
        params = ''
        resp = self._session.get(url, params=params)


    def lobbyconnection(self):
        url = self.URL + '/'
        params = ''
        resp = self._session.get(url, params=params)


    def lobbyconnectionpublish(self):
        url = self.URL + '/'
        params = ''
        resp = self._session.get(url, params=params)


    def lobbyconnectionsubscribe(self):
        url = self.URL + '/'
        params = ''
        resp = self._session.get(url, params=params)


