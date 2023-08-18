from typing import Any

from ..refdata import SkillResultCode, Team


def parse_match_skill(match_skill: dict[str, Any]) -> list[dict[str, Any]]:
    return [_parse_match_skill_value(msv) for msv in match_skill["Value"]]


def _parse_match_skill_value(
    match_skill_value: dict[str, Any]
) -> dict[str, Any]:
    msv = match_skill_value
    result = msv["Result"]
    return {
        "xuid": msv["Id"],
        "result_code": SkillResultCode(result["ResultCode"]),
        "team_id": Team(result["TeamId"]),
        "team_mmr": result["TeamMmr"],
        "pre_match_csr": result["RankRecap"]["PreMatchCsr"]["Value"],
        "post_match_csr": result["RankRecap"]["PostMatchCsr"]["Value"],
        "actual_kills": result["StatPerformances"]["Kills"]["Count"],
        "expected_kills": result["StatPerformances"]["Kills"]["Expected"],
        "actual_deaths": result["StatPerformances"]["Deaths"]["Count"],
        "expected_deaths": result["StatPerformances"]["Deaths"]["Expected"],
    }


def parse_playlist_csr(playlist_csr: dict[str, Any]) -> list[dict[str, Any]]:
    return [_parse_playlist_csr_value(pcv) for pcv in playlist_csr["Value"]]


def _parse_playlist_csr_value(
    playlist_csr_value: dict[str, Any]
) -> dict[str, Any]:
    pcv = playlist_csr_value
    result = pcv["Result"]
    return {
        "xuid": pcv["Id"],
        "result_code": SkillResultCode(result["ResultCode"]),
        "current_csr": result["Current"]["Value"],
        "season_max_csr": result["SeasonMax"]["Value"],
        "all_time_max_csr": result["AllTimeMax"]["Value"],
    }
