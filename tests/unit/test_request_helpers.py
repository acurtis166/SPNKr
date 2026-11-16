"""Test request helper functions."""

import datetime as dt
from unittest.mock import Mock
from uuid import UUID

import pytest

from spnkr.models.refdata import GameplayInteraction, GameVariantCategory
from spnkr.request_helpers import (
    clean_season_id,
    get_localized_asset_kwargs,
    prepare_search_asset_params,
    prepare_service_record_params,
    validate_xuids,
)


class TestPrepareServiceRecordParams:
    """Tests for prepare_service_record_params function."""

    def test_matchmade_no_filters(self):
        """Test matchmade match type with no filters."""
        result = prepare_service_record_params(match_type="matchmade")
        assert result == {}

    def test_matchmade_with_season_id(self):
        """Test matchmade with season_id filter."""
        result = prepare_service_record_params(
            match_type="matchmade", season_id="season123"
        )
        assert result == {"seasonid": "season123"}

    def test_matchmade_with_game_variant_category(self):
        """Test matchmade with game_variant_category filter."""
        result = prepare_service_record_params(
            match_type="matchmade",
            season_id="season123",
            game_variant_category=GameVariantCategory.CAMPAIGN,
        )
        assert result == {"seasonid": "season123", "gamevariantcategory": "1"}

    def test_matchmade_with_game_variant_category_int(self):
        """Test matchmade with game_variant_category as int."""
        result = prepare_service_record_params(
            match_type="matchmade",
            season_id="season123",
            game_variant_category=0,
        )
        assert result == {"seasonid": "season123", "gamevariantcategory": "0"}

    def test_matchmade_with_playlist_asset_id(self):
        """Test matchmade with playlist_asset_id filter."""
        result = prepare_service_record_params(
            match_type="matchmade",
            season_id="season123",
            playlist_asset_id="playlist-id-123",
        )
        assert result == {"seasonid": "season123", "playlistassetid": "playlist-id-123"}

    def test_matchmade_with_uuid_playlist_asset_id(self):
        """Test matchmade with UUID playlist_asset_id."""
        uuid_val = UUID("12345678-1234-5678-1234-567812345678")
        result = prepare_service_record_params(
            match_type="matchmade",
            season_id="season123",
            playlist_asset_id=uuid_val,
        )
        assert result == {"seasonid": "season123", "playlistassetid": str(uuid_val)}

    def test_matchmade_with_is_ranked(self):
        """Test matchmade with is_ranked filter."""
        result = prepare_service_record_params(
            match_type="matchmade",
            season_id="season123",
            game_variant_category=GameVariantCategory.CAMPAIGN,
            is_ranked=True,
        )
        assert result == {
            "seasonid": "season123",
            "gamevariantcategory": "1",
            "isranked": "True",
        }

    def test_matchmade_with_gameplay_interaction(self):
        """Test matchmade with gameplay_interaction filter."""
        result = prepare_service_record_params(
            match_type="matchmade",
            season_id="season123",
            gameplay_interaction=GameplayInteraction.PVP,
        )
        assert result == {"seasonid": "season123", "gameplayinteraction": "1"}

    def test_game_variant_category_only(self):
        """Test with only game_variant_category filter."""
        result = prepare_service_record_params(
            match_type="matchmade",
            game_variant_category=GameVariantCategory.CAMPAIGN,
        )
        assert result == {"gamevariantcategory": "1"}

    def test_custom_match_type_with_filters_raises_warning(self):
        """Test that custom match type with filters raises warning."""
        with pytest.warns(UserWarning, match="only applicable to matchmade"):
            result = prepare_service_record_params(
                match_type="custom", season_id="season123"
            )
        assert result == {}

    def test_local_match_type_with_filters_raises_warning(self):
        """Test that local match type with filters raises warning."""
        with pytest.warns(UserWarning, match="only applicable to matchmade"):
            result = prepare_service_record_params(
                match_type="local", season_id="season123"
            )
        assert result == {}

    def test_invalid_filter_combination_raises_error(self):
        """Test that invalid filter combination raises ValueError."""
        with pytest.raises(ValueError, match="Invalid filter combination"):
            prepare_service_record_params(
                match_type="matchmade",
                season_id="season123",
                is_ranked=True,
            )

    def test_case_insensitive_match_type(self):
        """Test that match_type is case insensitive."""
        result = prepare_service_record_params(
            match_type="MATCHMADE",  # type: ignore
            season_id="season123",
        )
        assert result == {"seasonid": "season123"}


class TestValidateXuids:
    """Tests for validate_xuids function."""

    def test_valid_string_xuids(self):
        """Test with valid string XUIDs."""
        xuids = ["1234567890123456", "9876543210987654"]
        result = validate_xuids(xuids)
        assert result == xuids

    def test_valid_int_xuids(self):
        """Test with valid integer XUIDs."""
        xuids = [1234567890123456, 9876543210987654]
        result = validate_xuids(xuids)
        assert result == xuids

    def test_mixed_string_and_int_xuids(self):
        """Test with mixed string and int XUIDs."""
        xuids = ["1234567890123456", 9876543210987654]
        result = validate_xuids(xuids)
        assert result == xuids

    def test_tuple_input(self):
        """Test with tuple input."""
        xuids = ("1234567890123456", "9876543210987654")
        result = validate_xuids(xuids)
        assert result == list(xuids)

    def test_generator_input(self):
        """Test with generator input."""

        def xuid_gen():
            yield "1234567890123456"
            yield "9876543210987654"

        result = validate_xuids(xuid_gen())
        assert result == ["1234567890123456", "9876543210987654"]

    def test_string_input_raises_error(self):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError, match="must be an iterable"):
            validate_xuids("1234567890123456")

    def test_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_xuids([])

    def test_empty_tuple_raises_error(self):
        """Test that empty tuple raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_xuids(())


class TestPrepareSearchAssetParams:
    """Tests for prepare_search_asset_params function."""

    def test_default_params(self):
        """Test with default parameters."""
        result = prepare_search_asset_params()
        assert result == {
            "start": 0,
            "count": 25,
            "sort": "playsrecent",
            "order": "desc",
        }

    def test_custom_start_and_count(self):
        """Test with custom start and count."""
        result = prepare_search_asset_params(start=50, count=100)
        assert result["start"] == 50
        assert result["count"] == 100

    def test_custom_sort(self):
        """Test with custom sort property."""
        result = prepare_search_asset_params(sort="likes")
        assert result["sort"] == "likes"

    def test_sort_with_underscores_converted(self):
        """Test that sort properties with underscores are converted."""
        result = prepare_search_asset_params(sort="plays_all_time")
        assert result["sort"] == "playsalltime"

    def test_custom_order(self):
        """Test with custom order."""
        result = prepare_search_asset_params(order="asc")
        assert result["order"] == "asc"

    def test_asset_kind_map(self):
        """Test with asset_kind 'map'."""
        result = prepare_search_asset_params(asset_kind="map")
        assert result["assetKind"] == "map"

    def test_asset_kind_prefab(self):
        """Test with asset_kind 'prefab'."""
        result = prepare_search_asset_params(asset_kind="prefab")
        assert result["assetKind"] == "prefab"

    def test_asset_kind_ugc_game_variant(self):
        """Test with asset_kind 'ugc_game_variant'."""
        result = prepare_search_asset_params(asset_kind="ugc_game_variant")
        assert result["assetKind"] == "ugcgamevariant"

    def test_asset_kind_none_excluded(self):
        """Test that None asset_kind is excluded from params."""
        result = prepare_search_asset_params(asset_kind=None)
        assert "assetKind" not in result

    def test_term(self):
        """Test with search term."""
        result = prepare_search_asset_params(term="sword")
        assert result["term"] == "sword"

    def test_tags_as_list(self):
        """Test with tags as list."""
        result = prepare_search_asset_params(tags=["infection", "pvp"])
        assert result["tags"] == ["infection", "pvp"]

    def test_tags_as_string(self):
        """Test with tags as single string (converted to list)."""
        result = prepare_search_asset_params(tags="infection")
        assert result["tags"] == ["infection"]

    def test_author(self):
        """Test with author."""
        result = prepare_search_asset_params(author="343 Industries")
        assert result["author"] == "343 Industries"

    def test_average_rating_min(self):
        """Test with average_rating_min."""
        result = prepare_search_asset_params(average_rating_min=4.5)
        assert result["averageRatingMin"] == 4.5

    def test_from_date_created_utc_datetime(self):
        """Test with from_date_created_utc as datetime."""
        date = dt.datetime(2023, 1, 1, 12, 0, 0)
        result = prepare_search_asset_params(from_date_created_utc=date)
        assert result["fromDateCreatedUtc"] == "2023-01-01T12:00:00"

    def test_from_date_created_utc_date(self):
        """Test with from_date_created_utc as date."""
        date = dt.date(2023, 1, 1)
        result = prepare_search_asset_params(from_date_created_utc=date)
        assert result["fromDateCreatedUtc"] == "2023-01-01"

    def test_to_date_created_utc(self):
        """Test with to_date_created_utc."""
        date = dt.date(2023, 12, 31)
        result = prepare_search_asset_params(to_date_created_utc=date)
        assert result["toDateCreatedUtc"] == "2023-12-31"

    def test_from_date_modified_utc(self):
        """Test with from_date_modified_utc."""
        date = dt.date(2023, 6, 1)
        result = prepare_search_asset_params(from_date_modified_utc=date)
        assert result["fromDateModifiedUtc"] == "2023-06-01"

    def test_to_date_modified_utc(self):
        """Test with to_date_modified_utc."""
        date = dt.date(2023, 6, 30)
        result = prepare_search_asset_params(to_date_modified_utc=date)
        assert result["toDateModifiedUtc"] == "2023-06-30"

    def test_from_date_published_utc(self):
        """Test with from_date_published_utc."""
        date = dt.date(2023, 1, 1)
        result = prepare_search_asset_params(from_date_published_utc=date)
        assert result["fromDatePublishedUtc"] == "2023-01-01"

    def test_to_date_published_utc(self):
        """Test with to_date_published_utc."""
        date = dt.date(2023, 12, 31)
        result = prepare_search_asset_params(to_date_published_utc=date)
        assert result["toDatePublishedUtc"] == "2023-12-31"

    def test_all_params_combined(self):
        """Test with all parameters."""
        date = dt.date(2023, 1, 1)
        result = prepare_search_asset_params(
            start=10,
            count=50,
            sort="likes",
            order="asc",
            asset_kind="map",
            term="forge",
            tags=["creative", "customs"],
            author="Community",
            average_rating_min=4.0,
            from_date_created_utc=date,
            to_date_created_utc=date,
        )
        assert result["start"] == 10
        assert result["count"] == 50
        assert result["sort"] == "likes"
        assert result["order"] == "asc"
        assert result["assetKind"] == "map"
        assert result["term"] == "forge"
        assert result["tags"] == ["creative", "customs"]
        assert result["author"] == "Community"
        assert result["averageRatingMin"] == 4.0
        assert result["fromDateCreatedUtc"] == "2023-01-01"
        assert result["toDateCreatedUtc"] == "2023-01-01"


class TestGetLocalizedAssetKwargs:
    """Tests for get_localized_asset_kwargs function."""

    def test_language_none_returns_empty_dict(self):
        """Test that language=None returns empty dict."""
        session = Mock()
        result = get_localized_asset_kwargs(session, None)
        assert result == {}

    def test_language_specified_no_cache(self):
        """Test with language specified and no cache."""
        session = Mock()
        result = get_localized_asset_kwargs(session, "en-US")
        assert result == {"headers": {"Accept-Language": "en-US"}}

    def test_language_with_cache_include_headers_true(self):
        """Test with language and cache with include_headers=True."""
        cache = Mock()
        cache.include_headers = True
        session = Mock()
        session.cache = cache
        result = get_localized_asset_kwargs(session, "en-US")
        assert result == {"headers": {"Accept-Language": "en-US"}}

    def test_language_with_cache_include_headers_false_raises_warning(self):
        """Test that cache without include_headers raises warning."""
        cache = Mock()
        cache.include_headers = False
        session = Mock()
        session.cache = cache
        with pytest.warns(UserWarning, match="Localized Discovery UGC"):
            result = get_localized_asset_kwargs(session, "en-US")
        assert result == {"headers": {"Accept-Language": "en-US"}, "expire_after": 0}

    def test_various_languages(self):
        """Test with various language codes."""
        session = Mock()
        for lang in ["en-US", "fr-FR", "de-DE", "ja-JP", "es-ES"]:
            result = get_localized_asset_kwargs(session, lang)
            assert result == {"headers": {"Accept-Language": lang}}


class TestCleanSeasonId:
    """Tests for clean_season_id function."""

    def test_season_with_path_and_json_extension(self):
        """Test cleaning season ID with path and .json extension."""
        result = clean_season_id("Csr/Seasons/CsrSeason5-1.json")
        assert result == "CsrSeason5-1"

    def test_season_with_path_only(self):
        """Test cleaning season ID with path only."""
        result = clean_season_id("Csr/Seasons/CsrSeason10")
        assert result == "CsrSeason10"

    def test_season_with_json_extension_only(self):
        """Test cleaning season ID with .json extension only."""
        result = clean_season_id("CsrSeason3.json")
        assert result == "CsrSeason3"

    def test_season_id_no_cleaning_needed(self):
        """Test season ID that doesn't need cleaning."""
        result = clean_season_id("CsrSeason2")
        assert result == "CsrSeason2"

    def test_season_with_multiple_path_components(self):
        """Test season ID with multiple path components."""
        result = clean_season_id("Foo/Bar/Baz/Season1.json")
        assert result == "Season1"

    def test_season_with_dots_in_name(self):
        """Test season ID with dots in the name (before .json)."""
        result = clean_season_id("Path/To/Season1.0.1.json")
        assert result == "Season1.0.1"
