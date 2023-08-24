"""Models for the HIUGC_Discovery authority."""

from typing import Any
from uuid import UUID

from ..refdata import AssetKind
from .base import PascalCaseModel


class OnlineUriReference(PascalCaseModel):
    """A reference to an online resource.

    Attributes:
        authority_id: The ID of the authority that hosts the resource.
        path: The path to the resource, relative to the authority's host.
        query_string: The query string of the resource's URL.
        retry_policy_id: The ID of the retry policy to use when accessing the resource.
        topic_name: The name of the topic to use when accessing the resource.
        acknowledgement_type_id: The ID of the acknowledgement type to use when accessing the resource.
        authentication_lifetime_extension_supported: Whether the resource supports extending the lifetime of an authentication token.
        clearance_aware: Whether the resource is clearance aware.
    """

    authority_id: str
    path: str
    query_string: str | None
    retry_policy_id: str
    topic_name: str
    acknowledgement_type_id: int
    authentication_lifetime_extension_supported: bool
    clearance_aware: bool


class AssetFiles(PascalCaseModel):
    """Information about the files that make up an asset.

    Attributes:
        prefix: The root path to the asset's files.
        file_relative_paths: The relative paths to the asset's files.
        prefix_endpoint: Details about the endpoint of `prefix`.
    """

    prefix: str
    file_relative_paths: list[str]
    prefix_endpoint: OnlineUriReference


class AssetStats(PascalCaseModel):
    """Statistics about an asset.

    Attributes:
        plays_recent: The number of times the asset has been played recently.
        plays_all_time: The number of times the asset has been played in total.
        favorites: The number of times the asset has been favorited.
        likes: The number of times the asset has been liked.
        bookmarks: The number of times the asset has been bookmarked.
        parent_asset_count: The number of assets that link to this asset.
        average_rating: The asset's average rating.
        number_of_ratings: The number of ratings the asset has received.
    """

    plays_recent: int
    plays_all_time: int
    favorites: int
    likes: int
    bookmarks: int
    parent_asset_count: int
    average_rating: float | None
    number_of_ratings: int


class Asset(PascalCaseModel):
    """A game asset, such as a map or game mode.

    Attributes:
        asset_type: The type of asset.
        asset_id: The asset's GUID.
        version_id: The asset version's GUID.
        public_name: The asset's name.
        description: The asset's description.
        files: Information about the files that make up the asset.
        contributors: The names of the asset's contributors.
        asset_home: The asset's home.
        asset_stats: Statistics about the asset.
        inspection_result: The asset's inspection result.
        clone_behavior: The asset's clone behavior.
        order: The asset's order.
    """

    asset_type: AssetKind
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
    """Custom data related to map variant assets.

    Attributes:
        num_of_objects_on_map: The number of objects on the map.
        tag_level_id: The ID of the tag level.
        is_baked: Whether the map is baked.
        has_node_graph: Whether the map has a node graph.
    """

    num_of_objects_on_map: int
    tag_level_id: int
    is_baked: bool
    has_node_graph: bool


class Map(Asset):
    """A map variant asset.

    Attributes:
        custom_data: Custom data related to the map variant.
        tags: Keywords for the map variant asset, such as "343i".
        prefab_links: Details about prefabricated assets used by the map variant.
    """

    custom_data: MapCustomData
    tags: list[str]
    prefab_links: list[Asset] | None


class RotationWeight(PascalCaseModel):
    """A weighting for a map-mode pair in a playlist.

    Attributes:
        weight: The weight of the map-mode pair in the playlist.
    """

    weight: float


class RotationEntry(Asset):
    """A map-mode pair in a playlist.

    Attributes:
        metadata: A weighting for the map-mode pair in the playlist.
    """

    metadata: RotationWeight


class PlaylistEntry(PascalCaseModel):
    """A map-mode pair in a playlist.

    Attributes:
        map_mode_pair_asset_id: The UUID of the map-mode pair asset.
        metadata: A weighting for the map-mode pair in the playlist.
    """

    map_mode_pair_asset_id: str
    metadata: RotationWeight


class PlaylistCustomData(PascalCaseModel):
    """Custom data related to playlist assets.

    Attributes:
        playlist_entries: The map-mode pairs in the playlist.
        strategy: The playlist's strategy ID.
        min_teams: The minimum number of teams needed to make a match.
        min_team_size: The minimum number of team members needed to make a match.
        max_teams: The maximum number of teams allowed in a match.
        max_team_size: The maximum number of team members allowed in a match.
        max_team_imbalance: The allowable difference in team size.
        max_splitscreen_players_allowed: The maximum number of players allowed to play splitscreen.
        allow_friend_join_in_progress: Whether match players' friends are allowed to join a match in progress.
        allow_matchmaking_join_in_progress: Whether new players are allowed to join a match in progress.
        allow_bot_join_in_progress: Whether bots are allowed to join a match in progress.
        exit_experience_duration_sec: The duration of the exit experience, in seconds.
        fireteam_leader_kick_allowed: Whether fireteam leaders are allowed to kick members.
        disable_midgame_chat: Whether chat is disabled in game.
        allowed_device_inputs: The input device IDs allowed in the playlist (KB/M, controller, etc.).
        bot_difficulty: The difficulty of bots in the playlist.
        min_fireteam_size: The minimum number of players expected in a fireteam.
        max_fireteam_size: The maximum number of players allowed in a fireteam.
    """

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
    """A playlist asset.

    Attributes:
        custom_data: Custom data related to the playlist.
        tags: Keywords for the playlist asset, such as "343i".
        rotation_entries: The map-mode pairs in the playlist.
    """

    custom_data: PlaylistCustomData
    tags: list[str]
    rotation_entries: list[RotationEntry]


class MapModePair(Asset):
    """A map-mode pair asset.

    Attributes:
        custom_data: Custom data related to the map-mode pair.
        tags: Keywords for the map-mode pair asset, such as "343i".
        map_link: Details about the map variant asset.
        ugc_game_variant_link: Details about the game variant asset.
    """

    custom_data: dict[Any, Any]
    tags: list[str]
    map_link: Asset
    ugc_game_variant_link: Asset


class UgcGameVariantCustomData(PascalCaseModel):
    """Custom data related to game variant assets.

    Attributes:
        key_values: Key-value pairs of custom data.
    """

    key_values: dict[Any, Any]


class UgcGameVariant(Asset):
    """A user-generated game variant asset.

    Attributes:
        custom_data: Custom data related to the game variant.
        tags: Keywords for the game variant asset, such as "343i".
        engine_game_variant_link: Details about the mode's engine game variant.
    """

    custom_data: UgcGameVariantCustomData
    tags: list[str]
    engine_game_variant_link: Asset
