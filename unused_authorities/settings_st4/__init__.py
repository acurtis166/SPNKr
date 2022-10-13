""""""

from spnkr import util
from spnkr.api.authorities import base
from spnkr.api.authorities.settings_st4 import models


class settings_st4Authority(base.BaseAuthority):

    URL = 'https://settings.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'Https'

    def getflightedfeatureflags(self):
        url = self.URL + '/featureflags/hi'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def activeflight(self):
        url = self.URL + '/oban/flight-configurations/titles/hi/audiences/RETAIL/active'
        params = '?sandbox={sandbox}&build={buildNumber}'
        resp = self._session.get(url, params=params)


    def getclearance(self):
        url = self.URL + '/oban/flight-configurations/titles/hi/audiences/{audience}/active'
        params = '?sandbox={sandbox}&build={buildNumber}'
        resp = self._session.get(url, params=params)


    def getplayerclearance(self):
        url = self.URL + '/oban/flight-configurations/titles/hi/audiences/{audience}/players/{player}/active'
        params = '?sandbox={sandbox}&build={buildNumber}'
        resp = self._session.get(url, params=params)


    def playerclearance(self):
        url = self.URL + '/oban/flight-configurations/titles/hi/audiences/RETAIL/players/{player}/active'
        params = '?sandbox={sandbox}&build={buildNumber}'
        resp = self._session.get(url, params=params)


