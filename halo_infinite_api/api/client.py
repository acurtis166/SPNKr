
from halo_infinite_api.api.session import Session
from halo_infinite_api.api.authorities import profile, skill, stats, ugc_discovery
from halo_infinite_api.authentication.manager import AuthenticationManager


class Client:
    def __init__(self, auth_mgr: AuthenticationManager, validate_tokens: bool = True):
        session = Session(auth_mgr, validate_tokens)

        self.profile = profile.ProfileAuthority(session)
        self.skill = skill.SkillAuthority(session)
        self.stats = stats.StatsAuthority(session)
        self.ugc_discovery = ugc_discovery.UgcDiscoveryAuthority(session)

        