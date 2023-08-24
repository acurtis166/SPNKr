"""Parse match skills from a directory of JSON files."""

import argparse
import json
from pathlib import Path

import pandas as pd

from spnkr.parsers import records as rp


def main(input_dir: Path, output_path: Path) -> None:
    results = []

    # For repeat use, it would make sense to check which files have already been
    # processed and skip them. For now, we'll just process everything.
    for i, file in enumerate(input_dir.glob("*.json")):
        print(f"Processing file number {i + 1:6}", end="\r")
        data = json.loads(file.read_bytes())
        results += rp.parse_match_skill(file.stem, data)

    # Save the parsed records to files.
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "i", type=Path, help="Directory of JSON files to parse."
    )
    parser.add_argument("o", type=Path, help="File path to write CSV results.")
    args = parser.parse_args()
    assert args.i.is_dir()
    assert args.o.suffix == ".csv"

    main(args.i, args.o)
