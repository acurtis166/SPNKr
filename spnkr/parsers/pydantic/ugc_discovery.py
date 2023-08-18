"""Models for the HIUGC_Discovery authority."""

from typing import Any
from uuid import UUID

from .base import PascalCaseModel


class OnlineUriReference(PascalCaseModel):
    authority_id: str
    path: str
    query_string: str | None
    retry_policy_id: str
    topic_name: str
    acknowledgement_type_id: int
    authentication_lifetime_extension_supported: bool
    clearance_aware: bool


class AssetFiles(PascalCaseModel):
    prefix: str
    file_relative_paths: list[str]
    prefix_endpoint: OnlineUriReference


class AssetStats(PascalCaseModel):
    plays_recent: int
    plays_all_time: int
    favorites: int
    likes: int
    bookmarks: int
    parent_asset_count: int
    average_rating: float | None
    number_of_ratings: int


class Asset(PascalCaseModel):
    asset_id: UUID
    version_id: UUID
    public_name: str
    description: str
    files: AssetFiles
    contributors: list[str]
    asset_home: int
    asset_stats: AssetStats
    inspection_result: int
    clone_behavior: int
    order: int


class MapCustomData(PascalCaseModel):
    num_of_objects_on_map: int
    tag_level_id: int
    is_baked: bool
    has_node_graph: bool


class Map(Asset):
    custom_data: MapCustomData
    tags: list[str]
    prefab_links: list[Asset] | None


class RotationWeight(PascalCaseModel):
    weight: float


class RotationEntry(Asset):
    metadata: RotationWeight


class PlaylistEntry(PascalCaseModel):
    map_mode_pair_asset_id: str
    metadata: RotationWeight


class PlaylistCustomData(PascalCaseModel):
    playlist_entries: list[PlaylistEntry]
    strategy: int
    min_teams: int
    min_team_size: int
    max_teams: int
    max_team_size: int
    max_team_imbalance: int
    max_splitscreen_players_allowed: int
    allow_friend_join_in_progress: bool
    allow_matchmaking_join_in_progress: bool
    allow_bot_join_in_progress: bool
    exit_experience_duration_sec: int
    fireteam_leader_kick_allowed: bool
    disable_midgame_chat: bool
    allowed_device_inputs: list[int]
    bot_difficulty: int
    min_fireteam_size: int
    max_fireteam_size: int


class Playlist(Asset):
    custom_data: PlaylistCustomData
    tags: list[str]
    rotation_entries: list[RotationEntry]


class MapModePair(Asset):
    custom_data: dict[Any, Any]
    tags: list[str]
    map_link: Asset
    ugc_game_variant_link: Asset


class UgcGameVariantCustomData(PascalCaseModel):
    key_values: dict[Any, Any]


class UgcGameVariant(Asset):
    custom_data: UgcGameVariantCustomData
    tags: list[str]
    engine_game_variant_link: Asset
