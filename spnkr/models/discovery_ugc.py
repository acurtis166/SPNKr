"""Models for the HIUGC_Discovery authority."""

import datetime as dt
import urllib.parse
from typing import Any
from uuid import UUID

from pydantic import Field

from spnkr.models.base import PascalCaseModel
from spnkr.models.refdata import (
    AssetHome,
    AssetKind,
    CloneBehavior,
    FilmChunkType,
    FilmStatus,
    InspectionResult,
    PlaylistBotDifficulty,
    PlaylistDeviceInput,
    PlaylistEntrySelectionStrategy,
)
from spnkr.models.types import ReadOnlyDict


class OnlineUriReference(PascalCaseModel, frozen=True):
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


class AssetFiles(PascalCaseModel, frozen=True):
    """Information about the files that make up an asset.

    Attributes:
        prefix: The root path to the asset's files.
        file_relative_paths: The relative paths to the asset's files.
        prefix_endpoint: Details about the endpoint of `prefix`.
    """

    prefix: str
    file_relative_paths: tuple[str, ...]
    prefix_endpoint: OnlineUriReference


class AssetStats(PascalCaseModel, frozen=True):
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


class Asset(PascalCaseModel, frozen=True):
    """A game asset, such as a map or game mode.

    Attributes:
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

    asset_id: UUID
    version_id: UUID
    public_name: str
    description: str
    files: AssetFiles
    contributors: tuple[str, ...]
    asset_home: AssetHome
    asset_stats: AssetStats
    inspection_result: InspectionResult
    clone_behavior: CloneBehavior
    order: int


class MapCustomData(PascalCaseModel, frozen=True):
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


class Map(Asset, frozen=True):
    """A map variant asset.

    Attributes:
        custom_data: Custom data related to the map variant.
        tags: Keywords for the map variant asset, such as "343i".
        prefab_links: Details about prefabricated assets used by the map variant.
    """

    custom_data: MapCustomData
    tags: tuple[str, ...]
    prefab_links: tuple[Asset, ...] | None


class RotationWeight(PascalCaseModel, frozen=True):
    """A weighting for a map-mode pair in a playlist.

    Attributes:
        weight: The weight of the map-mode pair in the playlist.
    """

    weight: float


class RotationEntry(Asset, frozen=True):
    """A map-mode pair in a playlist.

    Attributes:
        metadata: A weighting for the map-mode pair in the playlist.
    """

    metadata: RotationWeight


class PlaylistEntry(PascalCaseModel, frozen=True):
    """A map-mode pair in a playlist.

    Attributes:
        map_mode_pair_asset_id: The UUID of the map-mode pair asset.
        metadata: A weighting for the map-mode pair in the playlist.
    """

    map_mode_pair_asset_id: str
    metadata: RotationWeight


class PlaylistCustomData(PascalCaseModel, frozen=True):
    """Custom data related to playlist assets.

    Attributes:
        playlist_entries: The map-mode pairs in the playlist.
        strategy: The strategy used to select map-mode pairs in the playlist.
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
        allowed_device_inputs: The input devices allowed in the playlist (KB/M, controller, etc.).
        bot_difficulty: The difficulty of bots in the playlist.
        min_fireteam_size: The minimum number of players expected in a fireteam.
        max_fireteam_size: The maximum number of players allowed in a fireteam.
    """

    playlist_entries: tuple[PlaylistEntry, ...]
    strategy: PlaylistEntrySelectionStrategy
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
    allowed_device_inputs: tuple[PlaylistDeviceInput, ...]
    bot_difficulty: PlaylistBotDifficulty
    min_fireteam_size: int
    max_fireteam_size: int


class Playlist(Asset, frozen=True):
    """A playlist asset.

    Attributes:
        custom_data: Custom data related to the playlist.
        tags: Keywords for the playlist asset, such as "343i".
        rotation_entries: The map-mode pairs in the playlist.
    """

    custom_data: PlaylistCustomData
    tags: tuple[str, ...]
    rotation_entries: tuple[RotationEntry, ...]


class MapModePair(Asset, frozen=True):
    """A map-mode pair asset.

    Attributes:
        custom_data: Custom data related to the map-mode pair.
        tags: Keywords for the map-mode pair asset, such as "343i".
        map_link: Details about the map variant asset.
        ugc_game_variant_link: Details about the game variant asset.
    """

    custom_data: ReadOnlyDict[Any, Any]
    tags: tuple[str, ...]
    map_link: Asset | None
    ugc_game_variant_link: Asset


class UgcGameVariantCustomData(PascalCaseModel, frozen=True):
    """Custom data related to game variant assets.

    Attributes:
        key_values: Key-value pairs of custom data.
    """

    key_values: ReadOnlyDict[Any, Any]


class UgcGameVariant(Asset, frozen=True):
    """A user-generated game variant asset.

    Attributes:
        custom_data: Custom data related to the game variant.
        tags: Keywords for the game variant asset, such as "343i".
        engine_game_variant_link: Details about the mode's engine game variant.
    """

    custom_data: UgcGameVariantCustomData
    tags: tuple[str, ...]
    engine_game_variant_link: Asset


class AssetSearchTagCount(PascalCaseModel, frozen=True):
    """A tag name and count.

    Attributes:
        tag: The tag name.
        count: The number of times the tag appears in the filtered search results.
    """

    tag: str
    count: int


class Date(PascalCaseModel, frozen=True):
    """A date object.

    Attributes:
        value: The date value.
    """

    value: dt.datetime = Field(alias="ISO8601Date")


class AssetSearchResult(PascalCaseModel, frozen=True):
    """An individual asset search result.

    Attributes:
        asset_id: The UUID of the asset.
        asset_version_id: The UUID of the asset version.
        name: The asset's name.
        description: The asset's description.
        asset_kind: The kind of asset, such as "map".
        tags: Keywords for the asset, such as "343i".
        thumbnail_url: The URL of the asset's thumbnail image.
        referenced_assets: The UUIDs of assets referenced by the asset.
        original_author: The ID of the asset's original author.
        likes: The number of times the asset has been liked.
        bookmarks: The number of times the asset has been bookmarked.
        plays_recent: The number of times the asset has been played recently.
        number_of_objects: The number of objects in a map/prefab asset.
        date_created_utc: The asset's creation date.
        date_modified_utc: The asset's modification date.
        date_published_utc: The asset's publication date.
        has_node_graph: Whether the map has a node graph.
        read_only_clones: Whether clones of the asset can be modified.
        plays_all_time: The number of times the asset has been played in total.
        contributors: The IDs of the asset's contributors.
        parent_asset_count: The number of assets that link to this asset.
        average_rating: The asset's average rating.
        number_of_ratings: The number of ratings the asset has received.
    """

    asset_id: UUID
    asset_version_id: UUID
    name: str
    description: str
    asset_kind: AssetKind
    tags: tuple[str, ...]
    thumbnail_url: str
    referenced_assets: tuple[UUID, ...]
    original_author: str
    likes: int
    bookmarks: int
    plays_recent: int
    number_of_objects: int
    date_created_utc: Date
    date_modified_utc: Date
    date_published_utc: Date
    has_node_graph: bool | None
    read_only_clones: bool
    plays_all_time: int
    contributors: tuple[str, ...]
    parent_asset_count: int
    average_rating: float
    number_of_ratings: int


class AssetSearchPage(PascalCaseModel, frozen=True):
    """A page of map/mode/prefab search results.

    Attributes:
        tags: The tags that appear in the filtered search results.
        estimated_total: The estimated total number of results.
        start: The index of the first result returned.
        count: The number of results requested.
        result_count: The number of results returned.
        results: The search results.
        links: ...
    """

    tags: tuple[AssetSearchTagCount, ...]
    estimated_total: int
    start: int
    count: int
    result_count: int
    results: tuple[AssetSearchResult, ...]
    links: ReadOnlyDict[Any, Any]


class FilmChunk(PascalCaseModel, frozen=True):
    """A chunk of a saved film.

    Attributes:
        index: The index of the chunk.
        chunk_start_time_offset_milliseconds: The start time of the chunk, in
            milliseconds.
        duration_milliseconds: The duration of the chunk, in milliseconds.
        chunk_size: The size of the chunk, in bytes.
        file_relative_path: The relative path to the chunk's file.
        chunk_type: The type of chunk - header, replication data, or highlight
            events.
    """

    index: int
    chunk_start_time_offset_milliseconds: int
    duration_milliseconds: int
    chunk_size: int
    file_relative_path: str
    chunk_type: FilmChunkType


class FilmCustomData(PascalCaseModel, frozen=True):
    """Custom data related to film assets.

    Attributes:
        film_length: The length of the film, in milliseconds.
        chunks: The film's chunks.
        has_game_ended: Whether the game has ended.
        manifest_refresh_seconds: ...
        match_id: The UUID of the match.
        film_major_version: The film's major version.
    """

    film_length: int
    chunks: tuple[FilmChunk, ...]
    has_game_ended: bool
    manifest_refresh_seconds: int
    match_id: UUID
    film_major_version: int


class Film(PascalCaseModel, frozen=True):
    """A saved film asset for a match.

    Attributes:
        film_status_bond: The status, such as "complete", of the film.
        custom_data: Data specific to film assets, such as length and chunks.
        blob_storage_path_prefix: The prefix for the film's blob storage path.
        asset_id: The UUID of the film asset.
    """

    film_status_bond: FilmStatus
    custom_data: FilmCustomData
    blob_storage_path_prefix: str
    asset_id: UUID

    @property
    def highlight_events_url(self) -> str | None:
        """Get the URL for the "highlight events" chunk of the film, if available."""
        chunk, url = self.get_chunks_and_urls()[-1]
        if chunk.chunk_type is FilmChunkType.HIGHLIGHT_EVENTS:
            return url

    def get_chunks_and_urls(self) -> list[tuple[FilmChunk, str]]:
        """Get (chunk, URL) tuples for all film chunks, in order of index.

        URLs are public blob storage URLs for downloading the compressed binary chunk
        data. The first is the film header, the last chunk is highlight events, and all
        chunks in between are 20-second replication data chunks.

        Returns:
            The chunk and blob storage URL pairs.
        """
        out = []
        prefix = self.blob_storage_path_prefix
        for chunk in sorted(self.custom_data.chunks, key=lambda c: c.index):
            name = chunk.file_relative_path.lstrip("/")
            path = urllib.parse.urljoin(prefix, name)
            out.append((chunk, path))
        return out
