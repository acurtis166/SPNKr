import json
from importlib import resources

_bytes = (resources.files("spnkr.film") / "medal_codes.json").read_bytes()
MEDALS: dict[int, str] = {int(k): v for k, v in json.loads(_bytes).items()}
"""Mapping of int encodings to their respective medal names."""
