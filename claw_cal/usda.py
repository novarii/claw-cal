"""USDA FoodData Central API lookups."""
import requests
from .config import USDA_API_KEY, USDA_SEARCH_URL


def lookup_food(query: str) -> dict | None:
    """Search USDA for a food item. Returns per-serving nutrition or None."""
    try:
        resp = requests.get(USDA_SEARCH_URL, params={
            "query": query,
            "api_key": USDA_API_KEY,
            "pageSize": 5,
        }, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return None

    foods = resp.json().get("foods", [])
    if not foods:
        return None

    # Prefer FNDDS/SR Legacy/Foundation over Branded
    best = None
    for f in foods:
        if f.get("dataType") in ("Survey (FNDDS)", "SR Legacy", "Foundation"):
            best = f
            break
    if not best:
        best = foods[0]

    nutrients = {}
    for n in best.get("foodNutrients", []):
        num = n.get("nutrientNumber", "")
        if num == "208":
            nutrients["calories"] = round(n["value"])
        elif num == "203":
            nutrients["protein"] = round(n["value"], 1)
        elif num == "204":
            nutrients["fat"] = round(n["value"], 1)
        elif num == "205":
            nutrients["carbs"] = round(n["value"], 1)

    nutrients.setdefault("calories", 0)
    nutrients.setdefault("protein", 0)
    nutrients.setdefault("fat", 0)
    nutrients.setdefault("carbs", 0)

    return {
        "description": best["description"],
        "data_type": best.get("dataType", ""),
        "serving_size_g": best.get("servingSize"),
        **nutrients,
    }
