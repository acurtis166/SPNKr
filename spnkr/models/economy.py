"""Models for the "economy" authority."""

import datetime as dt

from pydantic import ConfigDict, Field

from spnkr.models.base import PascalCaseModel


class Date(PascalCaseModel, frozen=True):
    """A date object.

    Attributes:
        value: The date value.
    """

    value: dt.datetime = Field(alias="ISO8601Date")


class ThemeEmblem(PascalCaseModel, frozen=True):
    path: str
    location_id: int
    configuration_id: int


class ArmorCoreTheme(PascalCaseModel, frozen=True):
    first_modified_date_utc: Date
    last_modified_date_utc: Date
    is_equipped: bool
    is_default: bool
    theme_path: str
    coating_path: str
    glove_path: str
    helmet_path: str
    helmet_attachment_path: str
    chest_attachment_path: str
    knee_pad_path: str
    left_shoulder_pad_path: str
    right_shoulder_pad_path: str
    emblems: tuple[ThemeEmblem, ...]
    armor_fx_path: str
    mythic_fx_path: str
    visor_path: str
    hip_attachment_path: str
    wrist_attachment_path: str
    armor_fx_paths: tuple[str, ...] | None


class ArmorCore(PascalCaseModel, frozen=True):
    core_path: str
    is_equipped: bool
    themes: tuple[ArmorCoreTheme, ...]
    core_id: str
    core_type: str


class ArmorCores(PascalCaseModel, frozen=True):
    armor_cores: tuple[ArmorCore, ...]


class SpartanBody(PascalCaseModel, frozen=True):
    last_modified_date_utc: Date
    left_arm: str
    right_arm: str
    left_leg: str
    right_leg: str
    body_type: str
    voice_path: str


class AppearanceEmblem(PascalCaseModel, frozen=True):
    emblem_path: str
    configuration_id: int


class Appearance(PascalCaseModel, frozen=True):
    last_modified_date_utc: Date
    action_pose_path: str
    backdrop_image_path: str
    emblem: AppearanceEmblem
    service_tag: str
    intro_emote_path: str | None
    player_title_path: str | None


class WeaponCoreTheme(PascalCaseModel, frozen=True):
    first_modified_date_utc: Date
    last_modified_date_utc: Date
    is_equipped: bool
    is_default: bool
    theme_path: str
    coating_path: str
    emblems: tuple[ThemeEmblem, ...]
    death_fx_path: str
    ammo_counter_color_path: str
    stat_tracker_path: str
    weapon_charm_path: str
    alternate_geometry_region_path: str


class WeaponCore(PascalCaseModel, frozen=True):
    core_path: str
    themes: tuple[WeaponCoreTheme, ...]
    core_id: str
    core_type: str


class WeaponCores(PascalCaseModel, frozen=True):
    weapon_cores: tuple[WeaponCore, ...]


class AiCoreTheme(PascalCaseModel, frozen=True):
    first_modified_date_utc: Date
    last_modified_date_utc: Date
    is_equipped: bool
    is_default: bool
    theme_path: str
    model_path: str
    color_path: str

    model_config = ConfigDict(protected_namespaces=())


class AiCore(PascalCaseModel, frozen=True):
    core_path: str
    is_equipped: bool
    themes: tuple[AiCoreTheme, ...]
    core_id: str
    core_type: str


class AiCores(PascalCaseModel, frozen=True):
    ai_cores: tuple[AiCore, ...]


class VehicleCoreTheme(PascalCaseModel, frozen=True):
    first_modified_date_utc: Date
    last_modified_date_utc: Date
    is_equipped: bool
    is_default: bool
    theme_path: str
    coating_path: str
    horn_path: str
    vehicle_fx_path: str
    vehicle_charm_path: str
    emblems: tuple[ThemeEmblem, ...]
    alternate_geometry_region_path: str


class VehicleCore(PascalCaseModel, frozen=True):
    core_id: str
    core_path: str
    themes: tuple[VehicleCoreTheme, ...]
    core_type: str


class VehicleCores(PascalCaseModel, frozen=True):
    vehicle_cores: tuple[VehicleCore, ...]


class PlayerCustomization(PascalCaseModel, frozen=True):
    armor_cores: ArmorCores
    spartan_body: SpartanBody
    appearance: Appearance
    weapon_cores: WeaponCores
    ai_cores: AiCores
    vehicle_cores: VehicleCores
