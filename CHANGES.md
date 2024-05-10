# Changelog

## [Unreleased]

### Added

- Economy service, `get_player_customization` method, and associated response model.

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

[unreleased]: https://github.com/acurtis166/SPNKr/compare/v0.7.0...HEAD
[0.7.0]: https://github.com/acurtis166/SPNKr/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/acurtis166/SPNKr/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/acurtis166/SPNKr/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/acurtis166/SPNKr/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/acurtis166/SPNKr/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/acurtis166/SPNKr/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/acurtis166/SPNKr/releases/tag/v0.1.0