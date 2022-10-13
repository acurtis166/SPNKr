""""""

from haloinfinite import util
from haloinfinite.api.authorities import base
from haloinfinite.api.authorities.gamecms_hacs import models


class gamecms_hacsAuthority(base.BaseAuthority):

    URL = 'https://gamecms-hacs.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'Https'

    def getbotcustomization(self):
        url = self.URL + '/hi/multiplayer/file/Academy/BotCustomizationData.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getcontenttest(self):
        url = self.URL + '/hi/multiplayer/file/Academy/AcademyClientManifest_Test.json'
        params = '?flight={clearanceId}'
        resp = self._session.get(url, params=params)


