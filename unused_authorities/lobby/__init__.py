""""""

from spnkr import util
from spnkr.api.authorities import base
from spnkr.api.authorities.lobby import models


class lobbyAuthority(base.BaseAuthority):

    URL = 'https://lobby-hi.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'Https'

    def getqosservers(self):
        url = self.URL + '/titles/hi/qosservers'
        params = ''
        resp = self._session.get(url, params=params)


    def joinlobby(self):
        url = self.URL + '/hi/lobbies/{lobbyId}/players/{player}'
        params = '?auth=st'
        resp = self._session.get(url, params=params)


    def lobbypresence(self):
        url = self.URL + '/hi/presence'
        params = ''
        resp = self._session.get(url, params=params)


    def registerjoinlobbyhandle(self):
        url = self.URL + '/hi/handles/{handleId}/players/{player}'
        params = '?auth=st'
        resp = self._session.get(url, params=params)


    def thirdpartyjoinhandle(self):
        url = self.URL + '/hi/lobbies/{lobbyId}/players/{player}/thirdPartyJoinHandle'
        params = '?audience={handleAudience}&platform={handlePlatform}'
        resp = self._session.get(url, params=params)


