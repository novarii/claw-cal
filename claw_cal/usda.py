"""USDA FoodData Central API lookups."""
import requests
from .config import USDA_API_KEY, USDA_SEARCH_URL


def search_foods(query: str, limit: int = 5) -> list[dict]:
    """Search USDA and return top matches with nutrition per 100g."""
    try:
        resp = requests.get(USDA_SEARCH_URL, params={
            "query": query,
            "api_key": USDA_API_KEY,
            "pageSize": limit,
        }, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return []

    results = []
    for f in resp.json().get("foods", []):
        nutrients = {}
        for n in f.get("foodNutrients", []):
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

        results.append({
            "description": f["description"],
            "data_type": f.get("dataType", ""),
            "serving_size_g": f.get("servingSize"),
            "household": f.get("householdServingFullText", ""),
            **nutrients,
        })

    return results


def lookup_food(query: str) -> dict | None:
    """Search USDA for a food item. Returns best match or None."""
    results = search_foods(query, limit=5)
    if not results:
        return None

    # Prefer FNDDS/SR Legacy/Foundation over Branded
    for r in results:
        if r["data_type"] in ("Survey (FNDDS)", "SR Legacy", "Foundation"):
            return r
    return results[0]
