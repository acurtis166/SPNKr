""""""

from haloinfinite import util
from haloinfinite.api.authorities import base
from haloinfinite.api.authorities.hiugc_authoring_authority import models


class hiugc_authoring_authorityAuthority(base.BaseAuthority):

    URL = 'https://authoring-infiniteugc.svc.halowaypoint.com:443'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'Https'

    def checkassetplayerbookmark(self):
        url = self.URL + '/{title}/players/{player}/favorites/{assetType}/{assetId}'
        params = ''
        resp = self._session.get(url, params=params)


    def createassetversionagnostic(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions'
        params = ''
        resp = self._session.get(url, params=params)


    def deleteallversions(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions'
        params = ''
        resp = self._session.get(url, params=params)


    def deleteasset(self):
        url = self.URL + '/{title}/{assetType}/{assetId}'
        params = ''
        resp = self._session.get(url, params=params)


    def deleteversion(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions/{versionId}'
        params = ''
        resp = self._session.get(url, params=params)


    def endsession(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/sessions/active'
        params = ''
        resp = self._session.get(url, params=params)


    def favoriteanasset(self):
        url = self.URL + '/hi/players/{player}/favorites/{assetType}/{assetId}'
        params = ''
        resp = self._session.get(url, params=params)


    def getasset(self):
        url = self.URL + '/{title}/{assetType}/{assetId}'
        params = ''
        resp = self._session.get(url, params=params)


    def getlatestassetversion(self):
        url = self.URL + '/{title}/films/{assetId}/versions/latest'
        params = ''
        resp = self._session.get(url, params=params)


    def getlatestassetversionagnostic(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions/latest'
        params = ''
        resp = self._session.get(url, params=params)


    def getpublishedversion(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions/published'
        params = ''
        resp = self._session.get(url, params=params)


    def getspecificassetversion(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions/{versionId}'
        params = ''
        resp = self._session.get(url, params=params)


    def listallversions(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions'
        params = ''
        resp = self._session.get(url, params=params)


    def listplayerassets(self):
        url = self.URL + '/{title}/players/{player}/assets'
        params = ''
        resp = self._session.get(url, params=params)


    def listplayerfavorites(self):
        url = self.URL + '/hi/players/{player}/favorites/{assetType}'
        params = ''
        resp = self._session.get(url, params=params)


    def listplayerfavoritesagnostic(self):
        url = self.URL + '/hi/players/{player}/favorites'
        params = ''
        resp = self._session.get(url, params=params)


    def patchassetversion(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions/{versionId}'
        params = ''
        resp = self._session.get(url, params=params)


    def publishassetversion(self):
        url = self.URL + '/hi/{assetType}/{assetId}/publish/{versionId}'
        params = '?clearanceId={clearanceId}'
        resp = self._session.get(url, params=params)


    def rateanasset(self):
        url = self.URL + '/hi/players/{player}/ratings/{assetType}/{assetId}'
        params = ''
        resp = self._session.get(url, params=params)


    def reportanasset(self):
        url = self.URL + '/hi/players/{player}/reports/{assetType}/{assetId}'
        params = ''
        resp = self._session.get(url, params=params)


    def spawnasset(self):
        url = self.URL + '/{title}/{assetType}'
        params = ''
        resp = self._session.get(url, params=params)


    def spectatefilm(self):
        url = self.URL + '/hi/films/{assetId}/spectate'
        params = ''
        resp = self._session.get(url, params=params)


    def startsessionagnostic(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/sessions'
        params = '?include-container-sas={includeContainerSas}'
        resp = self._session.get(url, params=params)


    def stringvalidation(self):
        url = self.URL + '/{title}/validation/strings'
        params = ''
        resp = self._session.get(url, params=params)


    def undeleteasset(self):
        url = self.URL + '/{title}/{assetType}/{assetId}'
        params = ''
        resp = self._session.get(url, params=params)


    def undeleteversion(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/versions/{versionId}/recover'
        params = ''
        resp = self._session.get(url, params=params)


    def unpublishasset(self):
        url = self.URL + '/hi/{assetType}/{assetId}/unpublish'
        params = ''
        resp = self._session.get(url, params=params)


    def uploadimage(self):
        url = self.URL + '/{title}/{assetType}/{assetId}/sessions/{sessionId}/Image/{filePath}'
        params = '?player={player}'
        resp = self._session.get(url, params=params)


