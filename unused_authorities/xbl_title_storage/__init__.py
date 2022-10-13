""""""

from spnkr import util
from spnkr.api.authorities import base
from spnkr.api.authorities.xbl_title_storage import models


class xbl_title_storageAuthority(base.BaseAuthority):

    URL = 'https://titlestorage.xboxlive.com:443'
    AUTHENTICATION_METHODS = ['XSTSv3XboxAudience']
    SCHEME = 'Https'

    def titlemanagedstorage(self):
        url = self.URL + '/trustedplatform/users/xuid({xuid})/scids/{scid}/data/thunderhead_campaign_saves'
        params = ''
        resp = self._session.get(url, params=params)


    def titlemanagedstoragefile(self):
        url = self.URL + '/trustedplatform/users/xuid({xuid})/scids/{scid}/data/thunderhead_campaign_saves/{filename},{type}'
        params = ''
        resp = self._session.get(url, params=params)


