"""Services available for retrieving Halo Infinite data.

Access service instances via
[HaloInfiniteClient][spnkr.client.HaloInfiniteClient] properties.
"""

from .discovery_ugc import DiscoveryUgcService
from .gamecms_hacs import GameCmsHacsService
from .profile import ProfileService
from .skill import SkillService
from .stats import StatsService

__all__ = [
    "DiscoveryUgcService",
    "GameCmsHacsService",
    "ProfileService",
    "SkillService",
    "StatsService",
]
