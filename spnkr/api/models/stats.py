from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from enum import IntEnum
from uuid import UUID

from dateutil.parser import isoparse


def _parse_iso_duration(iso_duration: str) -> dt.timedelta:
    """Parse an ISO 8601 duration string to a timedelta object."""
    assert iso_duration.startswith("PT")
    kwargs = {}
    search = iso_duration[2:]
    seps = {
        "W": "weeks",
        "D": "days",
        "H": "hours",
        "M": "minutes",
        "S": "seconds",
    }
    for sep, attr in seps.items():
        parts = search.split(sep)
        if len(parts) > 1:
            kwargs[attr] = float(parts[0])
            search = parts[1]
    return dt.timedelta(**kwargs)


class Outcome(IntEnum):
    TIE = 1
    WIN = 2
    LOSS = 3
    DID_NOT_FINISH = 4


class GameVariantCategory(IntEnum):
    SLAYER = 6
    ATTRITION = 7
    ELIMINATION = 8
    FIESTA = 9
    STRONGHOLDS = 11
    BASTION = 12
    TOTAL_CONTROL = 14
    CTF = 15
    ASSAULT = 16
    EXTRACTION = 17
    ODDBALL = 18
    STOCKPILE = 19
    JUGGERNAUT = 20
    ESCORT = 23
    GUN_GAME = 24
    GRIFBALL = 25
    TEST_ENGINE = 32
    LAND_GRAB = 39


@dataclass(frozen=True, slots=True)
class MatchCountResponse:
    """Matches played by a player.

    Attributes:
        custom (int): Number of custom matches played.
        total (int): Total number of matches played.
        matchmade (int): Number of matchmade matches played.
        local (int): Number of local matches played.
    """

    custom: int
    total: int
    matchmade: int
    local: int

    @classmethod
    def from_dict(cls, data: dict) -> MatchCountResponse:
        """Create a MatchCountResponse from a dictionary."""
        custom = data["CustomMatchesPlayedCount"]
        total = data["MatchesPlayedCount"]
        matchmade = data["MatchmadeMatchesPlayedCount"]
        local = data["LocalMatchesPlayedCount"]
        return cls(custom, total, matchmade, local)


@dataclass(frozen=True, slots=True)
class Asset:
    """A game asset, such as a map, mode, or playlist.

    Attributes:
        id (uuid.UUID): The ID of the asset.
        version_id (uuid.UUID): The version ID of the asset.
    """

    id: UUID
    version_id: UUID

    @classmethod
    def from_dict(cls, data: dict) -> Asset:
        """Create an Asset from a dictionary."""
        id = UUID(data["AssetId"])
        version_id = UUID(data["VersionId"])
        return cls(id, version_id)


@dataclass(frozen=True, slots=True)
class MatchInfo:
    """Information about a match.

    Attributes:
        start (datetime.datetime): The start time of the match.
        end (datetime.datetime): The end time of the match.
        duration (datetime.timedelta): The duration of the match.
        category (GameVariantCategory): The game mode category of the
            match.
        map (Asset): The map the match was played on.
        mode (Asset): The mode played in the match.
        playlist (Asset | None): The playlist that the match was made in. This
            is None if the match was a custom or local match.
        season_id (str): The season ID of the match.
    """

    start: dt.datetime
    end: dt.datetime
    duration: dt.timedelta
    category: GameVariantCategory
    map: Asset
    mode: Asset
    playlist: Asset | None
    season_id: str

    @classmethod
    def from_dict(cls, data: dict) -> MatchInfo:
        """Create a MatchInfo object from a dictionary."""
        start = isoparse(data["StartTime"])
        end = isoparse(data["EndTime"])
        duration = _parse_iso_duration(data["Duration"])
        category = GameVariantCategory(data["GameVariantCategory"])
        map = Asset.from_dict(data["MapVariant"])
        mode = Asset.from_dict(data["UgcGameVariant"])
        playlist = None
        if data["Playlist"]:
            playlist = Asset.from_dict(data["Playlist"])
        season = data["SeasonId"]
        return cls(start, end, duration, category, map, mode, playlist, season)


@dataclass(frozen=True, slots=True)
class MatchHistoryRecord:
    """A record of a match played by a player.

    Attributes:
        id (uuid.UUID): The ID of the match.
        info (MatchInfo): Information about the match.
        last_team_id (int): The ID of the team the player was on at the end of
            the match.
        outcome (Outcome): The outcome of the match for the player (win,
            loss, tie, or did not finish).
    """

    id: UUID
    info: MatchInfo
    last_team_id: int
    outcome: Outcome
    rank: int
    present_at_end_of_match: bool

    @classmethod
    def from_dict(cls, data: dict) -> MatchHistoryRecord:
        """Create a MatchHistoryRecord from a dictionary."""
        id = UUID(data["MatchId"])
        info = MatchInfo.from_dict(data["MatchInfo"])
        last_team_id = data["LastTeamId"]
        outcome = Outcome(data["Outcome"])
        rank = data["Rank"]
        present_at_end = data["PresentAtEndOfMatch"]
        return cls(id, info, last_team_id, outcome, rank, present_at_end)


@dataclass(frozen=True, slots=True)
class MatchHistoryResponse:
    """A response containing a list of matches played by a player.

    The matches are ordered by start time, with the most recent match first.

    Attributes:
        raw (dict): The raw response data.
        start (int): The index of the first match in the response.
        count (int): The number of matches requested.
        result_count (int): The number of matches returned.
        matches (list[MatchHistoryRecord]): The list of matches.
    """

    raw: dict
    start: int
    count: int
    result_count: int
    matches: list[MatchHistoryRecord]

    @classmethod
    def from_dict(cls, data: dict) -> MatchHistoryResponse:
        """Create a MatchHistoryResponse from a dictionary."""
        raw = data
        start: int = data["Start"]
        count: int = data["Count"]
        result_count: int = data["ResultCount"]
        matches = [MatchHistoryRecord.from_dict(x) for x in data["Results"]]
        return cls(raw, start, count, result_count, matches)


@dataclass(frozen=True, slots=True)
class CoreStats:
    """Stats that are common to all game modes.

    Attributes:
        score (int): The player's score related to the objective of the game.
        personal_score (int): The player's personal score, determined by the
            player's performance (e.g. kills, assists, medals, etc.).
        kills (int): The number of kills the player had.
        deaths (int): The number of deaths the player had.
        assists (int): The number of assists the player had.
        kda (float): The player's kills-deaths-assists metric. This is
            calculated as (kills + (assists / 3)) - deaths.
        suicides (int): The number of times the player killed themselves.
        betrayals (int): The number of times the player killed a teammate.
        average_life_duration (datetime.timedelta): The average duration of
            the player's life.
        grenade_kills (int): The number of kills the player had with grenades.
        headshot_kills (int): The number of kills the player had with headshots.
        melee_kills (int): The number of kills the player had with melee
            attacks.
        power_weapon_kills (int): The number of kills the player had with
            power weapons.
        shots_fired (int): The number of shots the player fired.
        shots_hit (int): The number of shots the player hit.
        accuracy (float): The player's accuracy. This is calculated as
            shots_hit / shots_fired * 100.
        damage_dealt (int): The amount of damage the player dealt.
        damage_taken (int): The amount of damage the player took.
        callout_assists (int): The number of times the player assisted a
            teammate with a ping/mark.
        vehicle_destroys (int): The number of vehicles the player destroyed.
        driver_assists (int): The number of times the player assisted a
            teammate by driving a vehicle.
        hijacks (int): The number of times the player hijacked a vehicle.
        emp_assists (int): The number of times the player assisted a teammate
            by EMPing an enemy.
        max_killing_spree (int): The longest killing spree the player had.
        medals (dict[int, int]): A dictionary containing medal counts, keyed by
            medal ID.
    """

    score: int
    personal_score: int
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
    medals: dict[int, int]

    @classmethod
    def from_dict(cls, data: dict) -> CoreStats:
        """Create a CoreStats object from a dictionary."""
        return cls(
            score=data["Score"],
            personal_score=data["PersonalScore"],
            kills=data["Kills"],
            deaths=data["Deaths"],
            assists=data["Assists"],
            kda=data["KDA"],
            suicides=data["Suicides"],
            betrayals=data["Betrayals"],
            average_life_duration=_parse_iso_duration(
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
            medals={x["NameId"]: x["Count"] for x in data["Medals"]},
        )


@dataclass(frozen=True, slots=True)
class BombStats:
    """Stats related to bomb game modes.

    Attributes:
        carriers_killed (int): The number of times the player killed a bomb
            carrier.
        defusals (int): The number of times the player defused a bomb.
        defusers_killed (int): The number of times the player killed a bomb
            defuser.
        detonations (int): The number of times the player detonated a bomb.
        pick_ups (int): The number of times the player picked up a bomb.
        plants (int): The number of times the player planted a bomb.
        returns (int): The number of times the player returned a bomb.
        kills_as_carrier (int): The number of times the player killed an enemy
            while carrying a bomb.
        time_as_carrier (datetime.timedelta): The total amount of time the
            player carried a bomb.
    """

    carriers_killed: int
    defusals: int
    defusers_killed: int
    detonations: int
    pick_ups: int
    plants: int
    returns: int
    kills_as_carrier: int
    time_as_carrier: dt.timedelta

    @classmethod
    def from_dict(cls, data: dict) -> BombStats:
        """Create a BombStats object from a dictionary."""
        return cls(
            carriers_killed=data["BombCarriersKilled"],
            defusals=data["BombDefusals"],
            defusers_killed=data["BombDefusersKilled"],
            detonations=data["BombDetonations"],
            pick_ups=data["BombPickUps"],
            plants=data["BombPlants"],
            returns=data["BombReturns"],
            kills_as_carrier=data["KillsAsBombCarrier"],
            time_as_carrier=_parse_iso_duration(data["TimeAsBombCarrier"]),
        )


@dataclass(frozen=True, slots=True)
class CaptureTheFlagStats:
    """Stats related to capture the flag game modes.

    Attributes:
        capture_assists (int): The number of times the player assisted a
            teammate in capturing a flag.
        captures (int): The number of times the player captured a flag.
        carriers_killed (int): The number of times the player killed a flag
            carrier.
        grabs (int): The number of times the player grabbed a flag.
        returners_killed (int): The number of times the player killed a flag
            returner.
        returns (int): The number of times the player returned a flag.
        secures (int): The number of times the player secured a flag.
        steals (int): The number of times the player stole a flag.
        kills_as_carrier (int): The number of times the player killed an enemy
            while carrying a flag.
        kills_as_returner (int): The number of times the player killed an enemy
            while returning a flag.
        time_as_carrier (datetime.timedelta): The total amount of time the
            player carried a flag.
    """

    capture_assists: int
    captures: int
    carriers_killed: int
    grabs: int
    returners_killed: int
    returns: int
    secures: int
    steals: int
    kills_as_carrier: int
    kills_as_returner: int
    time_as_carrier: dt.timedelta

    @classmethod
    def from_dict(cls, data: dict) -> CaptureTheFlagStats:
        """Create a CaptureTheFlagStats object from a dictionary."""
        return cls(
            capture_assists=data["FlagCaptureAssists"],
            captures=data["FlagCaptures"],
            carriers_killed=data["FlagCarriersKilled"],
            grabs=data["FlagGrabs"],
            returners_killed=data["FlagReturnersKilled"],
            returns=data["FlagReturns"],
            secures=data["FlagSecures"],
            steals=data["FlagSteals"],
            kills_as_carrier=data["KillsAsFlagCarrier"],
            kills_as_returner=data["KillsAsFlagReturner"],
            time_as_carrier=_parse_iso_duration(data["TimeAsFlagCarrier"]),
        )


@dataclass(frozen=True, slots=True)
class EliminationStats:
    """Stats related to elimination game modes.

    Attributes:
        allies_revived (int): The number of times the player revived an ally.
        elimination_assists (int): The number of times the player assisted an
            elimination.
        eliminations (int): The number of times the player eliminated an enemy.
        enemy_revives_denied (int): The number of times the player denied an
            enemy revive.
        executions (int): The number of times the player executed an enemy.
        kills_as_last_player_standing (int): The number of times the player
            killed an enemy while they were the last player standing for their
            team.
        last_players_standing_killed (int): The number of times the player
            killed the last player standing on the enemy team.
        rounds_survived (int): The number of rounds the player survived.
        times_revived_by_ally (int): The number of times the player was revived
            by an ally.
        lives_remaining (int): The number of lives the player had remaining at
            the end of the game.
        elimination_order (int): The order in which the player was eliminated.
    """

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
        """Create an EliminationStats object from a dictionary."""
        return cls(
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


@dataclass(frozen=True, slots=True)
class ExtractionStats:
    """Stats related to extraction game modes."""

    conversions_completed: int
    conversions_denied: int
    initiations_completed: int
    initiations_denied: int
    successful_extractions: int

    @classmethod
    def from_dict(cls, data: dict) -> ExtractionStats:
        """Create an ExtractionStats object from a dictionary."""
        return cls(
            conversions_completed=data["ExtractionConversionsCompleted"],
            conversions_denied=data["ExtractionConversionsDenied"],
            initiations_completed=data["ExtractionInitiationsCompleted"],
            initiations_denied=data["ExtractionInitiationsDenied"],
            successful_extractions=data["SuccessfulExtractions"],
        )


class InfectionStats:
    """Stats related to infection game modes. Infection hasn't released yet."""

    pass


@dataclass(frozen=True, slots=True)
class OddballStats:
    """Stats related to oddball game modes.

    Attributes:
        kills_as_carrier (int): The number of times the player killed an enemy
            while carrying the oddball.
        longest_carry (datetime.timedelta): The longest amount of time the
            player carried the oddball.
        carriers_killed (int): The number of times the player killed an enemy
            that was carrying the oddball.
        skull_grabs (int): The number of times the player grabbed the oddball.
        time_as_carrier (datetime.timedelta): The total amount of time the
            player carried the oddball.
        scoring_ticks (int): The number of points the player scored by
            carrying the oddball.
    """

    kills_as_carrier: int
    longest_carry: dt.timedelta
    carriers_killed: int
    skull_grabs: int
    time_as_carrier: dt.timedelta
    scoring_ticks: int

    @classmethod
    def from_dict(cls, data: dict) -> OddballStats:
        """Create an OddballStats object from a dictionary."""
        return cls(
            kills_as_carrier=data["KillsAsSkullCarrier"],
            longest_carry=_parse_iso_duration(
                data["LongestTimeAsSkullCarrier"]
            ),
            carriers_killed=data["SkullCarriersKilled"],
            skull_grabs=data["SkullGrabs"],
            time_as_carrier=_parse_iso_duration(data["TimeAsSkullCarrier"]),
            scoring_ticks=data["SkullScoringTicks"],
        )


@dataclass(frozen=True, slots=True)
class ZonesStats:
    """Stats related to zones game modes, such as strongholds or KOTH.

    Attributes:
        captures (int): The number of times the player captured a zone.
        defensive_kills (int): The number of times the player killed an enemy
            while defending a zone.
        offensive_kills (int): The number of times the player killed an enemy
            while attacking a zone.
        secures (int): The number of times the player secured a zone.
        occupation_time (datetime.timedelta): The total amount of time the
            player occupied a zone.
        scoring_ticks (int): The number of points the player scored by
            occupying a zone.
    """

    captures: int
    defensive_kills: int
    offensive_kills: int
    secures: int
    occupation_time: dt.timedelta
    scoring_ticks: int

    @classmethod
    def from_dict(cls, data: dict) -> ZonesStats:
        """Create a ZonesStats object from a dictionary."""
        return cls(
            captures=data["StrongholdCaptures"],
            defensive_kills=data["StrongholdDefensiveKills"],
            offensive_kills=data["StrongholdOffensiveKills"],
            secures=data["StrongholdSecures"],
            occupation_time=_parse_iso_duration(
                data["StrongholdOccupationTime"]
            ),
            scoring_ticks=data["StrongholdScoringTicks"],
        )


@dataclass(frozen=True, slots=True)
class StockpileStats:
    """Stats related to stockpile game modes.

    Attributes:
        kills_as_carrier (int): The number of times the player killed an enemy
            while carrying a power seed.
        deposited (int): The number of power seeds the player deposited.
        stolen (int): The number of power seeds the player stole.
        carriers_killed (int): The number of times the player killed an enemy
            that was carrying a power seed.
        time_as_carrier (datetime.timedelta): The total amount of time the
            player carried a power seed.
        time_as_driver (datetime.timedelta): The total amount of time the
            player drove a power seed.
    """

    kills_as_carrier: int
    deposited: int
    stolen: int
    carriers_killed: int
    time_as_carrier: dt.timedelta
    time_as_driver: dt.timedelta

    @classmethod
    def from_dict(cls, data: dict) -> StockpileStats:
        """Create a StockpileStats object from a dictionary."""
        return cls(
            kills_as_carrier=data["KillsAsPowerSeedCarrier"],
            deposited=data["PowerSeedsDeposited"],
            stolen=data["PowerSeedsStolen"],
            carriers_killed=data["PowerSeedCarriersKilled"],
            time_as_carrier=_parse_iso_duration(data["TimeAsPowerSeedCarrier"]),
            time_as_driver=_parse_iso_duration(data["TimeAsPowerSeedDriver"]),
        )


@dataclass(frozen=True, slots=True)
class Stats:
    """Stats for a player or team.

    Core stats are available for all game modes. Stats for specific game modes
    are available when the match is of that game mode. All remaining stats are
    None.

    Attributes:
        core (CoreStats): General stats common to all game modes.
        bomb (BombStats | None): Stats related to bomb game modes.
        ctf (CaptureTheFlagStats | None): Stats related to capture the flag
            game modes.
        elimination (EliminationStats | None): Stats related to elimination
            game modes.
        extraction (ExtractionStats | None): Stats related to extraction game
            modes.
        infection (InfectionStats | None): Stats related to infection game
            modes.
        oddball (OddballStats | None): Stats related to oddball game modes.
        zones (ZonesStats | None): Stats related to zones game modes.
        stockpile (StockpileStats | None): Stats related to stockpile game
            modes.
    """

    core: CoreStats
    bomb: BombStats | None
    ctf: CaptureTheFlagStats | None
    elimination: EliminationStats | None
    extraction: ExtractionStats | None
    infection: InfectionStats | None
    oddball: OddballStats | None
    zones: ZonesStats | None
    stockpile: StockpileStats | None

    @classmethod
    def from_dict(cls, data: dict) -> Stats:
        """Create a Stats object from a dictionary."""
        core = CoreStats.from_dict(data["CoreStats"])
        bomb = None
        ctf = None
        elim = None
        extract = None
        infect = None
        ball = None
        zone = None
        stock = None

        if data["BombStats"]:
            bomb = BombStats.from_dict(data["BombStats"])
        elif data["CaptureTheFlagStats"]:
            ctf = CaptureTheFlagStats.from_dict(data["CaptureTheFlagStats"])
        elif data["EliminationStats"]:
            elim = EliminationStats.from_dict(data["EliminationStats"])
        elif data["ExtractionStats"]:
            extract = ExtractionStats.from_dict(data["ExtractionStats"])
        elif data["InfectionStats"]:
            infect = InfectionStats(**data["InfectionStats"])
        elif data["OddballStats"]:
            ball = OddballStats.from_dict(data["OddballStats"])
        elif data["ZonesStats"]:
            zone = ZonesStats.from_dict(data["ZonesStats"])
        elif data["StockpileStats"]:
            stock = StockpileStats.from_dict(data["StockpileStats"])

        return cls(core, bomb, ctf, elim, extract, infect, ball, zone, stock)


@dataclass(frozen=True, slots=True)
class Team:
    """A team in a match.

    Attributes:
        id (int): The ID of the team.
        outcome (Outcome): The outcome of the match from the perspective
            of the team (win, loss, tie, did not finish).
        rank (int): The rank of the team.
        stats (Stats): The aggregate stats for the team.
    """

    id: int
    outcome: Outcome
    rank: int
    stats: Stats

    @classmethod
    def from_dict(cls, data: dict) -> Team:
        """Create a Team object from a dictionary."""
        id = data["TeamId"]
        outcome = Outcome(data["Outcome"])
        rank = data["Rank"]
        stats = Stats.from_dict(data["Stats"])
        return cls(id, outcome, rank, stats)


@dataclass(frozen=True, slots=True)
class ParticipationInfo:
    """Information about a player's participation in a match.

    Attributes:
        first_joined_time (datetime.datetime): The time the player first
            joined the match.
        last_leave_time (datetime.datetime | None): The time the player last
            left the match. None if the player finished the match.
        present_at_beginning (bool): Whether the player was present at the
            beginning of the match.
        joined_in_progress (bool): Whether the player joined the match after
            the match had started.
        left_in_progress (bool): Whether the player left the match before it
            had finished.
        present_at_completion (bool): Whether the player was present at the
            end of the match.
        time_played (datetime.timedelta): The total amount of time the player
            was present in the match.
    """

    first_joined_time: dt.datetime
    last_leave_time: dt.datetime | None
    present_at_beginning: bool
    joined_in_progress: bool
    left_in_progress: bool
    present_at_completion: bool
    time_played: dt.timedelta

    @classmethod
    def from_dict(cls, data: dict) -> ParticipationInfo:
        """Create a ParticipationInfo object from a dictionary."""
        last_leave_time = None
        if data["LastLeaveTime"]:
            last_leave_time = isoparse(data["LastLeaveTime"])
        return cls(
            first_joined_time=isoparse(data["FirstJoinedTime"]),
            last_leave_time=last_leave_time,
            present_at_beginning=data["PresentAtBeginning"],
            joined_in_progress=data["JoinedInProgress"],
            left_in_progress=data["LeftInProgress"],
            present_at_completion=data["PresentAtCompletion"],
            time_played=_parse_iso_duration(data["TimePlayed"]),
        )


@dataclass(frozen=True, slots=True)
class Player:
    """A player in a match.

    Attributes:
        xuid (str): The XUID of the player, including the xuid() wrapper.
        is_human (bool): Whether the player is a human.
        is_bot (bool): Whether the player is a bot.
        bot_difficulty (int | None): The difficulty of the bot. None if the
            player is not a bot.
        last_team_id (int): The ID of the team the player was on at the end
            of the match.
        outcome (Outcome): The outcome of the match from the perspective
            of the player (win, loss, tie, did not finish).
        rank (int): The rank of the player.
        participation (ParticipationInfo): Information about the player's
            participation in the match.
        stats (dict[int, Stats]): The stats for the player for each team
            they were on. The key is the team ID. If the player was only on one
            team or if only the last team they were on is relevant, use the
            `last_team_stats` attribute to directly access the stats for that
            team association.
        last_team_stats (Stats): The stats for the player for the last team
            they were on. If the player was only on one team, this is simply
            a convenience attribute for accessing the player's stats.
    """

    xuid: str
    is_human: bool
    is_bot: bool
    bot_difficulty: int | None
    last_team_id: int
    outcome: Outcome
    rank: int
    participation: ParticipationInfo
    stats: dict[int, Stats]
    last_team_stats: Stats

    @classmethod
    def from_dict(cls, data: dict) -> Player:
        """Create a Player object from a dictionary."""
        bot_difficulty: int | None = None
        if data["BotAttributes"]:
            bot_difficulty = data["BotAttributes"]["Difficulty"]
        stats = {}
        for pts in data["PlayerTeamStats"]:
            stats[pts["TeamId"]] = Stats.from_dict(pts["Stats"])
        return cls(
            xuid=data["PlayerId"],
            is_human=data["PlayerType"] == 1,
            is_bot=data["PlayerType"] == 2,
            bot_difficulty=bot_difficulty,
            last_team_id=data["LastTeamId"],
            outcome=Outcome(data["Outcome"]),
            rank=data["Rank"],
            participation=ParticipationInfo.from_dict(
                data["ParticipationInfo"]
            ),
            stats=stats,
            last_team_stats=stats[data["LastTeamId"]],
        )


@dataclass(frozen=True, slots=True)
class MatchStatsResponse:
    """The stats for a match.

    Attributes:
        raw (dict): The raw data returned by the API.
        id (uuid.UUID): The UUID of the match.
        info (MatchInfo): Information about the match.
        teams (list[Team]): The teams in the match.
        players (list[Player]): The players in the match.
    """

    raw: dict
    id: UUID
    info: MatchInfo
    teams: list[Team]
    players: list[Player]

    @classmethod
    def from_dict(cls, data: dict) -> MatchStatsResponse:
        """Create a MatchStats object from a dictionary."""
        raw = data
        id = UUID(data["MatchId"])
        info = MatchInfo.from_dict(data["MatchInfo"])
        teams = [Team.from_dict(x) for x in data["Teams"]]
        players = [Player.from_dict(x) for x in data["Players"]]
        return cls(raw, id, info, teams, players)
