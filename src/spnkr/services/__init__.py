"""Services available for retrieving Halo Infinite data.

Access service instances via
[HaloInfiniteClient][spnkr.client.HaloInfiniteClient] properties.
"""

from spnkr.services.discovery_ugc import DiscoveryUgcService
from spnkr.services.economy import EconomyService
from spnkr.services.gamecms_hacs import GameCmsHacsService
from spnkr.services.profile import ProfileService
from spnkr.services.skill import SkillService
from spnkr.services.stats import StatsService

__all__ = [
    "DiscoveryUgcService",
    "EconomyService",
    "GameCmsHacsService",
    "ProfileService",
    "SkillService",
    "StatsService",
]
