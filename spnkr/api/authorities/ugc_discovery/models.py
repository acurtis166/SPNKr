"""Models for the HIUGC_Discovery authority."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from spnkr.models import Date


@dataclass(frozen=True)
class OnlineUriReference:
    authority_id: str
    path: str
    query_string: str | None
    retry_policy_id: str
    topic_name: str
    acknowledgement_type_id: int
    authentication_lifetime_extension_supported: bool
    clearance_aware: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OnlineUriReference:
        return cls(
            authority_id=data["AuthorityId"],
            path=data["Path"],
            query_string=data.get("QueryString"),
            retry_policy_id=data["RetryPolicyId"],
            topic_name=data["TopicName"],
            acknowledgement_type_id=data["AcknowledgementTypeId"],
            authentication_lifetime_extension_supported=data[
                "AuthenticationLifetimeExtensionSupported"
            ],
            clearance_aware=data["ClearanceAware"],
        )


@dataclass(frozen=True)
class AssetFiles:
    prefix: str
    file_relative_paths: list[str]
    prefix_endpoint: OnlineUriReference

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AssetFiles:
        return cls(
            prefix=data["Prefix"],
            file_relative_paths=data["FileRelativePaths"],
            prefix_endpoint=OnlineUriReference.from_dict(
                data["PrefixEndpoint"]
            ),
        )


@dataclass(frozen=True)
class AssetStats:
    plays_recent: int
    plays_all_time: int
    favorites: int
    likes: int
    bookmarks: int
    parent_asset_count: int
    average_rating: float | None
    number_of_ratings: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AssetStats:
        return cls(
            plays_recent=data["PlaysRecent"],
            plays_all_time=data["PlaysAllTime"],
            favorites=data["Favorites"],
            likes=data["Likes"],
            bookmarks=data["Bookmarks"],
            parent_asset_count=data["ParentAssetCount"],
            average_rating=data.get("AverageRating"),
            number_of_ratings=data["NumberOfRatings"],
        )


@dataclass(frozen=True)
class Asset:
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Asset:
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
        )


@dataclass(frozen=True)
class ManifestCustomData:
    branch_name: str
    build_number: str
    kind: int
    content_version: str
    build_guid: UUID
    visibility: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ManifestCustomData:
        return cls(
            branch_name=data["BranchName"],
            build_number=data["BuildNumber"],
            kind=data["Kind"],
            content_version=data["ContentVersion"],
            build_guid=UUID(data["BuildGuid"]),
            visibility=data["Visibility"],
        )


@dataclass(frozen=True)
class Manifest(Asset):
    custom_data: ManifestCustomData | None
    tags: list[str]
    map_links: list[Asset]
    playlist_links: list[Asset]
    ugc_game_variant_links: list[Asset]
    prefab_links: list[Asset] | None = None
    map_mode_pair_links: list[Asset] | None = None
    engine_game_variant_links: list[Asset] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Manifest:
        custom_data = None
        if data["CustomData"]:
            custom_data = ManifestCustomData.from_dict(data["CustomData"])
        prefab_links = None
        if "PrefabLinks" in data:
            prefab_links = [
                Asset.from_dict(link) for link in data["PrefabLinks"]
            ]
        map_mode_pair_links = None
        if "MapModePairLinks" in data:
            map_mode_pair_links = [
                Asset.from_dict(link) for link in data["MapModePairLinks"]
            ]
        engine_game_variant_links = None
        if "EngineGameVariantLinks" in data:
            engine_game_variant_links = [
                Asset.from_dict(link) for link in data["EngineGameVariantLinks"]
            ]
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            custom_data=custom_data,
            tags=data["Tags"],
            map_links=[Asset.from_dict(link) for link in data["MapLinks"]],
            playlist_links=[
                Asset.from_dict(link) for link in data["PlaylistLinks"]
            ],
            ugc_game_variant_links=[
                Asset.from_dict(link) for link in data["UgcGameVariantLinks"]
            ],
            prefab_links=prefab_links,
            map_mode_pair_links=map_mode_pair_links,
            engine_game_variant_links=engine_game_variant_links,
        )


@dataclass(frozen=True)
class Project(Asset):
    custom_data: dict[Any, Any]
    tags: list[str]
    map_links: list[Asset]
    playlist_links: list[Asset]
    prefab_links: list[Asset] | None
    ugc_game_variant_links: list[Asset]
    map_mode_pair_links: list[Asset] | None
    engine_game_variant_links: list[Asset] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Project:
        prefab_links = None
        if data["PrefabLinks"]:
            prefab_links = [
                Asset.from_dict(link) for link in data["PrefabLinks"]
            ]
        map_mode_pair_links = None
        if data["MapModePairLinks"]:
            map_mode_pair_links = [
                Asset.from_dict(link) for link in data["MapModePairLinks"]
            ]
        engine_game_variant_links = None
        if "EngineGameVariantLinks" in data:
            engine_game_variant_links = [
                Asset.from_dict(link) for link in data["EngineGameVariantLinks"]
            ]
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            custom_data=data["CustomData"],
            tags=data["Tags"],
            map_links=[Asset.from_dict(link) for link in data["MapLinks"]],
            playlist_links=[
                Asset.from_dict(link) for link in data["PlaylistLinks"]
            ],
            prefab_links=prefab_links,
            ugc_game_variant_links=[
                Asset.from_dict(link) for link in data["UgcGameVariantLinks"]
            ],
            map_mode_pair_links=map_mode_pair_links,
            engine_game_variant_links=engine_game_variant_links,
        )


@dataclass(frozen=True)
class EngineGameVariantSubsetData:
    stat_bucket_game_type: int
    engine_name: str
    variant_name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EngineGameVariantSubsetData:
        return cls(
            stat_bucket_game_type=data["StatBucketGameType"],
            engine_name=data["EngineName"],
            variant_name=data["VariantName"],
        )


@dataclass(frozen=True)
class EngineGameVariantCustomData:
    subset_data: EngineGameVariantSubsetData
    localized_data: dict[Any, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EngineGameVariantCustomData:
        return cls(
            subset_data=EngineGameVariantSubsetData.from_dict(
                data["SubsetData"]
            ),
            localized_data=data["LocalizedData"],
        )


@dataclass(frozen=True)
class EngineGameVariant(Asset):
    custom_data: EngineGameVariantCustomData
    tags: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EngineGameVariant:
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            custom_data=EngineGameVariantCustomData.from_dict(
                data["CustomData"]
            ),
            tags=data["Tags"],
        )


@dataclass(frozen=True)
class MapCustomData:
    num_of_objects_on_map: int
    tag_level_id: int
    is_baked: bool
    has_node_graph: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MapCustomData:
        return cls(
            num_of_objects_on_map=data["NumOfObjectsOnMap"],
            tag_level_id=data["TagLevelId"],
            is_baked=data["IsBaked"],
            has_node_graph=data["HasNodeGraph"],
        )


@dataclass(frozen=True)
class Map(Asset):
    custom_data: MapCustomData
    tags: list[str]
    prefab_links: list[Asset] | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Map:
        prefab_links = None
        if data["PrefabLinks"]:
            prefab_links = [
                Asset.from_dict(link) for link in data["PrefabLinks"]
            ]
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            custom_data=MapCustomData.from_dict(data["CustomData"]),
            tags=data["Tags"],
            prefab_links=prefab_links,
        )


@dataclass(frozen=True)
class RotationWeight:
    weight: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RotationWeight:
        return cls(
            weight=data["Weight"],
        )


@dataclass(frozen=True)
class RotationEntry(Asset):
    metadata: RotationWeight

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RotationEntry:
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            metadata=RotationWeight.from_dict(data["Metadata"]),
        )


@dataclass(frozen=True)
class PlaylistEntry:
    map_mode_pair_asset_id: str
    metadata: RotationWeight

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PlaylistEntry:
        return cls(
            map_mode_pair_asset_id=data["MapModePairAssetId"],
            metadata=RotationWeight.from_dict(data["Metadata"]),
        )


@dataclass(frozen=True)
class PlaylistCustomData:
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PlaylistCustomData:
        return cls(
            playlist_entries=[
                PlaylistEntry.from_dict(entry)
                for entry in data["PlaylistEntries"]
            ],
            strategy=data["Strategy"],
            min_teams=data["MinTeams"],
            min_team_size=data["MinTeamSize"],
            max_teams=data["MaxTeams"],
            max_team_size=data["MaxTeamSize"],
            max_team_imbalance=data["MaxTeamImbalance"],
            max_splitscreen_players_allowed=data[
                "MaxSplitscreenPlayersAllowed"
            ],
            allow_friend_join_in_progress=data["AllowFriendJoinInProgress"],
            allow_matchmaking_join_in_progress=data[
                "AllowMatchmakingJoinInProgress"
            ],
            allow_bot_join_in_progress=data["AllowBotJoinInProgress"],
            exit_experience_duration_sec=data["ExitExperienceDurationSec"],
            fireteam_leader_kick_allowed=data["FireteamLeaderKickAllowed"],
            disable_midgame_chat=data["DisableMidgameChat"],
            allowed_device_inputs=data["AllowedDeviceInputs"],
            bot_difficulty=data["BotDifficulty"],
            min_fireteam_size=data["MinFireteamSize"],
            max_fireteam_size=data["MaxFireteamSize"],
        )


@dataclass(frozen=True)
class Playlist(Asset):
    custom_data: PlaylistCustomData
    tags: list[str]
    rotation_entries: list[RotationEntry]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Playlist:
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            custom_data=PlaylistCustomData.from_dict(data["CustomData"]),
            tags=data["Tags"],
            rotation_entries=[
                RotationEntry.from_dict(entry)
                for entry in data["RotationEntries"]
            ],
        )


@dataclass(frozen=True)
class MapModePair(Asset):
    custom_data: dict[Any, Any]
    tags: list[str]
    map_link: Asset
    ugc_game_variant_link: Asset

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MapModePair:
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            custom_data=data["CustomData"],
            tags=data["Tags"],
            map_link=Asset.from_dict(data["MapLink"]),
            ugc_game_variant_link=Asset.from_dict(data["UgcGameVariantLink"]),
        )


@dataclass(frozen=True)
class PrefabCustomData:
    parts: int
    has_node_graph: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PrefabCustomData:
        return cls(
            parts=data["Parts"],
            has_node_graph=data["HasNodeGraph"],
        )


@dataclass(frozen=True)
class Prefab(Asset):
    custom_data: PrefabCustomData
    tags: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Prefab:
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            custom_data=PrefabCustomData.from_dict(data["CustomData"]),
            tags=data["Tags"],
        )


@dataclass(frozen=True)
class Tag:
    name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Tag:
        return cls(name=data["Name"])


@dataclass(frozen=True)
class TagsInfo:
    canned_tags: list[Tag]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TagsInfo:
        return cls(
            canned_tags=[Tag.from_dict(tag) for tag in data["CannedTags"]],
        )


@dataclass(frozen=True)
class UgcGameVariantCustomData:
    key_values: dict[Any, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UgcGameVariantCustomData:
        return cls(key_values=data["KeyValues"])


@dataclass(frozen=True)
class UgcGameVariant(Asset):
    custom_data: UgcGameVariantCustomData
    tags: list[str]
    engine_game_variant_link: Asset

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UgcGameVariant:
        return cls(
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
            public_name=data["PublicName"],
            description=data["Description"],
            files=AssetFiles.from_dict(data["Files"]),
            contributors=data["Contributors"],
            asset_home=data["AssetHome"],
            asset_stats=AssetStats.from_dict(data["AssetStats"]),
            inspection_result=data["InspectionResult"],
            clone_behavior=data["CloneBehavior"],
            order=data["Order"],
            custom_data=UgcGameVariantCustomData.from_dict(data["CustomData"]),
            tags=data["Tags"],
            engine_game_variant_link=Asset.from_dict(
                data["EngineGameVariantLink"]
            ),
        )


@dataclass(frozen=True)
class TagCount:
    tag: str
    count: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TagCount:
        return cls(tag=data["Tag"], count=data["Count"])


@dataclass(frozen=True)
class SearchResult:
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SearchResult:
        return cls(
            asset_id=data["AssetId"],
            asset_version_id=data["AssetVersionId"],
            name=data["Name"],
            description=data["Description"],
            asset_kind=data["AssetKind"],
            tags=data["Tags"],
            thumbnail_url=data["ThumbnailUrl"],
            referenced_assets=data["ReferencedAssets"],
            original_author=data["OriginalAuthor"],
            likes=data["Likes"],
            bookmarks=data["Bookmarks"],
            plays_recent=data["PlaysRecent"],
            number_of_objects=data["NumberOfObjects"],
            date_created_utc=Date.from_dict(data["DateCreatedUtc"]),
            date_modified_utc=Date.from_dict(data["DateModifiedUtc"]),
            date_published_utc=Date.from_dict(data["DatePublishedUtc"]),
            has_node_graph=data["HasNodeGraph"],
            read_only_clones=data["ReadOnlyClones"],
            plays_all_time=data["PlaysAllTime"],
            contributors=data["Contributors"],
            parent_asset_count=data["ParentAssetCount"],
            average_rating=data["AverageRating"],
            number_of_ratings=data["NumberOfRatings"],
        )


@dataclass(frozen=True)
class Search:
    tags: list[TagCount]
    estimated_total: int
    start: int
    count: int
    result_count: int
    results: list[SearchResult]
    links: dict[Any, Any]  # uncertain

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Search:
        return cls(
            tags=[TagCount.from_dict(tag) for tag in data["Tags"]],
            estimated_total=data["EstimatedTotal"],
            start=data["Start"],
            count=data["Count"],
            result_count=data["ResultCount"],
            results=[
                SearchResult.from_dict(result) for result in data["Results"]
            ],
            links=data["Links"],
        )


@dataclass(frozen=True)
class FilmChunk:
    index: int
    chunk_start_time_offset_milliseconds: int
    duration_milliseconds: int
    chunk_size: int
    file_relative_path: str
    chunk_type: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FilmChunk:
        return cls(
            index=data["Index"],
            chunk_start_time_offset_milliseconds=data[
                "ChunkStartTimeOffsetMilliseconds"
            ],
            duration_milliseconds=data["DurationMilliseconds"],
            chunk_size=data["ChunkSize"],
            file_relative_path=data["FileRelativePath"],
            chunk_type=data["ChunkType"],
        )


@dataclass(frozen=True)
class FilmCustomData:
    film_length: int
    chunks: list[FilmChunk]
    has_game_ended: bool
    manifest_refresh_seconds: int
    match_id: str
    film_major_version: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FilmCustomData:
        return cls(
            film_length=data["FilmLength"],
            chunks=[FilmChunk.from_dict(chunk) for chunk in data["Chunks"]],
            has_game_ended=data["HasGameEnded"],
            manifest_refresh_seconds=data["ManifestRefreshSeconds"],
            match_id=data["MatchId"],
            film_major_version=data["FilmMajorVersion"],
        )


@dataclass(frozen=True)
class Film:
    film_status_bond: int
    custom_data: FilmCustomData
    blob_storage_path_prefix: str
    asset_id: UUID

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Film:
        return cls(
            film_status_bond=data["FilmStatusBond"],
            custom_data=FilmCustomData.from_dict(data["CustomData"]),
            blob_storage_path_prefix=data["BlobStoragePathPrefix"],
            asset_id=UUID(data["AssetId"]),
        )
