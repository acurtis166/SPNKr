from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from uuid import UUID

from spnkr.api import enums
from spnkr.parsers import parse_iso_datetime, parse_iso_duration


@dataclass(frozen=True)
class MatchCount:
    custom_matches_played_count: int
    matches_played_count: int
    matchmade_matches_played_count: int
    local_matches_played_count: int

    @classmethod
    def from_dict(cls, data: dict) -> MatchCount:
        return MatchCount(
            custom_matches_played_count=data["CustomMatchesPlayedCount"],
            matches_played_count=data["MatchesPlayedCount"],
            matchmade_matches_played_count=data["MatchmadeMatchesPlayedCount"],
            local_matches_played_count=data["LocalMatchesPlayedCount"],
        )


@dataclass(frozen=True)
class AssetStub:
    asset_kind: enums.AssetKind
    asset_id: UUID
    version_id: UUID

    @classmethod
    def from_dict(cls, data: dict) -> AssetStub:
        return AssetStub(
            asset_kind=enums.AssetKind(data["AssetKind"]),
            asset_id=UUID(data["AssetId"]),
            version_id=UUID(data["VersionId"]),
        )


@dataclass(frozen=True)
class MatchInfo:
    start_time: dt.datetime
    end_time: dt.datetime
    duration: dt.timedelta
    lifecycle_mode: enums.LifecycleMode
    game_variant_category: enums.GameVariantCategory
    level_id: UUID
    map_variant: AssetStub
    ugc_game_variant: AssetStub
    clearance_id: UUID
    playlist: AssetStub | None
    playlist_experience: enums.PlaylistExperience | None
    playlist_map_mode_pair: AssetStub | None
    season_id: str
    playable_duration: dt.timedelta
    teams_enabled: bool
    team_scoring_enabled: bool

    @classmethod
    def from_dict(cls, data: dict) -> MatchInfo:
        return MatchInfo(
            start_time=parse_iso_datetime(data["StartTime"]),
            end_time=parse_iso_datetime(data["EndTime"]),
            duration=parse_iso_duration(data["Duration"]),
            lifecycle_mode=enums.LifecycleMode(data["LifecycleMode"]),
            game_variant_category=enums.GameVariantCategory(
                data["GameVariantCategory"]
            ),
            level_id=UUID(data["LevelId"]),
            map_variant=AssetStub.from_dict(data["MapVariant"]),
            ugc_game_variant=AssetStub.from_dict(data["UgcGameVariant"]),
            clearance_id=UUID(data["ClearanceId"]),
            playlist=AssetStub.from_dict(data["Playlist"])
            if data["Playlist"]
            else None,
            playlist_experience=enums.PlaylistExperience(
                data["PlaylistExperience"]
            )
            if data["PlaylistExperience"]
            else None,
            playlist_map_mode_pair=AssetStub.from_dict(
                data["PlaylistMapModePair"]
            )
            if data["PlaylistMapModePair"]
            else None,
            season_id=data["SeasonId"],
            playable_duration=parse_iso_duration(data["PlayableDuration"]),
            teams_enabled=data["TeamsEnabled"],
            team_scoring_enabled=data["TeamScoringEnabled"],
        )


@dataclass(frozen=True)
class PlayerMatchHistoryRecord:
    match_id: UUID
    match_info: MatchInfo
    last_team_id: int
    outcome: enums.Outcome
    rank: int
    present_at_end_of_match: bool

    @classmethod
    def from_dict(cls, data: dict) -> PlayerMatchHistoryRecord:
        return PlayerMatchHistoryRecord(
            match_id=UUID(data["MatchId"]),
            match_info=MatchInfo.from_dict(data["MatchInfo"]),
            last_team_id=data["LastTeamId"],
            outcome=enums.Outcome(data["Outcome"]),
            rank=data["Rank"],
            present_at_end_of_match=data["PresentAtEndOfMatch"],
        )


@dataclass(frozen=True)
class Links:
    pass


@dataclass(frozen=True)
class MatchHistoryResponse:
    start: int
    count: int
    result_count: int
    results: list[PlayerMatchHistoryRecord]
    links: Links

    @classmethod
    def from_dict(cls, data: dict) -> MatchHistoryResponse:
        return MatchHistoryResponse(
            start=data["Start"],
            count=data["Count"],
            result_count=data["ResultCount"],
            results=[
                PlayerMatchHistoryRecord.from_dict(x) for x in data["Results"]
            ],
            links=Links(**data["Links"]),
        )


@dataclass(frozen=True)
class MatchResultPersonalScoreStats:
    name_id: int
    count: int
    total_personal_score_awarded: int

    @classmethod
    def from_dict(cls, data: dict) -> MatchResultPersonalScoreStats:
        return MatchResultPersonalScoreStats(
            name_id=data["NameId"],
            count=data["Count"],
            total_personal_score_awarded=data["TotalPersonalScoreAwarded"],
        )


@dataclass(frozen=True)
class MatchResultMedalStats:
    name_id: int
    count: int
    total_personal_score_awarded: int

    @classmethod
    def from_dict(cls, data: dict) -> MatchResultMedalStats:
        return MatchResultMedalStats(
            name_id=data["NameId"],
            count=data["Count"],
            total_personal_score_awarded=data["TotalPersonalScoreAwarded"],
        )


@dataclass(frozen=True)
class CoreStats:
    score: int
    personal_score: int
    rounds_won: int
    rounds_lost: int
    rounds_tied: int
    kills: int
    deaths: int
    assists: int
    kda: float
    suicides: int
    betrayals: int
    average_life_duration: dt.timedelta
    grenade_kills: int
    headshot_kills: int
    melee_kills: int
    power_weapon_kills: int
    shots_fired: int
    shots_hit: int
    accuracy: float
    damage_dealt: int
    damage_taken: int
    callout_assists: int
    vehicle_destroys: int
    driver_assists: int
    hijacks: int
    emp_assists: int
    max_killing_spree: int
    medals: list[MatchResultMedalStats]
    personal_scores: list[MatchResultPersonalScoreStats]
    deprecated_damage_dealt: float
    deprecated_damage_taken: float
    spawns: int

    @classmethod
    def from_dict(cls, data: dict) -> CoreStats:
        return CoreStats(
            score=data["Score"],
            personal_score=data["PersonalScore"],
            rounds_won=data["RoundsWon"],
            rounds_lost=data["RoundsLost"],
            rounds_tied=data["RoundsTied"],
            kills=data["Kills"],
            deaths=data["Deaths"],
            assists=data["Assists"],
            kda=data["KDA"],
            suicides=data["Suicides"],
            betrayals=data["Betrayals"],
            average_life_duration=parse_iso_duration(
                data["AverageLifeDuration"]
            ),
            grenade_kills=data["GrenadeKills"],
            headshot_kills=data["HeadshotKills"],
            melee_kills=data["MeleeKills"],
            power_weapon_kills=data["PowerWeaponKills"],
            shots_fired=data["ShotsFired"],
            shots_hit=data["ShotsHit"],
            accuracy=data["Accuracy"],
            damage_dealt=data["DamageDealt"],
            damage_taken=data["DamageTaken"],
            callout_assists=data["CalloutAssists"],
            vehicle_destroys=data["VehicleDestroys"],
            driver_assists=data["DriverAssists"],
            hijacks=data["Hijacks"],
            emp_assists=data["EmpAssists"],
            max_killing_spree=data["MaxKillingSpree"],
            medals=[MatchResultMedalStats.from_dict(x) for x in data["Medals"]],
            personal_scores=[
                MatchResultPersonalScoreStats.from_dict(x)
                for x in data["PersonalScores"]
            ],
            deprecated_damage_dealt=data["DeprecatedDamageDealt"],
            deprecated_damage_taken=data["DeprecatedDamageTaken"],
            spawns=data["Spawns"],
        )


@dataclass(frozen=True)
class BombStats:
    bomb_carriers_killed: int
    bomb_defusals: int
    bomb_defusers_killed: int
    bomb_detonations: int
    bomb_pick_ups: int
    bomb_plants: int
    bomb_returns: int
    kills_as_bomb_carrier: int
    time_as_bomb_carrier: dt.timedelta

    @classmethod
    def from_dict(cls, data: dict) -> BombStats:
        return BombStats(
            bomb_carriers_killed=data["BombCarriersKilled"],
            bomb_defusals=data["BombDefusals"],
            bomb_defusers_killed=data["BombDefusersKilled"],
            bomb_detonations=data["BombDetonations"],
            bomb_pick_ups=data["BombPickUps"],
            bomb_plants=data["BombPlants"],
            bomb_returns=data["BombReturns"],
            kills_as_bomb_carrier=data["KillsAsBombCarrier"],
            time_as_bomb_carrier=parse_iso_duration(data["TimeAsBombCarrier"]),
        )


@dataclass(frozen=True)
class CaptureTheFlagStats:
    flag_capture_assists: int
    flag_captures: int
    flag_carriers_killed: int
    flag_grabs: int
    flag_returners_killed: int
    flag_returns: int
    flag_secures: int
    flag_steals: int
    kills_as_flag_carrier: int
    kills_as_flag_returner: int
    time_as_flag_carrier: dt.timedelta

    @classmethod
    def from_dict(cls, data: dict) -> CaptureTheFlagStats:
        return CaptureTheFlagStats(
            flag_capture_assists=data["FlagCaptureAssists"],
            flag_captures=data["FlagCaptures"],
            flag_carriers_killed=data["FlagCarriersKilled"],
            flag_grabs=data["FlagGrabs"],
            flag_returners_killed=data["FlagReturnersKilled"],
            flag_returns=data["FlagReturns"],
            flag_secures=data["FlagSecures"],
            flag_steals=data["FlagSteals"],
            kills_as_flag_carrier=data["KillsAsFlagCarrier"],
            kills_as_flag_returner=data["KillsAsFlagReturner"],
            time_as_flag_carrier=parse_iso_duration(data["TimeAsFlagCarrier"]),
        )


@dataclass(frozen=True)
class EliminationStats:
    allies_revived: int
    elimination_assists: int
    eliminations: int
    enemy_revives_denied: int
    executions: int
    kills_as_last_player_standing: int
    last_players_standing_killed: int
    rounds_survived: int
    times_revived_by_ally: int
    lives_remaining: int | None
    elimination_order: int

    @classmethod
    def from_dict(cls, data: dict) -> EliminationStats:
        return EliminationStats(
            allies_revived=data["AlliesRevived"],
            elimination_assists=data["EliminationAssists"],
            eliminations=data["Eliminations"],
            enemy_revives_denied=data["EnemyRevivesDenied"],
            executions=data["Executions"],
            kills_as_last_player_standing=data["KillsAsLastPlayerStanding"],
            last_players_standing_killed=data["LastPlayersStandingKilled"],
            rounds_survived=data["RoundsSurvived"],
            times_revived_by_ally=data["TimesRevivedByAlly"],
            lives_remaining=data["LivesRemaining"],
            elimination_order=data["EliminationOrder"],
        )


@dataclass(frozen=True)
class ExtractionStats:
    extraction_conversions_completed: int
    extraction_conversions_denied: int
    extraction_initiations_completed: int
    extraction_initiations_denied: int
    successful_extractions: int

    @classmethod
    def from_dict(cls, data: dict) -> ExtractionStats:
        return ExtractionStats(
            extraction_conversions_completed=data[
                "ExtractionConversionsCompleted"
            ],
            extraction_conversions_denied=data["ExtractionConversionsDenied"],
            extraction_initiations_completed=data[
                "ExtractionInitiationsCompleted"
            ],
            extraction_initiations_denied=data["ExtractionInitiationsDenied"],
            successful_extractions=data["SuccessfulExtractions"],
        )


@dataclass(frozen=True)
class InfectionStats:
    pass


@dataclass(frozen=True)
class OddballStats:
    kills_as_skull_carrier: int
    longest_time_as_skull_carrier: dt.timedelta
    skull_carriers_killed: int
    skull_grabs: int
    time_as_skull_carrier: dt.timedelta
    skull_scoring_ticks: int

    @classmethod
    def from_dict(cls, data: dict) -> OddballStats:
        return OddballStats(
            kills_as_skull_carrier=data["KillsAsSkullCarrier"],
            longest_time_as_skull_carrier=parse_iso_duration(
                data["LongestTimeAsSkullCarrier"]
            ),
            skull_carriers_killed=data["SkullCarriersKilled"],
            skull_grabs=data["SkullGrabs"],
            time_as_skull_carrier=parse_iso_duration(
                data["TimeAsSkullCarrier"]
            ),
            skull_scoring_ticks=data["SkullScoringTicks"],
        )


@dataclass(frozen=True)
class ZonesStats:
    stronghold_captures: int
    stronghold_defensive_kills: int
    stronghold_offensive_kills: int
    stronghold_secures: int
    stronghold_occupation_time: dt.timedelta
    stronghold_scoring_ticks: int

    @classmethod
    def from_dict(cls, data: dict) -> ZonesStats:
        return ZonesStats(
            stronghold_captures=data["StrongholdCaptures"],
            stronghold_defensive_kills=data["StrongholdDefensiveKills"],
            stronghold_offensive_kills=data["StrongholdOffensiveKills"],
            stronghold_secures=data["StrongholdSecures"],
            stronghold_occupation_time=parse_iso_duration(
                data["StrongholdOccupationTime"]
            ),
            stronghold_scoring_ticks=data["StrongholdScoringTicks"],
        )


@dataclass(frozen=True)
class StockpileStats:
    kills_as_power_seed_carrier: int
    power_seeds_deposited: int
    power_seeds_stolen: int
    power_seed_carriers_killed: int
    time_as_power_seed_carrier: dt.timedelta
    time_as_power_seed_driver: dt.timedelta

    @classmethod
    def from_dict(cls, data: dict) -> StockpileStats:
        return StockpileStats(
            kills_as_power_seed_carrier=data["KillsAsPowerSeedCarrier"],
            power_seeds_deposited=data["PowerSeedsDeposited"],
            power_seeds_stolen=data["PowerSeedsStolen"],
            power_seed_carriers_killed=data["PowerSeedCarriersKilled"],
            time_as_power_seed_carrier=parse_iso_duration(
                data["TimeAsPowerSeedCarrier"]
            ),
            time_as_power_seed_driver=parse_iso_duration(
                data["TimeAsPowerSeedDriver"]
            ),
        )


@dataclass(frozen=True)
class Stats:
    core_stats: CoreStats
    bomb_stats: BombStats | None
    capture_the_flag_stats: CaptureTheFlagStats | None
    elimination_stats: EliminationStats | None
    extraction_stats: ExtractionStats | None
    infection_stats: InfectionStats | None
    oddball_stats: OddballStats | None
    zones_stats: ZonesStats | None
    stockpile_stats: StockpileStats | None

    @classmethod
    def from_dict(cls, data: dict) -> Stats:
        bomb_stats = None
        if data["BombStats"]:
            bomb_stats = BombStats.from_dict(data["BombStats"])
        capture_the_flag_stats = None
        if data["CaptureTheFlagStats"]:
            capture_the_flag_stats = CaptureTheFlagStats.from_dict(
                data["CaptureTheFlagStats"]
            )
        elimination_stats = None
        if data["EliminationStats"]:
            elimination_stats = EliminationStats.from_dict(
                data["EliminationStats"]
            )
        extraction_stats = None
        if data["ExtractionStats"]:
            extraction_stats = ExtractionStats.from_dict(
                data["ExtractionStats"]
            )
        infection_stats = None
        if data["InfectionStats"]:
            infection_stats = InfectionStats(**data["InfectionStats"])
        oddball_stats = None
        if data["OddballStats"]:
            oddball_stats = OddballStats.from_dict(data["OddballStats"])
        zones_stats = None
        if data["ZonesStats"]:
            zones_stats = ZonesStats.from_dict(data["ZonesStats"])
        stockpile_stats = None
        if data["StockpileStats"]:
            stockpile_stats = StockpileStats.from_dict(data["StockpileStats"])
        return Stats(
            core_stats=CoreStats.from_dict(data["CoreStats"]),
            bomb_stats=bomb_stats,
            capture_the_flag_stats=capture_the_flag_stats,
            elimination_stats=elimination_stats,
            extraction_stats=extraction_stats,
            infection_stats=infection_stats,
            oddball_stats=oddball_stats,
            zones_stats=zones_stats,
            stockpile_stats=stockpile_stats,
        )


@dataclass(frozen=True)
class Team:
    team_id: int
    outcome: enums.Outcome
    rank: int
    stats: Stats

    @classmethod
    def from_dict(cls, data: dict) -> Team:
        return Team(
            team_id=data["TeamId"],
            outcome=enums.Outcome(data["Outcome"]),
            rank=data["Rank"],
            stats=Stats.from_dict(data["Stats"]),
        )


@dataclass(frozen=True)
class BotAttributes:
    difficulty: enums.BotDifficulty

    @classmethod
    def from_dict(cls, data: dict) -> BotAttributes:
        return BotAttributes(difficulty=enums.BotDifficulty(data["Difficulty"]))


@dataclass(frozen=True)
class ParticipationInfo:
    first_joined_time: dt.datetime
    last_leave_time: dt.datetime | None
    present_at_beginning: bool
    joined_in_progress: bool
    left_in_progress: bool
    present_at_completion: bool
    time_played: dt.timedelta
    confirmed_participation: bool | None

    @classmethod
    def from_dict(cls, data: dict) -> ParticipationInfo:
        return ParticipationInfo(
            first_joined_time=parse_iso_datetime(data["FirstJoinedTime"]),
            last_leave_time=parse_iso_datetime(data["LastLeaveTime"])
            if data["LastLeaveTime"]
            else None,
            present_at_beginning=data["PresentAtBeginning"],
            joined_in_progress=data["JoinedInProgress"],
            left_in_progress=data["LeftInProgress"],
            present_at_completion=data["PresentAtCompletion"],
            time_played=parse_iso_duration(data["TimePlayed"]),
            confirmed_participation=data["ConfirmedParticipation"]
            if data["ConfirmedParticipation"]
            else None,
        )


@dataclass(frozen=True)
class PlayerTeamStats:
    team_id: int
    stats: Stats

    @classmethod
    def from_dict(cls, data: dict) -> PlayerTeamStats:
        return PlayerTeamStats(
            team_id=data["TeamId"], stats=Stats.from_dict(data["Stats"])
        )


@dataclass(frozen=True)
class Player:
    player_id: str
    player_type: enums.PlayerType
    bot_attributes: BotAttributes | None
    last_team_id: int
    outcome: enums.Outcome
    rank: int
    participation_info: ParticipationInfo
    player_team_stats: list[PlayerTeamStats]

    @classmethod
    def from_dict(cls, data: dict) -> Player:
        return Player(
            player_id=data["PlayerId"],
            player_type=enums.PlayerType(data["PlayerType"]),
            bot_attributes=BotAttributes.from_dict(data["BotAttributes"])
            if data["BotAttributes"]
            else None,
            last_team_id=data["LastTeamId"],
            outcome=enums.Outcome(data["Outcome"]),
            rank=data["Rank"],
            participation_info=ParticipationInfo.from_dict(
                data["ParticipationInfo"]
            ),
            player_team_stats=[
                PlayerTeamStats.from_dict(x) for x in data["PlayerTeamStats"]
            ],
        )


@dataclass(frozen=True)
class MatchStats:
    match_id: UUID
    match_info: MatchInfo
    teams: list[Team]
    players: list[Player]

    @classmethod
    def from_dict(cls, data: dict) -> MatchStats:
        return MatchStats(
            match_id=UUID(data["MatchId"]),
            match_info=MatchInfo.from_dict(data["MatchInfo"]),
            teams=[Team.from_dict(x) for x in data["Teams"]],
            players=[Player.from_dict(x) for x in data["Players"]],
        )
