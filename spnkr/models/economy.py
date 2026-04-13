"""Models for the "economy" authority."""

import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

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


class OperationPassSummary(BaseModel, frozen=True):
    reward_track_path: str
    track_id: str
    name: str
    description: str | None = None
    is_active: bool = False
    is_owned: bool = False
    last_unlocked_rank: int = 0
    next_rank: int | None = None
    partial_progress: int = 0
    xp_per_rank: int | None = None
    total_ranks: int = 0
    has_reached_max_rank: bool = False
    battle_pass_image: str | None = None
    background_image_path: str | None = None

    @property
    def status(self) -> str:
        if self.is_completed:
            return "completed"
        if self.is_not_started:
            return "not_started"
        return "in_progress"

    @property
    def is_completed(self) -> bool:
        return self.has_reached_max_rank or (
            self.total_ranks > 0 and self.last_unlocked_rank >= self.total_ranks
        )

    @property
    def is_not_started(self) -> bool:
        return not self.is_completed and self.last_unlocked_rank == 0 and self.partial_progress == 0

    @property
    def is_in_progress(self) -> bool:
        return not self.is_completed and not self.is_not_started

    @property
    def progress_fraction(self) -> float | None:
        if self.is_completed:
            return 1.0
        if self.xp_per_rank is None or self.xp_per_rank <= 0:
            return None
        return min(1.0, max(0.0, self.partial_progress / self.xp_per_rank))

    @classmethod
    def from_models(
        cls,
        player_operation_pass: PlayerOperationPass,
        operation_reward_track,
        *,
        is_active: bool = False,
        language: str | None = None,
    ) -> "OperationPassSummary":
        available_ranks: tuple[int, ...] = ()
        name = player_operation_pass.track_id
        description = None
        xp_per_rank = None
        battle_pass_image = None
        background_image_path = None
        track_id = player_operation_pass.track_id

        if operation_reward_track is not None:
            available_ranks = tuple(
                sorted(rank.rank for rank in operation_reward_track.ranks)
            )
            name = _resolve_localized_value(operation_reward_track.name, language) or name
            description = _resolve_localized_value(
                operation_reward_track.description,
                language,
            )
            xp_per_rank = operation_reward_track.xp_per_rank
            battle_pass_image = operation_reward_track.battle_pass_image
            background_image_path = operation_reward_track.background_image_path
            track_id = operation_reward_track.track_id or track_id

        next_rank = next(
            (rank for rank in available_ranks if rank > player_operation_pass.last_unlocked_rank),
            None,
        )

        return cls(
            reward_track_path=player_operation_pass.reward_track_path,
            track_id=track_id,
            name=name,
            description=description,
            is_active=is_active,
            is_owned=player_operation_pass.is_owned
            or bool(player_operation_pass.current_progress.is_owned),
            last_unlocked_rank=player_operation_pass.last_unlocked_rank,
            next_rank=None if player_operation_pass.has_reached_max_rank else next_rank,
            partial_progress=player_operation_pass.partial_progress,
            xp_per_rank=xp_per_rank,
            total_ranks=available_ranks[-1] if available_ranks else 0,
            has_reached_max_rank=player_operation_pass.has_reached_max_rank,
            battle_pass_image=battle_pass_image,
            background_image_path=background_image_path,
        )


def _resolve_localized_value(value, language: str | None) -> str | None:
    if value is None:
        return None
    if language:
        translations = getattr(value, "translations", {}) or {}
        normalized = language.lower()
        for key, translated in translations.items():
            if not isinstance(translated, str):
                continue
            key_normalized = str(key).lower()
            if key_normalized == normalized or key_normalized.startswith(f"{normalized}-"):
                return translated
    resolved = getattr(value, "value", None)
    if isinstance(resolved, str) and resolved:
        return resolved
    return None
