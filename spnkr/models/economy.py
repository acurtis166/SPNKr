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


class _ExtraPascalCaseModel(PascalCaseModel, frozen=True):
    model_config = ConfigDict(
        alias_generator=PascalCaseModel.model_config["alias_generator"],
        populate_by_name=True,
        extra="allow",
    )


class RewardTrackProgress(_ExtraPascalCaseModel, frozen=True):
    rank: int = 0
    partial_progress: int = 0
    has_reached_max_rank: bool = False
    is_owned: bool | None = None


class PlayerOperationPass(_ExtraPascalCaseModel, frozen=True):
    reward_track_path: str
    current_progress: RewardTrackProgress = Field(default_factory=RewardTrackProgress)
    is_owned: bool = False

    @property
    def track_id(self) -> str:
        return self.reward_track_path.rsplit("/", 1)[-1].removesuffix(".json")

    @property
    def last_unlocked_rank(self) -> int:
        return self.current_progress.rank

    @property
    def partial_progress(self) -> int:
        return self.current_progress.partial_progress

    @property
    def has_reached_max_rank(self) -> bool:
        return self.current_progress.has_reached_max_rank

    @property
    def is_completed(self) -> bool:
        return self.has_reached_max_rank

    @property
    def is_not_started(self) -> bool:
        return not self.is_completed and self.last_unlocked_rank == 0 and self.partial_progress == 0

    @property
    def is_in_progress(self) -> bool:
        return not self.is_completed and not self.is_not_started


class PlayerOperationPasses(_ExtraPascalCaseModel, frozen=True):
    active_operation_reward_track_path: str | None = None
    operation_reward_tracks: tuple[PlayerOperationPass, ...] = ()

    @property
    def active(self) -> PlayerOperationPass | None:
        if self.active_operation_reward_track_path is None:
            return None
        return next(
            (
                operation
                for operation in self.operation_reward_tracks
                if operation.reward_track_path == self.active_operation_reward_track_path
            ),
            None,
        )

    @property
    def completed(self) -> tuple[PlayerOperationPass, ...]:
        return tuple(operation for operation in self.operation_reward_tracks if operation.is_completed)

    @property
    def not_started(self) -> tuple[PlayerOperationPass, ...]:
        return tuple(operation for operation in self.operation_reward_tracks if operation.is_not_started)

    @property
    def in_progress(self) -> tuple[PlayerOperationPass, ...]:
        return tuple(operation for operation in self.operation_reward_tracks if operation.is_in_progress)


class PlayerCareerRank(_ExtraPascalCaseModel, frozen=True):
    current_progress: RewardTrackProgress = Field(default_factory=RewardTrackProgress)
    spartan_id: str | None = None

