# Changelog

## [Unreleased]

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

First release.

[unreleased]: https://github.com/acurtis166/SPNKr/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/acurtis166/SPNKr/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/acurtis166/SPNKr/releases/tag/v0.1.0