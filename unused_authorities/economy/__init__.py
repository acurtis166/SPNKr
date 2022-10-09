""""""

from halo_infinite_api import util
from halo_infinite_api.api.authorities import base
from halo_infinite_api.api.authorities.economy import models


class economyAuthority(base.BaseAuthority):

    URL = 'https://economy.svc.halowaypoint.com:443'

    def aicorecustomization(self):
        url = self.URL + '/hi/players/{player}/customization/ais/{coreId}'
        params = ''
        resp = self._session.get(url, params=params)


    def aicorescustomization(self):
        url = self.URL + '/hi/players/{player}/customization/ais'
        params = ''
        resp = self._session.get(url, params=params)


    def allownedcoresdetails(self):
        url = self.URL + '/hi/players/{player}/cores'
        params = ''
        resp = self._session.get(url, params=params)


    def armorcorecustomization(self):
        url = self.URL + '/hi/players/{player}/customization/armors/{coreId}'
        params = ''
        resp = self._session.get(url, params=params)


    def armorcorescustomization(self):
        url = self.URL + '/hi/players/{player}/customization/armors'
        params = ''
        resp = self._session.get(url, params=params)


    def getactiveboosts(self):
        url = self.URL + '/hi/players/{player}/boosts'
        params = ''
        resp = self._session.get(url, params=params)


    def getawardedrewards(self):
        url = self.URL + '/hi/players/{player}/rewards/{rewardId}'
        params = ''
        resp = self._session.get(url, params=params)


    def getboostsstore(self):
        url = self.URL + '/hi/players/{player}/stores/boosts'
        params = ''
        resp = self._session.get(url, params=params)


    def geteventsstore(self):
        url = self.URL + '/hi/players/{player}/stores/events'
        params = ''
        resp = self._session.get(url, params=params)


    def getgiveawayrewards(self):
        url = self.URL + '/hi/players/{player}/giveaways'
        params = ''
        resp = self._session.get(url, params=params)


    def gethcsstore(self):
        url = self.URL + '/hi/players/{player}/stores/hcs'
        params = ''
        resp = self._session.get(url, params=params)


    def getinventoryitems(self):
        url = self.URL + '/hi/players/{player}/inventory'
        params = ''
        resp = self._session.get(url, params=params)


    def getmainstore(self):
        url = self.URL + '/hi/players/{player}/stores/main'
        params = ''
        resp = self._session.get(url, params=params)


    def getmultipleplayerscustomization(self):
        url = self.URL + '/hi/customization'
        params = ''
        resp = self._session.get(url, params=params)


    def getoperationrewardlevelsstore(self):
        url = self.URL + '/hi/players/{player}/stores/operationrewardlevels'
        params = ''
        resp = self._session.get(url, params=params)


    def getoperationsstore(self):
        url = self.URL + '/hi/players/{player}/stores/operations'
        params = ''
        resp = self._session.get(url, params=params)


    def getrewardtrack(self):
        url = self.URL + '/hi/players/{player}/rewardtracks/{rewardTrackType}s/{trackId}'
        params = ''
        resp = self._session.get(url, params=params)


    def getvirtualcurrencybalances(self):
        url = self.URL + '/hi/players/{player}/currencies'
        params = ''
        resp = self._session.get(url, params=params)


    def getxpgrantsstore(self):
        url = self.URL + '/hi/players/{player}/stores/xpgrants'
        params = ''
        resp = self._session.get(url, params=params)


    def ownedcoredetails(self):
        url = self.URL + '/hi/players/{player}/cores/{coreId}'
        params = ''
        resp = self._session.get(url, params=params)


    def playerappearancecustomization(self):
        url = self.URL + '/hi/players/{player}/customization/appearance'
        params = ''
        resp = self._session.get(url, params=params)


    def playercustomization(self):
        url = self.URL + '/hi/players/{player}/customization'
        params = '?view={viewType}'
        resp = self._session.get(url, params=params)


    def playeroperations(self):
        url = self.URL + '/hi/players/{player}/rewardtracks/operations'
        params = ''
        resp = self._session.get(url, params=params)


    def postcurrencytransaction(self):
        url = self.URL + '/hi/players/{player}/currencies/{currencyId}/transactions'
        params = ''
        resp = self._session.get(url, params=params)


    def purchasestorefrontofferingtransaction(self):
        url = self.URL + '/hi/players/{player}/storetransactions'
        params = ''
        resp = self._session.get(url, params=params)


    def scheduledstorefrontofferings(self):
        url = self.URL + '/hi/players/{player}/stores/{storeId}'
        params = ''
        resp = self._session.get(url, params=params)


    def spartanbodycustomization(self):
        url = self.URL + '/hi/players/{player}/customization/spartanbody'
        params = ''
        resp = self._session.get(url, params=params)


    def vehiclecorecustomization(self):
        url = self.URL + '/hi/players/{player}/customization/vehicles/{coreId}'
        params = ''
        resp = self._session.get(url, params=params)


    def vehiclecorescustomization(self):
        url = self.URL + '/hi/players/{player}/customization/vehicles'
        params = ''
        resp = self._session.get(url, params=params)


    def weaponcorecustomization(self):
        url = self.URL + '/hi/players/{player}/customization/weapons/{coreId}'
        params = ''
        resp = self._session.get(url, params=params)


    def weaponcorescustomization(self):
        url = self.URL + '/hi/players/{player}/customization/weapons'
        params = ''
        resp = self._session.get(url, params=params)


