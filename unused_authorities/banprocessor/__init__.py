""""""

from typing import List
from spnkr import util
from spnkr.api.authorities import base
from spnkr.api.authorities.banprocessor import models


class BanProcessorAuthority(base.BaseAuthority):

    URL = 'https://banprocessor.svc.halowaypoint.com:443'

    def ban_summary(self,
                   player_xuids: List[str] | None = None,
                   devices: List[str] | None = None) -> models.BanSummaryQueryResult:
        wrapped_xuids = [util.wrap_xuid(x) for x in player_xuids or []]
        wrapped_devices = [f'Authenticated({d})' for d in devices or []]
        url = self.URL + '/hi/bansummary'
        params = {
            'auth': 'st',
            'targets': wrapped_xuids + wrapped_devices
        }
        resp = self._session.get(url, params=params)
        return models.BanSummaryQueryResult.parse_raw(resp.text)

