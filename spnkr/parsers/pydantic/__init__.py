"""Parse responses into pydantic models."""

from .gamecms_hacs import MedalMetadata
from .skill import MatchSkill, PlaylistCsr
from .stats import MatchCount, MatchHistory, MatchStats
from .ugc_discovery import Map, MapModePair, Playlist, UgcGameVariant
