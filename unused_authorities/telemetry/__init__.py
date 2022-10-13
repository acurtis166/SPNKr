""""""

from haloinfinite import util
from haloinfinite.api.authorities import base
from haloinfinite.api.authorities.telemetry import models


class telemetryAuthority(base.BaseAuthority):

    URL = 'https://telemetry-clients.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'SecureAmqpWebSocket'

    def highpriority(self):
        url = self.URL + '/'
        params = ''
        resp = self._session.get(url, params=params)


    def lowpriority(self):
        url = self.URL + '/'
        params = ''
        resp = self._session.get(url, params=params)


