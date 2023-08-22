"""Models for the HIUGC_Discovery authority."""

from typing import Any
from uuid import UUID

from .base import PascalCaseModel


class OnlineUriReference(PascalCaseModel):
    """A reference to an online resource."""

    authority_id: str
    """The ID of the authority that hosts the resource."""
    path: str
    """The path to the resource, relative to the authority's host."""
    query_string: str | None
    """The query string of the resource's URL."""
    retry_policy_id: str
    """The ID of the retry policy to use when accessing the resource."""
    topic_name: str
    """The name of the topic to use when accessing the resource."""
    acknowledgement_type_id: int
    """The ID of the acknowledgement type to use when accessing the resource."""
    authentication_lifetime_extension_supported: bool
    """Whether the resource supports extending the lifetime of an authentication token."""
    clearance_aware: bool
    """Whether the resource is clearance aware."""


class AssetFiles(PascalCaseModel):
    """Information about the files that make up an asset."""

    prefix: str
    """The root path to the asset's files."""
    file_relative_paths: list[str]
    """The relative paths to the asset's files."""
    prefix_endpoint: OnlineUriReference
    """Details about the endpoint of `prefix`."""


class AssetStats(PascalCaseModel):
    """Statistics about an asset."""

    plays_recent: int
    """The number of times the asset has been played recently."""
    plays_all_time: int
    """The number of times the asset has been played in total."""
    favorites: int
    """The number of times the asset has been favorited."""
    likes: int
    """The number of times the asset has been liked."""
    bookmarks: int
    """The number of times the asset has been bookmarked."""
    parent_asset_count: int
    """The number of assets that link to this asset."""
    average_rating: float | None
    """The asset's average rating."""
    number_of_ratings: int
    """The number of ratings the asset has received."""


class Asset(PascalCaseModel):
    """A game asset, such as a map or game mode."""

    asset_id: UUID
    """The asset's GUID."""
    version_id: UUID
    """The asset version's GUID."""
    public_name: str
    """The asset's name."""
    description: str
    """The asset's description."""
    files: AssetFiles
    """Information about the files that make up the asset."""
    contributors: list[str]
    """The names of the asset's contributors."""
    asset_home: int
    """The asset's home."""
    asset_stats: AssetStats
    """Statistics about the asset."""
    inspection_result: int
    """The asset's inspection result."""
    clone_behavior: int
    """The asset's clone behavior."""
    order: int
    """The asset's order."""


class MapCustomData(PascalCaseModel):
    """Custom data related to map variant assets."""

    num_of_objects_on_map: int
    """The number of objects on the map."""
    tag_level_id: int
    """The ID of the tag level."""
    is_baked: bool
    """Whether the map is baked."""
    has_node_graph: bool
    """Whether the map has a node graph."""


class Map(Asset):
    """A map variant asset."""

    custom_data: MapCustomData
    """Custom data related to the map variant."""
    tags: list[str]
    """Keywords for the map variant asset, such as "343i"."""
    prefab_links: list[Asset] | None
    """Details about prefabricated assets used by the map variant."""


class RotationWeight(PascalCaseModel):
    """A weighting for a map-mode pair in a playlist."""

    weight: float
    """The weight of the map-mode pair in the playlist."""


class RotationEntry(Asset):
    """A map-mode pair in a playlist."""

    metadata: RotationWeight
    """A weighting for the map-mode pair in the playlist."""


class PlaylistEntry(PascalCaseModel):
    """A map-mode pair in a playlist."""

    map_mode_pair_asset_id: str
    """The UUID of the map-mode pair asset."""
    metadata: RotationWeight
    """A weighting for the map-mode pair in the playlist."""


class PlaylistCustomData(PascalCaseModel):
    """Custom data related to playlist assets."""

    playlist_entries: list[PlaylistEntry]
    """The map-mode pairs in the playlist."""
    strategy: int
    """The playlist's strategy ID."""
    min_teams: int
    """The minimum number of teams needed to make a match."""
    min_team_size: int
    """The minimum number of team members needed to make a match."""
    max_teams: int
    """The maximum number of teams allowed in a match."""
    max_team_size: int
    """The maximum number of team members allowed in a match."""
    max_team_imbalance: int
    """The allowable difference in team size."""
    max_splitscreen_players_allowed: int
    """The maximum number of players allowed to play splitscreen."""
    allow_friend_join_in_progress: bool
    """Whether match players' friends are allowed to join a match in progress."""
    allow_matchmaking_join_in_progress: bool
    """Whether new players are allowed to join a match in progress."""
    allow_bot_join_in_progress: bool
    """Whether bots are allowed to join a match in progress."""
    exit_experience_duration_sec: int
    """The duration of the exit experience, in seconds."""
    fireteam_leader_kick_allowed: bool
    """Whether fireteam leaders are allowed to kick members."""
    disable_midgame_chat: bool
    """Whether chat is disabled in game."""
    allowed_device_inputs: list[int]
    """The input device IDs allowed in the playlist (KB/M, controller, etc.)."""
    bot_difficulty: int
    """The difficulty of bots in the playlist."""
    min_fireteam_size: int
    """The minimum number of players expected in a fireteam."""
    max_fireteam_size: int
    """The maximum number of players allowed in a fireteam."""


class Playlist(Asset):
    """A playlist asset."""

    custom_data: PlaylistCustomData
    """Custom data related to the playlist."""
    tags: list[str]
    """Keywords for the playlist asset, such as "343i"."""
    rotation_entries: list[RotationEntry]
    """The map-mode pairs in the playlist."""


class MapModePair(Asset):
    """A map-mode pair asset."""

    custom_data: dict[Any, Any]
    """Custom data related to the map-mode pair."""
    tags: list[str]
    """Keywords for the map-mode pair asset, such as "343i"."""
    map_link: Asset
    """Details about the map variant asset."""
    ugc_game_variant_link: Asset
    """Details about the game variant asset."""


class UgcGameVariantCustomData(PascalCaseModel):
    """Custom data related to game variant assets."""

    key_values: dict[Any, Any]
    """Key-value pairs of custom data."""


class UgcGameVariant(Asset):
    """A user-generated game variant asset."""

    custom_data: UgcGameVariantCustomData
    """Custom data related to the game variant."""
    tags: list[str]
    """Keywords for the game variant asset, such as "343i"."""
    engine_game_variant_link: Asset
    """Details about the mode's engine game variant."""
