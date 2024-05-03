"""Models for the "gamecms_hacs" authority."""

import datetime as dt

from pydantic import Field

from spnkr.models.base import CamelCaseModel, PascalCaseModel
from spnkr.models.refdata import MedalDifficulty, MedalType
from spnkr.models.types import ReadOnlyDict


class TranslatableString(CamelCaseModel, frozen=True):
    """A string value accompanied by a dictionary of translations.

    Attributes:
        value: The string value.
        translations: A dictionary of language codes to translations for the string value.
    """

    value: str
    translations: ReadOnlyDict[str, str]


class Medal(CamelCaseModel, frozen=True):
    """Metadata for a single medal.

    Attributes:
        name_id: The medal's ID.
        name: The medal's name.
        description: The medal's description.
        sprite_index: The index of the medal's sprite in the sprite sheet.
        sorting_weight: The medal's sorting weight.
        difficulty: The medal's difficulty, such as "normal" or "legendary".
        type: The medal's type, such as "mode" or "proficiency".
        personal_score: The amount of personal score awarded by obtaining the medal.
    """

    name_id: int
    name: TranslatableString
    description: TranslatableString
    sprite_index: int
    sorting_weight: int
    difficulty: MedalDifficulty = Field(alias="difficultyIndex")
    type: MedalType = Field(alias="typeIndex")
    personal_score: int


class SpriteSheet(CamelCaseModel, frozen=True):
    """Information about a sprite sheet that contains medal sprites.

    Attributes:
        path: The path to the sprite sheet, relative to the "gamecms_hacs" host.
        columns: The number of columns in the sprite sheet.
        size: The size of each sprite in the sprite sheet.
    """

    path: str
    columns: int
    size: int


class SpriteSheets(CamelCaseModel, frozen=True):
    """Sizes of sprite sheets that contain medal sprites.

    Attributes:
        small: A sprite sheet with small sprites.
        medium: A sprite sheet with medium sprites.
        extra_large: A sprite sheet with extra large sprites.
    """

    small: SpriteSheet
    medium: SpriteSheet
    extra_large: SpriteSheet = Field(alias="extra-large")


class MedalMetadata(CamelCaseModel, frozen=True):
    """Metadata for all medals.

    Attributes:
        difficulties: The list of possible difficulties.
        types: The list of possible types.
        sprites: Information about the medal sprite sheets that contain medal.
        medals: The list of available medals.
    """

    difficulties: tuple[str, ...]
    types: tuple[str, ...]
    sprites: SpriteSheets
    medals: tuple[Medal, ...]


class Date(PascalCaseModel, frozen=True):
    """A date object.

    Attributes:
        value: The date value.
    """

    value: dt.datetime = Field(alias="ISO8601Date")


class CsrSeason(PascalCaseModel, frozen=True):
    """A CSR season.

    Attributes:
        csr_season_file_path: The relative path to the CSR season file. The stem
            of the path is the CSR season's ID, e.g., "CsrSeason5-1".
        start_date: The UTC start date of the season.
        end_date: The UTC end date of the season.
    """

    csr_season_file_path: str
    start_date: Date
    end_date: Date


class CsrSeasonCalendar(PascalCaseModel, frozen=True):
    """A collection of past and current CSR seasons.

    Attributes:
        seasons: The list of CSR seasons.
    """

    seasons: tuple[CsrSeason, ...]


class Season(PascalCaseModel, frozen=True):
    """An promotional, reward-track operation contained within a CSR season.

    Attributes:
        csr_season_file_path: The relative path to the CSR season file. The stem
            of the path is the CSR season's ID, e.g., "CsrSeason5-1".
        operation_track_path: The relative path to the operation's reward track
            file.
        season_metadata: The relative path to the operation metadata file.
        start_date: The UTC start date of the season.
        end_date: The UTC end date of the season.
    """

    csr_season_file_path: str
    operation_track_path: str
    season_metadata: str
    start_date: Date
    end_date: Date


class Event(PascalCaseModel, frozen=True):
    """A promotional, reward-track event contained within a CSR season.

    Events were superseded by operations as of October 2023.

    Attributes:
        reward_track_path: The relative path to the event's reward track file.
        start_date: The UTC start date of the event.
        end_date: The UTC end date of the event.
    """

    reward_track_path: str
    start_date: Date
    end_date: Date


class CareerRank(PascalCaseModel, frozen=True):
    """Information related to career rank progression.

    Attributes:
        reward_track_path: The relative path to the career rank reward track
            file.
    """

    reward_track_path: str


class SeasonCalendar(PascalCaseModel, frozen=True):
    """A collection of past and current reward tracks.

    Attributes:
        seasons: The list of "operation" reward tracks.
        events: The list of "event" reward tracks. Events were superseded by
            operations as of October 2023.
        career_rank: Information about career rank progression.
    """

    seasons: tuple[Season, ...]
    events: tuple[Event, ...]
    career_rank: CareerRank


class InventoryReward(PascalCaseModel, frozen=True):
    """An inventory item reward, such as a weapon skin or armor piece.

    Attributes:
        inventory_item_path: The relative path to the inventory item file.
        amount: The quantity of the inventory item awarded.
        type: The type of inventory item, such as "ArmorCoating".
    """

    inventory_item_path: str
    amount: int
    type: str


class CurrencyReward(PascalCaseModel, frozen=True):
    """A currency reward, such as an XP boost.

    Attributes:
        currency_path: The relative path to the currency file.
        amount: The quantity of the currency awarded.
    """

    currency_path: str
    amount: int


class RankRewards(PascalCaseModel, frozen=True):
    """A collection of inventory and currency rewards earned at a rank.

    Attributes:
        inventory_rewards: The list of inventory item rewards.
        currency_rewards: The list of currency rewards.
    """

    inventory_rewards: tuple[InventoryReward, ...]
    currency_rewards: tuple[CurrencyReward, ...]


class TranslatableStringWithStatus(CamelCaseModel, frozen=True):
    """A string value accompanied by a dictionary of translations.

    Attributes:
        status: The status of the attribute.
        value: The string value.
        translations: A dictionary of language codes to translations for the
            string value.
    """

    status: str
    value: str
    translations: ReadOnlyDict[str, str]


class CareerRewardTrackRank(PascalCaseModel, frozen=True):
    """A rank in the career rank progression reward track.

    Title, subtitle, and grade can be combined for the rank's full name, e.g.,
    "Sergeant Bronze 2".

    Attributes:
        rank: The rank number.
        free_rewards: The rewards earned by all players that reach the rank.
        paid_rewards: The rewards earned by players that purchase the battle
            pass and reach the rank.
        xp_required_for_rank: The amount of XP required to reach the rank.
        rank_title: The rank's title, such as "Private" or "General".
        rank_sub_title: The rank's subtitle, such as "Bronze" or "Onyx".
        rank_tier: The rank's integer tier/grade - the smallest unit of rank
            progression.
        rank_icon: The relative path to the rank's icon file. Has a height of
            280px.
        rank_large_icon: The relative path to the rank's large icon file. This
            is the icon presented after a player acheives the rank. Has a height
            of 600px.
        rank_adornment_icon: The relative path to the rank's adornment icon
            file. Has a height of 196px.
        tier_type: The rank's tier type, such as "Bronze" or "Onyx".
        rank_grade: The rank's integer grade. Max is 3.
    """

    rank: int
    free_rewards: RankRewards
    paid_rewards: RankRewards
    xp_required_for_rank: int
    rank_title: TranslatableStringWithStatus
    rank_sub_title: TranslatableStringWithStatus
    rank_tier: TranslatableStringWithStatus
    rank_icon: str
    rank_large_icon: str
    rank_adornment_icon: str
    tier_type: str
    rank_grade: int


class CareerRewardTrack(PascalCaseModel, frozen=True):
    """The career rank progression reward track.

    Attributes:
        track_id: The reward track's ID.
        ranks: The list of ranks in the reward track.
        name: The reward track's name.
        description: The reward track's description.
        operation_number: The reward track's operation number.
        date_range: The reward track's date range.
        is_ritual: ...
        summary_image_path: The relative path to the reward track's summary
            image file.
        xp_per_rank: The amount of XP awarded per rank.
    """

    track_id: str
    ranks: tuple[CareerRewardTrackRank, ...]
    name: TranslatableStringWithStatus
    description: TranslatableStringWithStatus
    operation_number: int
    date_range: TranslatableStringWithStatus
    is_ritual: bool
    summary_image_path: str
    week_number: None
    xp_per_rank: int
