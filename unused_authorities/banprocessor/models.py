"""Models for the banprocessor authority."""

from typing import Any, Dict, List

from spnkr.api.models import OnlineUriReference, ResultContainer
from spnkr.models import PascalModel


class BanResult(PascalModel):
    bans_in_effect: List[Any]  # uncertain


class TargetBanSummary(ResultContainer):
    result: BanResult


class BanSummaryQueryResult(PascalModel):
    results: List[TargetBanSummary]
    links: Dict[str, OnlineUriReference]

    