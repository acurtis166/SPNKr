"""Services available for retrieving Halo Infinite data.

Access service instances via
[HaloInfiniteClient][spnkr.client.HaloInfiniteClient] properties.
"""

from .discovery_ugc import DiscoveryUgcService
from .economy import EconomyService
from .gamecms_hacs import GameCmsHacsService
from .profile import ProfileService
from .skill import SkillService
from .stats import StatsService

__all__ = [
    "DiscoveryUgcService",
    "EconomyService",
    "GameCmsHacsService",
    "ProfileService",
    "SkillService",
    "StatsService",
]
