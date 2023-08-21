"""Models for the gamecms_hacs authority."""

from pydantic import Field

from ..refdata import MedalDifficulty, MedalType
from .base import CamelCaseModel


class TranslatableString(CamelCaseModel):
    value: str
    translations: dict[str, str]


class Medal(CamelCaseModel):
    name_id: int
    name: TranslatableString
    description: TranslatableString
    sprite_index: int
    sorting_weight: int
    difficulty: MedalDifficulty = Field(alias="difficultyIndex")
    type: MedalType = Field(alias="typeIndex")
    personal_score: int


class SpriteSheet(CamelCaseModel):
    path: str
    columns: int
    size: int


class SpriteSheets(CamelCaseModel):
    small: SpriteSheet
    medium: SpriteSheet
    extra_large: SpriteSheet = Field(alias="extra-large")


class MedalMetadata(CamelCaseModel):
    difficulties: list[str]
    types: list[str]
    sprites: SpriteSheets
    medals: list[Medal]
