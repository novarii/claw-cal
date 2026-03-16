import os
import json
from pathlib import Path

DATA_DIR = Path(os.environ.get("CLAW_CAL_DIR", os.path.expanduser("~/.claw-cal")))
LOG_DIR = DATA_DIR / "log"
CACHE_DIR = DATA_DIR / "cache"
CONFIG_FILE = DATA_DIR / "config.json"
USER_PRESETS_FILE = DATA_DIR / "user_presets.json"

USDA_API_KEY = os.environ.get("USDA_API_KEY", "3QOIh2rPP64oUqe6gXy7VWIVdfncQG66gf5mXTAN")
USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

DINING_BASE_URL = "https://dining.rochester.edu/locations"
LOCATIONS = {
    "douglass": "douglass-dining",
    "doug": "douglass-dining",
    "pit": "the-pit",
    "blue-cactus": "blue-cactus",
    "bc": "blue-cactus",
}

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def ensure_dirs():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"target": 2000}


def save_config(cfg):
    ensure_dirs()
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
