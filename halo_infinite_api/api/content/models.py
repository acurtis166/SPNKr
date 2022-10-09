"""Models for the HIUGC_Discovery authority."""

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from halo_infinite_api.models import PascalModel, Date


@dataclass
class OnlineUriReference(PascalModel):
    authority_id: str
    path: str
    query_string: str | None
    retry_policy_id: str
    topic_name: str
    acknowledgement_type_id: int
    authentication_lifetime_extension_supported: bool
    clearance_aware: bool


@dataclass
class AssetFiles(PascalModel):
    prefix: str
    file_relative_paths: list[str]
    prefix_endpoint: OnlineUriReference


@dataclass
class AssetStats(PascalModel):
    plays_recent: int
    plays_all_time: int
    favorites: int
    likes: int
    bookmarks: int
    parent_asset_count: int
    average_rating: float | None
    number_of_ratings: int


@dataclass
class Asset(PascalModel):
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


@dataclass
class ManifestCustomData(PascalModel):
    branch_name: str | None = None
    build_number: str | None = None
    kind: int | None = None
    content_version: str | None = None
    build_guid: UUID | None = None
    visibility: int | None = None


@dataclass
class Manifest(Asset):
    custom_data: ManifestCustomData
    tags: list[str]
    map_links: list[Asset]
    playlist_links: list[Asset]
    ugc_game_variant_links: list[Asset]
    prefab_links: list[Asset] | None = None
    map_mode_pair_links: list[Asset] | None = None
    engine_game_variant_links: list[Asset] | None = None


@dataclass
class Project(Asset):
    custom_data: dict[Any, Any]
    tags: list[str]
    map_links: list[Asset]
    playlist_links: list[Asset]
    prefab_links: list[Asset] | None
    ugc_game_variant_links: list[Asset]
    map_mode_pair_links: list[Asset] | None
    engine_game_variant_links: list[Asset] | None = None


@dataclass
class EngineGameVariantSubsetData(PascalModel):
    stat_bucket_game_type: int
    engine_name: str
    variant_name: str


@dataclass
class EngineGameVariantCustomData(PascalModel):
    subset_data: EngineGameVariantSubsetData
    localized_data: dict[Any, Any]


@dataclass
class EngineGameVariant(Asset):
    custom_data: EngineGameVariantCustomData
    tags: list[str]


@dataclass
class MapCustomData(PascalModel):
    num_of_objects_on_map: int
    tag_level_id: int
    is_baked: bool
    has_node_graph: bool


@dataclass
class Map(Asset):
    custom_data: MapCustomData
    tags: list[str]
    prefab_links: list[Asset] | None


@dataclass
class RotationWeight(PascalModel):
    weight: float


@dataclass
class RotationEntry(Asset):
    metadata: RotationWeight


@dataclass
class PlaylistEntry(PascalModel):
    map_mode_pair_asset_id: str
    metadata: RotationWeight


@dataclass
class PlaylistCustomData(PascalModel):
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


@dataclass
class Playlist(Asset):
    custom_data: PlaylistCustomData
    tags: list[str]
    rotation_entries: list[RotationEntry]


@dataclass
class MapModePair(Asset):
    custom_data: dict[Any, Any]
    tags: list[str]
    map_link: Asset
    ugc_game_variant_link: Asset


@dataclass
class PrefabCustomData(PascalModel):
    parts: int
    has_node_graph: bool


@dataclass
class Prefab(Asset):
    custom_data: PrefabCustomData
    tags: list[str]


@dataclass
class Tag(PascalModel):
    name: str


@dataclass
class TagsInfo(PascalModel):
    canned_tags: list[Tag]


@dataclass
class UgcGameVariantCustomData(PascalModel):
    key_values: dict[Any, Any]


@dataclass
class UgcGameVariant(Asset):
    custom_data: UgcGameVariantCustomData
    tags: list[str]
    engine_game_variant_link: Asset


@dataclass
class TagCount(PascalModel):
    tag: str
    count: int


@dataclass
class SearchResult(PascalModel):
    asset_id: str
    asset_version_id: str
    name: str
    description: str
    asset_kind: int
    tags: list[str]
    thumbnail_url: str
    referenced_assets: list[Any]  # uncertain
    original_author: str
    likes: int
    bookmarks: int
    plays_recent: int
    number_of_objects: int
    date_created_utc: Date
    date_modified_utc: Date
    date_published_utc: Date
    has_node_graph: bool
    read_only_clones: bool
    plays_all_time: int
    contributors: list[str]
    parent_asset_count: int
    average_rating: float
    number_of_ratings: int


@dataclass
class Search(PascalModel):
    tags: list[TagCount]
    estimated_total: int
    start: int
    count: int
    result_count: int
    results: list[SearchResult]
    links: dict[Any, Any]  # uncertain


@dataclass
class FilmChunk(PascalModel):
    index: int
    chunk_start_time_offset_milliseconds: int
    duration_milliseconds: int
    chunk_size: int
    file_relative_path: str
    chunk_type: int


@dataclass
class FilmCustomData(PascalModel):
    film_length: int
    chunks: list[FilmChunk]
    has_game_ended: bool
    manifest_refresh_seconds: int
    match_id: str
    film_major_version: int


@dataclass
class Film(PascalModel):
    film_status_bond: int
    custom_data: FilmCustomData
    blob_storage_path_prefix: str
    asset_id: UUID

