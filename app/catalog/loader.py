import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "catalog.json"

def load_catalog() -> dict:
    with open(CATALOG_PATH, "r") as f:
        return json.load(f)
