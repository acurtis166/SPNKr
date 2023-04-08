"""Models for the profile authority."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProfileResponse:
    """Response returned when requesting profiles from the Xbox Live API.

    Attributes:
        raw (dict): The raw data returned from the Xbox Live API.
        gamertags (dict[str, str]): A dictionary of gamertags keyed by the
            players' XUIDs.
    """

    raw: dict
    gamertags: dict[str, str]

    @classmethod
    def from_dict(cls, data: dict) -> ProfileResponse:
        """Create a new instance from a dictionary."""
        raw = data
        gamertags = {}
        for user in data["profileUsers"]:
            for setting in user["settings"]:
                if setting["id"] == "Gamertag":
                    gamertags[user["id"]] = setting["value"]
                    break
        return cls(raw, gamertags)
