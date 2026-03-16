import json
import re
from datetime import date

import requests
from bs4 import BeautifulSoup

from .config import DINING_BASE_URL, CACHE_DIR, USER_AGENT, LOCATIONS, ensure_dirs


def _cache_path(location_slug: str, d: date) -> str:
    return CACHE_DIR / f"{location_slug}_{d.isoformat()}.json"


def scrape_menu(location: str, d: date | None = None) -> list[dict]:
    """Scrape menu items + nutrition from the dining site.
    Returns list of {name, station, calories, protein, fat, carbs, fiber, sodium, serving_size, description}.
    """
    d = d or date.today()
    slug = LOCATIONS.get(location, location)
    ensure_dirs()

    # check cache
    cache = _cache_path(slug, d)
    if cache.exists():
        return json.loads(cache.read_text())

    url = f"{DINING_BASE_URL}/{slug}/?date={d.isoformat()}"
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    items = []

    for link in soup.select("a.show-nutrition"):
        recipe_id = link.get("data-recipe", "")
        name = link.get_text(strip=True)

        # find station header by walking up
        station = ""
        parent = link.find_parent("ul")
        if parent:
            prev = parent.find_previous_sibling()
            if prev and prev.name in ("h3", "h4", "div"):
                station = prev.get_text(strip=True)

        # parse embedded nutrition JSON
        nutrition_div = soup.find(id=f"recipe-nutrition-{recipe_id}")
        if not nutrition_div:
            continue

        try:
            data = json.loads(nutrition_div.get_text(strip=True))
        except (json.JSONDecodeError, TypeError):
            continue

        facts = {f["label"]: f["value"] for f in data.get("facts", [])}

        items.append({
            "name": data.get("name", name),
            "station": station,
            "description": data.get("description", ""),
            "serving_size": data.get("serving_size", ""),
            "calories": facts.get("Calories", 0),
            "protein": facts.get("Protein", 0),
            "fat": facts.get("Total Fat", 0),
            "carbs": facts.get("Total Carbohydrate", 0),
            "fiber": facts.get("Dietary Fiber", 0),
            "sodium": facts.get("Sodium", 0),
            "sugar": facts.get("Total Sugars", 0),
            "ingredients": data.get("ingredients_list", ""),
            "allergens": data.get("allergens_list", ""),
        })

    # cache result
    cache.write_text(json.dumps(items, indent=2))
    return items
