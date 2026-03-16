import json
from datetime import date, datetime

from .config import LOG_DIR, ensure_dirs, load_config


def _log_path(d: date) -> str:
    return LOG_DIR / f"{d.isoformat()}.json"


def _load_day(d: date) -> dict:
    path = _log_path(d)
    if path.exists():
        return json.loads(path.read_text())
    return {"date": d.isoformat(), "target": load_config().get("target", 2000), "entries": []}


def _save_day(d: date, data: dict):
    ensure_dirs()
    _log_path(d).write_text(json.dumps(data, indent=2))


def log_entry(items: list[dict], source: str, d: date | None = None) -> dict:
    """Log one or more items. Returns updated day summary."""
    d = d or date.today()
    day = _load_day(d)

    entry = {
        "time": datetime.now().strftime("%H:%M"),
        "source": source,
        "items": [],
        "total_calories": 0,
        "total_protein": 0,
        "total_fat": 0,
        "total_carbs": 0,
    }

    for item in items:
        entry["items"].append({
            "name": item.get("name", "Unknown"),
            "calories": item.get("calories", 0),
            "protein": item.get("protein", 0),
            "fat": item.get("fat", 0),
            "carbs": item.get("carbs", 0),
        })
        entry["total_calories"] += item.get("calories", 0)
        entry["total_protein"] += item.get("protein", 0)
        entry["total_fat"] += item.get("fat", 0)
        entry["total_carbs"] += item.get("carbs", 0)

    day["entries"].append(entry)
    _save_day(d, day)
    return get_status(d)


def get_status(d: date | None = None) -> dict:
    """Get day summary."""
    d = d or date.today()
    day = _load_day(d)

    totals = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for entry in day["entries"]:
        totals["calories"] += entry.get("total_calories", 0)
        totals["protein"] += entry.get("total_protein", 0)
        totals["fat"] += entry.get("total_fat", 0)
        totals["carbs"] += entry.get("total_carbs", 0)

    target = day.get("target", load_config().get("target", 2000))
    remaining = target - totals["calories"]

    return {
        "date": d.isoformat(),
        "target": target,
        "remaining": remaining,
        "entries": len(day["entries"]),
        **totals,
    }


def get_history(days: int = 7) -> list[dict]:
    """Get status for last N days."""
    from datetime import timedelta
    today = date.today()
    return [get_status(today - timedelta(days=i)) for i in range(days)]
