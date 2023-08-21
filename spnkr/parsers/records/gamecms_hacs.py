"""Parsing functions for the "gamecms_hacs" authority."""

from typing import Any, NamedTuple

from ..refdata import MedalDifficulty, MedalType


class MedalRecord(NamedTuple):
    """Details about a medal.

    Attributes:
        name_id: The medal's ID.
        name: The medal's name.
        description: The medal's description.
        sprite_index: The index of the sprite in the sprite sheet.
        sorting_weight: The medal's sorting weight for the post-game carnage
            report.
        difficulty: The medal's difficulty.
        type: The medal's type.
        personal_score: The personal score awarded for earning the medal.
    """

    name_id: int
    name: str
    description: str
    sprite_index: int
    sorting_weight: int
    difficulty: MedalDifficulty
    type: MedalType
    personal_score: int


def parse_medal_metadata(data: dict[str, Any]) -> list[MedalRecord]:
    """Parse `get_medal_metadata` response JSON from the client.

    Args:
        data: The deserialized JSON from the client's `get_medal_metadata`
            method.

    Returns:
        A list of medal detail records.
    """
    return [_parse_medal(medal_data) for medal_data in data["medals"]]


def _parse_medal(medal_data: dict[str, Any]) -> MedalRecord:
    """Parse a single medal from the `get_medal_metadata` response JSON."""
    return MedalRecord(
        name_id=medal_data["nameId"],
        name=medal_data["name"]["value"],
        description=medal_data["description"]["value"],
        sprite_index=medal_data["spriteIndex"],
        sorting_weight=medal_data["sortingWeight"],
        difficulty=MedalDifficulty(medal_data["difficultyIndex"]),
        type=MedalType(medal_data["typeIndex"]),
        personal_score=medal_data["personalScore"],
    )
