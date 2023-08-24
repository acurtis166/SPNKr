"""Parse match stats from a directory of JSON files."""

import argparse
import json
from pathlib import Path

import pandas as pd

from spnkr.parsers import records as rp

PLAYER_FILE = "players.csv"
TEAM_FILE = "teams.csv"
MEDAL_FILE = "medals.csv"


def main(input_dir: Path, output_dir: Path) -> None:
    player_results = []
    team_results = []
    medal_results = []

    # For repeat use, it would make sense to check which files have already been
    # processed and skip them. For now, we'll just process everything.
    for i, file in enumerate(input_dir.glob("*.json")):
        print(f"Processing file number {i + 1:6}", end="\r")
        data = json.loads(file.read_bytes())
        player_results += rp.parse_player_core_stats(data)
        team_results += rp.parse_team_core_stats(data)
        medal_results += rp.parse_player_medals(data)

    # Save the parsed records to files.
    player_df = pd.DataFrame(player_results)
    player_df.to_csv(output_dir / PLAYER_FILE, index=False)

    team_df = pd.DataFrame(team_results)
    team_df.to_csv(output_dir / TEAM_FILE, index=False)

    medal_df = pd.DataFrame(medal_results)
    medal_df.to_csv(output_dir / MEDAL_FILE, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "i", type=Path, help="Directory of JSON files to parse."
    )
    parser.add_argument("o", type=Path, help="Directory to write CSV results.")
    args = parser.parse_args()
    assert args.i.is_dir()
    assert args.o.is_dir()

    main(args.i, args.o)
