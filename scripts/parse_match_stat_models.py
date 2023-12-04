"""Parse match stats from a directory of JSON files.

Use pydantic parsing to generate models from the JSON files. Nothing is done
with the models, but the script is useful for finding gaps in parsing logic.
"""

import argparse
import json
import logging
from pathlib import Path

import pydantic

from spnkr.models.stats import MatchStats


def main(input_dir: Path) -> None:
    logging.basicConfig(
        level=logging.ERROR,
        format="%(message)s",
        filename="parse_match_stat_models.log",
        filemode="w",
    )

    for i, file in enumerate(input_dir.glob("*.json")):
        print(f"Processing file number {i + 1:6}", end="\r")
        data = json.loads(file.read_bytes())
        try:
            MatchStats(**data)
        except pydantic.ValidationError:
            logging.exception(f"Error parsing match {file.stem}")
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "i", type=Path, help="Directory of JSON files to parse."
    )
    args = parser.parse_args()
    assert args.i.is_dir()

    main(args.i)
