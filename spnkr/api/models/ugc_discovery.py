"""Models for the HIUGC_Discovery authority."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AssetResponse:
    """Represents an asset in the UGC Discovery authority.

    Attributes:
        raw: The raw data returned by the API.
        id: The asset's ID.
        version_id: The asset's version ID.
        name: The asset's public name.
    """

    raw: dict
    id: UUID
    version_id: UUID
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> AssetResponse:
        """Create an Asset from a dictionary."""
        return cls(
            raw=data,
            id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            name=data["PublicName"],
        )
