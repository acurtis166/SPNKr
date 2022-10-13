""""""

from haloinfinite import util
from haloinfinite.api.authorities import base
from haloinfinite.api.authorities.gamecms import models


class gamecmsAuthority(base.BaseAuthority):

    URL = 'https://gamecms:None'
    AUTHENTICATION_METHODS = ['SpartanTokenV4']
    SCHEME = 'GameCms'

    def getcontent(self):
        url = self.URL + '/hi/multiplayer/file/Academy/AcademyClientManifest.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getstardefinitions(self):
        url = self.URL + '/hi/multiplayer/file/Academy/AcademyStarGUIDDefinitions.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getachievements(self):
        url = self.URL + '/hi/Multiplayer/file/Live/Achievements.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getarmorcoremanifest(self):
        url = self.URL + '/hi/Progression/file/Inventory/Manifest/armorcores.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getasynccomputeoverrides(self):
        url = self.URL + '/hi/Specs/file/graphics/AsyncComputeOverrides.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getbanmessage(self):
        url = self.URL + '/hi/Banning/file/{banMessagePath}'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getchallenge(self):
        url = self.URL + '/hi/Progression/file/{challengePath}'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getchallengedeck(self):
        url = self.URL + '/hi/Progression/file/{challengeDeckPath}'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getclawaccess(self):
        url = self.URL + '/hi/TitleAuthorization/file/claw/access.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getcpupresets(self):
        url = self.URL + '/hi/Specs/file/cpu/presets.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getcustomgamedefaults(self):
        url = self.URL + '/hi/Multiplayer/file/NonMatchmaking/customgame.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getcustomizationcatalog(self):
        url = self.URL + '/hi/Progression/file/inventory/catalog/inventory_catalog.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getdevicepresetoverrides(self):
        url = self.URL + '/hi/Specs/file/graphics/DevicePresetOverrides.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getevent(self):
        url = self.URL + '/hi/Progression/file/{eventPath}'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def geteventmanifest(self):
        url = self.URL + '/hi/Progression/file/RewardTracks/Manifest/eventmanifest.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getgraphicsspeccontroloverrides(self):
        url = self.URL + '/hi/Specs/file/graphics/GraphicsSpecControlOverrides.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getgraphicspecs(self):
        url = self.URL + '/hi/Specs/file/graphics/overrides.json'
        params = ''
        resp = self._session.get(url, params=params)


    def images(self):
        url = self.URL + '/hi/images/guide/xo'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def multiplayer(self):
        url = self.URL + '/hi/Multiplayer/guide/xo'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def news(self):
        url = self.URL + '/hi/News/guide/xo'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def progression(self):
        url = self.URL + '/hi/Progression/guide/xo'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def specs(self):
        url = self.URL + '/hi/Specs/guide/xo'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def titleauthorization(self):
        url = self.URL + '/hi/TitleAuthorization/guide/xo'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getimage(self):
        url = self.URL + '/hi/images/file/{filePath}'
        params = ''
        resp = self._session.get(url, params=params)


    def getitem(self):
        url = self.URL + '/hi/Progression/file/{itemPath}'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getlobbyerrormessages(self):
        url = self.URL + '/hi/Multiplayer/file/gameStartErrorMessages/LobbyHoppperErrorMessageList.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getmetadata(self):
        url = self.URL + '/hi/Progression/file/metadata/metadata.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getnetworkconfiguration(self):
        url = self.URL + '/hi/Multiplayer/file/network/config.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getnews(self):
        url = self.URL + '/hi/news/file/{filePath}'
        params = ''
        resp = self._session.get(url, params=params)


    def getprogressionfile(self):
        url = self.URL + '/hi/Progression/file/{filePath}'
        params = ''
        resp = self._session.get(url, params=params)


    def getrecommendeddrivers(self):
        url = self.URL + '/hi/Specs/file/graphics/RecommendedDrivers.json'
        params = ''
        resp = self._session.get(url, params=params)


    def getseasonrewardtrack(self):
        url = self.URL + '/hi/Progression/file/{seasonPath}'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getseasonrewardtrackmanifest(self):
        url = self.URL + '/hi/Progression/file/RewardTracks/Manifest/seasonmanifest.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getstorefronts(self):
        url = self.URL + '/hi/Progression/file/Store/storefronts.json'
        params = '?flight={flightId}'
        resp = self._session.get(url, params=params)


    def getuiconfigurationjson(self):
        url = self.URL + '/branches/oly/UI-Settings/data/Settings.json'
        params = ''
        resp = self._session.get(url, params=params)


