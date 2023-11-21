"""Parse responses into pydantic models."""

from .gamecms_hacs import MedalMetadata
from .profile import User
from .skill import MatchSkill, PlaylistCsr
from .stats import MatchCount, MatchHistory, MatchStats
from .ugc_discovery import Map, MapModePair, Playlist, UgcGameVariant

__all__ = [
    "Map",
    "MapModePair",
    "MatchCount",
    "MatchHistory",
    "MatchSkill",
    "MatchStats",
    "MedalMetadata",
    "Playlist",
    "PlaylistCsr",
    "UgcGameVariant",
    "User",
]
