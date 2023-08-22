"""Models for the "gamecms_hacs" authority."""

from pydantic import Field

from ..refdata import MedalDifficulty, MedalType
from .base import CamelCaseModel


class TranslatableString(CamelCaseModel):
    """A string value accompanied by a dictionary of translations."""

    value: str
    """The string value."""
    translations: dict[str, str]
    """A dictionary of language codes to translations for the string value."""


class Medal(CamelCaseModel):
    """Metadata for a single medal."""

    name_id: int
    """The medal's ID."""
    name: TranslatableString
    """The medal's name."""
    description: TranslatableString
    """The medal's description."""
    sprite_index: int
    """The index of the medal's sprite in the sprite sheet."""
    sorting_weight: int
    """The medal's sorting weight."""
    difficulty: MedalDifficulty = Field(alias="difficultyIndex")
    """The medal's difficulty, such as "normal" or "legendary"."""
    type: MedalType = Field(alias="typeIndex")
    """The medal's type, such as "mode" or "proficiency"."""
    personal_score: int
    """The amount of personal score awarded by obtaining the medal."""


class SpriteSheet(CamelCaseModel):
    """Information about a sprite sheet that contains medal sprites."""

    path: str
    """The path to the sprite sheet, relative to the "gamecms_hacs" host."""
    columns: int
    """The number of columns in the sprite sheet."""
    size: int
    """The size of each sprite in the sprite sheet."""


class SpriteSheets(CamelCaseModel):
    """Sizes of sprite sheets that contain medal sprites."""

    small: SpriteSheet
    """A sprite sheet with small sprites."""
    medium: SpriteSheet
    """A sprite sheet with medium sprites."""
    extra_large: SpriteSheet = Field(alias="extra-large")
    """A sprite sheet with extra large sprites."""


class MedalMetadata(CamelCaseModel):
    """Metadata for all medals."""

    difficulties: list[str]
    """The list of possible difficulties."""
    types: list[str]
    """The list of possible types."""
    sprites: SpriteSheets
    """Information about the medal sprite sheets that contain medal."""
    medals: list[Medal]
    """The list of available medals."""
