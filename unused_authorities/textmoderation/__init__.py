""""""

from haloinfinite import util
from haloinfinite.api.authorities import base
from haloinfinite.api.authorities.textmoderation import models


class textmoderationAuthority(base.BaseAuthority):

    URL = 'https://text.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'Https'

    def postinappropriatemessagereport(self):
        url = self.URL + '/hi/players/{player}/text-message-reports'
        params = ''
        resp = self._session.get(url, params=params)


    def posttextformoderation(self):
        url = self.URL + '/hi/players/{player}/text-messages'
        params = ''
        resp = self._session.get(url, params=params)


