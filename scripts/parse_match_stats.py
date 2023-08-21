"""Parse match stats from a directory of JSON files."""

import argparse
import json
from pathlib import Path

import pandas as pd

from spnkr.parsers.records import stats

PLAYER_FILE = "players.csv"
TEAM_FILE = "teams.csv"
MEDAL_FILE = "medals.csv"


def main(input_dir: Path, output_dir: Path) -> None:
    player_results = []
    team_results = []
    medal_results = []

    for i, file in enumerate(input_dir.glob("*.json")):
        print(f"Processing file number {i + 1:6}", end="\r")
        data = json.loads(file.read_bytes())
        player_results += stats.parse_player_core_stats(data)
        team_results += stats.parse_team_core_stats(data)
        medal_results += stats.parse_player_medals(data)

    player_df = pd.DataFrame(player_results)
    team_df = pd.DataFrame(team_results)
    medal_df = pd.DataFrame(medal_results)

    player_df.to_csv(output_dir / PLAYER_FILE, index=False)
    team_df.to_csv(output_dir / TEAM_FILE, index=False)
    medal_df.to_csv(output_dir / MEDAL_FILE, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "i", type=Path, help="Directory of JSON files to parse."
    )
    parser.add_argument("o", type=Path, help="Directory to write CSV results.")
    args = parser.parse_args()

    main(args.i, args.o)
