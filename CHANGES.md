# Changelog

## [Unreleased]

## [0.10.0] - 2025-08-08

### Added

- Add `VipStats` model for the match stats response.
- Add `MedalNameId` class to enumerate medal name ids in stats and metadata responses.
- Add `PersonalScoreNameId` class to enumerate personal score name ids in stats responses.

### Changed

- Rename some members of `GameVariantCategory`, `LifecycleMode`, `PlaylistExperience`, and `SubTier` enums to align with data sources.
- Rename `tools` module to `extras`.
- Refactor `tools.Rank` class (now `extras.CompetitiveSkillRank`)

### Removed

- Remove several items from the `tools` module that are accessible elsewhere.

## [0.9.6] - 2025-07-24

### Fixed

- Fix film highlight event parsing for major versions >=39.

## [0.9.5] - 2025-02-04

### Added

- Add medal encodings for highlight event parsing.
- Add medal name ID to name mapping entries.
- Add additional attributes to match stats and service record models.
- Add "gameplay_interaction" parameter to service record request.

## [0.9.4] - 2024-10-17

### Fixed

- Fix `tools.BOT_MAP`. Original values were pulled from Halo Waypoint network traffic. New values line up to bot names used in-game.

## [0.9.3] - 2024-10-16

### Added

- New `xuids` property on `MatchStats` as a convenience to get all user IDs.

### Fixed

- Fix `MatchSkillResult` model to handle missing attributes in skill response parsing.
- Use single, shared event loop for tests to fix error with unclosed event loop.

## [0.9.2] - 2024-10-02

### Added

- New medal encodings for highlight event parsing.
- Medal name ID to name mapping.

## [0.9.1] - 2024-08-27

### Fixed

- Include "spnkr/film/medal_codes.json" as package data via MANIFEST.in file.

## [0.9.0] - 2024-08-26

### Added

- Read functionality for highlight event film chunks.

### Changed

- Remove ability to pass `None` as an argument for `requests_per_second` when creating a client.

## [0.8.0] - 2024-05-11

### Added

- Economy service, `get_player_customization` method, and associated response model.
- Exposed token updating for `HaloInfiniteClient` via a `set_tokens` method.
- Primary imports are available directly from `spnkr`.

### Changed

- Return `aiohttp.ClientResponse` wrappers from service methods instead of returning Pydantic response models directly. This provides access to the raw response data and doesn't force users to subscribe to parsing the full payload.
- Use absolute imports instead of relative.
- Simplify session and response typing.

## [0.7.0] - 2024-04-25

### Added

- Error handling for failed OAuth2 authentication.

### Fixed

- Added `FIREFIGHT` enum value to `PlaylistExperience`.

## [0.6.0] - 2024-02-23

### Added

- `is_human` property to `PlayerStats` model.
- Caching support via `aiohttp-client-cache`.
- Integration tests.

### Fixed

- AsyncMock warning in tests.
- Added `LOCAL_AREA_NETWORK` enum value to `LifecycleMode`.

## [0.5.0] - 2023-12-17

### Changed

- Changed some `int` types on `discovery_ugc` response models to enumerated data types where applicable. The new types include `AssetHome`, `CloneBehavior`, `InspectionResult`, `PlaylistBotDifficulty`, `PlaylistDeviceInput`, and `PlaylistEntrySelectionStrategy`.
- Response models are now "faux immutable".
    - Set all models to be "frozen" via Pydantic configuration.
    - Replaced `list` types with `tuple` types.
    - Replaced `dict` types with a simple, read-only mapping type.

### Added

- `DiscoveryUgcService.search_assets` method.
- `DiscoveryUgcService.get_film_by_match_id` method.
- `GameCmsHacsService.get_csr_season_calendar` method.
- `GameCmsHacsService.get_season_calendar` method.
- `GameCmsHacsService.get_career_reward_track` method.
- `GameCmsHacsService.get_image` method.

### Fixed

- Unregistered `GameVariantCategory` variants are handled by assigning them to a default `UNKNOWN` variant.

## [0.4.0] - 2023-12-06

### Changed

- Service methods now return parsed JSON as Pydantic models. In turn, Pydantic is now a required dependency.
- Record parsing logic was removed.
- `spnkr.parsers` module was renamed to `spnkr.models` and restructured to contain the Pydantic response models.
- Removed unnecessary parameters from clearance token request.

### Added

- `SkillService.get_playlist_csr` method now has a `season` parameter.

### Fixed

- `str` and empty `xuids` arguments are now handled appropriately by `ProfileService.get_users_by_id`, `SkillService.get_match_skill`, and `SkillService.get_playlist_csr`.
- `GameVariantCategory` enum now has an entry for "Firefight Bastion".

## [0.3.0] - 2023-11-30

### Changed

- Grouped endpoints by their URL hosts to create a `services` module. The data retrieval methods didn't change, but they did move to their respective service classes. `HaloInfiniteClient` remains the core API entrypoint, but now indirectly serves data via cached service properties `gamecms_hacs`, `profile`, `discovery_ugc`, `skill`, and `stats`. This will make adding more services and endpoints more graceful than just appending more methods to the client class. Additionally, this design makes it easy to rate-limit requests per host rather than globally.

## [0.2.0] - 2023-11-28

### Added

- `HaloInfiniteClient.get_service_record` method.
- `HaloInfiniteClient.get_current_user` method.
- `HaloInfiniteClient.get_user_by_gamertag` method.
- `HaloInfiniteClient.get_user_by_id` method.
- `HaloInfiniteClient.get_users_by_id` method.
- User and service record parsing for the above methods.
- Support for gamertags as player arguments to "stats" client methods (`get_match_count`, `get_match_history`, `get_service_record`, `get_match_stats`).
- New enum entries based on HaloWaypoint JavaScript code.
- New mappings, `BOT_MAP` and `TEAM_MAP`, to the `tools` module.

### Changed

- XUID wrapping/unwrapping to be more precise/strict.
- `xuid` parameter to `player` for "stats" client methods.
- `Tier.NOT_APPLICABLE` to `Tier.UNRANKED` for accuracy.

### Fixed

- Allow `None` for `MapModePair.map_link` attribute in Pydantic parsing.
- `SubTier` enum values (zero-based index increasing by CSR).

## [0.1.0] - 2023-08-24

First documented release.

[unreleased]: https://github.com/acurtis166/SPNKr/compare/v0.10.0...HEAD
[0.10.0]: https://github.com/acurtis166/SPNKr/compare/v0.9.6...v0.10.0
[0.9.6]: https://github.com/acurtis166/SPNKr/compare/v0.9.5...v0.9.6
[0.9.5]: https://github.com/acurtis166/SPNKr/compare/v0.9.4...v0.9.5
[0.9.4]: https://github.com/acurtis166/SPNKr/compare/v0.9.3...v0.9.4
[0.9.3]: https://github.com/acurtis166/SPNKr/compare/v0.9.2...v0.9.3
[0.9.2]: https://github.com/acurtis166/SPNKr/compare/v0.9.1...v0.9.2
[0.9.1]: https://github.com/acurtis166/SPNKr/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/acurtis166/SPNKr/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/acurtis166/SPNKr/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/acurtis166/SPNKr/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/acurtis166/SPNKr/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/acurtis166/SPNKr/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/acurtis166/SPNKr/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/acurtis166/SPNKr/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/acurtis166/SPNKr/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/acurtis166/SPNKr/releases/tag/v0.1.0