""""""

from dataclasses import dataclass

from halo_infinite_api.models import CamelModel


@dataclass
class Setting(CamelModel):
    id: str
    value: str


@dataclass
class ProfileUser(CamelModel):
    id: str
    host_id: str
    settings: list[Setting]
    is_sponsored_user: bool


@dataclass
class ProfileResponse(CamelModel):
    profile_users: list[ProfileUser]

    