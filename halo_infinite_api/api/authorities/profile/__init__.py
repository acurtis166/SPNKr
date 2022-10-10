""""""

from halo_infinite_api.api.authorities.base import BaseAuthority
from halo_infinite_api.api.authorities.profile import models
from halo_infinite_api.api.enums import AuthenticationMethod, ProfileSetting
from halo_infinite_api.exceptions import ApiRateLimitException
from halo_infinite_api import util


class ProfileAuthority(BaseAuthority):
    URL = 'https://profile.xboxlive.com:443'
    AUTH_METHOD = AuthenticationMethod.XSTSv3XboxAudience

    def get_profiles(self,
                     xuids: list[str],
                     settings: list[ProfileSetting] | None = None) -> models.ProfileResponse:
        url = self.URL + '/users/batch/profile/settings'
        settings = settings or list(ProfileSetting)
        data = {
            'settings': [ps.value for ps in settings],
            'userIds': [util.unwrap_xuid(x) for x in xuids],
        }
        resp = self._session.post(url, json=data, auth_method=self.AUTH_METHOD)
        if resp.status_code == 429:
            raise ApiRateLimitException('Request rate exceeded')
        resp.raise_for_status()
        return models.ProfileResponse.parse_json(resp.text)

    def get_profile_by_xuid(self,
                            xuid: str,
                            settings: list[ProfileSetting] | None = None
                            ) -> models.ProfileResponse:
        url = self.URL + f'/users/{util.wrap_xuid(xuid)}/profile/settings'
        settings = settings or list(ProfileSetting)
        params = {
            'settings': ','.join([ps.value for ps in settings]),
        }
        resp = self._session.get(url, params=params, auth_method=self.AUTH_METHOD)
        if resp.status_code == 429:
            raise ApiRateLimitException('Request rate exceeded')
        resp.raise_for_status()
        return models.ProfileResponse.parse_json(resp.text)

    def get_profile_by_gamertag(self,
                                gamertag: str,
                                settings: list[ProfileSetting] | None = None
                                ) -> models.ProfileResponse:
        url = self.URL + f'/users/gt({gamertag})/profile/settings'
        settings = settings or list(ProfileSetting)
        params = {
            'settings': ','.join([ps.value for ps in settings]),
        }
        resp = self._session.get(url, params=params, auth_method=self.AUTH_METHOD)
        if resp.status_code == 429:
            raise ApiRateLimitException('Request rate exceeded')
        resp.raise_for_status()
        return models.ProfileResponse.parse_json(resp.text)

