
from haloinfinite.api.session import Session


class BaseAuthority:
    def __init__(self, session: Session):
        self._session = session

