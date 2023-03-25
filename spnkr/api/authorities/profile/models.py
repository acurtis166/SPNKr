""""""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Setting:
    id: str
    value: str

    @classmethod
    def from_dict(cls, data: dict) -> Setting:
        return Setting(data["id"], data["value"])


@dataclass(frozen=True)
class ProfileUser:
    id: str
    host_id: str
    settings: list[Setting]
    is_sponsored_user: bool

    @classmethod
    def from_dict(cls, data: dict) -> ProfileUser:
        settings = [Setting.from_dict(s) for s in data["settings"]]
        return ProfileUser(
            data["id"], data["hostId"], settings, data["isSponsoredUser"]
        )


@dataclass(frozen=True)
class ProfileResponse:
    profile_users: list[ProfileUser]

    @classmethod
    def from_dict(cls, data: dict) -> ProfileResponse:
        profile_users = [ProfileUser.from_dict(u) for u in data["profileUsers"]]
        return ProfileResponse(profile_users)
