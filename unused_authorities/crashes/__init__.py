""""""

from haloinfinite import util
from haloinfinite.api.authorities import base
from haloinfinite.api.authorities.crashes import models


class crashesAuthority(base.BaseAuthority):

    URL = 'https://crashes.svc.halowaypoint.com:443'

    def upload(self):
        url = self.URL + '/crashes/hipc/bf05b320-ee8f-4be5-879d-505b669654c9'
        resp = self._session.post(url, include_spartan_token=False)
        return resp.text

