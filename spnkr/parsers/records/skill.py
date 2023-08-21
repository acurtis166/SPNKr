"""Parsing functions for the "skill" authority."""

from typing import Any, NamedTuple

from ..refdata import SkillResultCode


class PlayerSkillRecord(NamedTuple):
    """A player's skill data for a single match.

    Attributes:
        xuid: The player's Xbox Live ID.
        result_code: The status of the skill request.
        team_id: The player's team ID.
        team_mmr: The average MMR of the player's team.
        pre_match_csr: The player's CSR before the match.
        post_match_csr: The player's CSR after the match.
        actual_kills: The number of kills the player got in the match.
        expected_kills: The number of kills the player was expected to get in
            the match.
        actual_deaths: The number of deaths the player got in the match.
        expected_deaths: The number of deaths the player was expected to get
            in the match.
    """

    xuid: str
    result_code: SkillResultCode
    team_id: int
    team_mmr: int
    pre_match_csr: int
    post_match_csr: int
    actual_kills: int
    expected_kills: int
    actual_deaths: int
    expected_deaths: int


class PlaylistCsrRecord(NamedTuple):
    """A player's CSR summary for a playlist.

    Attributes:
        xuid: The player's Xbox Live ID.
        result_code: The status of the CSR request.
        current_csr: The player's current CSR in the playlist.
        season_max_csr: The player's highest CSR in the current season.
        all_time_max_csr: The player's highest CSR of all time.
    """

    xuid: str
    result_code: SkillResultCode
    current_csr: int
    season_max_csr: int
    all_time_max_csr: int


def parse_match_skill(match_skill: dict[str, Any]) -> list[PlayerSkillRecord]:
    """Parse a match skill response into a list of player skill records.

    Args:
        match_skill: The deserialized JSON from the client's `get_match_skill`
            method.

    Returns:
        A list of player skill records.
    """
    return [_parse_match_skill_value(msv) for msv in match_skill["Value"]]


def _parse_match_skill_value(
    match_skill_value: dict[str, Any]
) -> PlayerSkillRecord:
    """Parse a single player's skill from the `get_match_skill` response JSON."""
    msv = match_skill_value
    result = msv["Result"]
    return PlayerSkillRecord(
        xuid=msv["Id"],
        result_code=SkillResultCode(msv["ResultCode"]),
        team_id=result["TeamId"],
        team_mmr=result["TeamMmr"],
        pre_match_csr=result["RankRecap"]["PreMatchCsr"]["Value"],
        post_match_csr=result["RankRecap"]["PostMatchCsr"]["Value"],
        actual_kills=result["StatPerformances"]["Kills"]["Count"],
        expected_kills=result["StatPerformances"]["Kills"]["Expected"],
        actual_deaths=result["StatPerformances"]["Deaths"]["Count"],
        expected_deaths=result["StatPerformances"]["Deaths"]["Expected"],
    )


def parse_playlist_csr(playlist_csr: dict[str, Any]) -> list[PlaylistCsrRecord]:
    """Parse a playlist CSR response into a list of player-playlist CSR records.

    Args:
        playlist_csr: The deserialized JSON from the client's `get_playlist_csr`
            method.

    Returns:
        A list of player CSR summary records.
    """
    return [_parse_playlist_csr_value(pcv) for pcv in playlist_csr["Value"]]


def _parse_playlist_csr_value(
    playlist_csr_value: dict[str, Any]
) -> PlaylistCsrRecord:
    """Parse a single player's CSR from the `get_playlist_csr` response JSON."""
    pcv = playlist_csr_value
    result = pcv["Result"]
    return PlaylistCsrRecord(
        xuid=pcv["Id"],
        result_code=SkillResultCode(pcv["ResultCode"]),
        current_csr=result["Current"]["Value"],
        season_max_csr=result["SeasonMax"]["Value"],
        all_time_max_csr=result["AllTimeMax"]["Value"],
    )
