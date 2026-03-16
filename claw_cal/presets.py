"""Hardcoded chain restaurant presets based on actual order history."""

PRESETS = {
    # === CHIPOTLE (verified via chipotle.com ingredient calculator) ===
    "chipotle-bowl": {
        "name": "Chipotle Burrito Bowl",
        "description": "Chicken, Brown Rice, Black Beans, Cheese, Corn Salsa, Sour Cream, Fajita Veggies",
        "calories": 845,
        "protein": 57,
        "fat": 37,
        "carbs": 82,
        "fiber": 13,
        "sodium": 2050,
    },
    "chipotle-bowl-double": {
        "name": "Chipotle Burrito Bowl (Double Chicken)",
        "description": "Double Chicken, Brown Rice, Black Beans, Queso, Cheese, Lettuce, Corn Salsa",
        "calories": 1035,
        "protein": 83,
        "fat": 43,
        "carbs": 80,
        "fiber": 13,
        "sodium": 2500,
    },
    "chipotle-hpt": {
        "name": "Chipotle HIGH PROTEIN TACO",
        "calories": 190,
        "protein": 15,
        "fat": 7,
        "carbs": 15,
        "fiber": 1,
        "sodium": 400,
    },
    "chipotle-chips-guac": {
        "name": "Chipotle Chips & Guacamole",
        "calories": 770,
        "protein": 10,
        "fat": 47,
        "carbs": 80,
        "fiber": 11,
        "sodium": 420,
    },
    "chipotle-tortilla": {
        "name": "Chipotle Tortilla On The Side",
        "calories": 320,
        "protein": 8,
        "fat": 9,
        "carbs": 50,
        "fiber": 2,
        "sodium": 690,
    },

    # === TACO BELL (verified via tacobell.com / fastfoodnutrition.org) ===
    "tbell-cantina-bowl": {
        "name": "Taco Bell Cantina Chicken Bowl",
        "description": "Slow-Roasted Chicken, Avocado Ranch, Black Beans, Cheese, Guac, Lettuce, Pico, Purple Cabbage, Sour Cream, Seasoned Rice",
        "calories": 530,
        "protein": 26,
        "fat": 21,
        "carbs": 59,
        "fiber": 8,
        "sodium": 1310,
    },
    "tbell-chalupa": {
        "name": "Taco Bell Chalupa Supreme (Beef)",
        "calories": 350,
        "protein": 13,
        "fat": 20,
        "carbs": 31,
        "fiber": 3,
        "sodium": 580,
    },
    "tbell-dlt-supreme": {
        "name": "Taco Bell Doritos Locos Taco Supreme",
        "calories": 190,
        "protein": 8,
        "fat": 11,
        "carbs": 15,
        "fiber": 2,
        "sodium": 370,
    },
    "tbell-flatbread": {
        "name": "Taco Bell 3 Cheese Chicken Flatbread Melt",
        "calories": 330,
        "protein": 20,
        "fat": 15,
        "carbs": 28,
        "fiber": 2,
        "sodium": 750,
    },
    "tbell-nacho-fries-chicken": {
        "name": "Taco Bell Chicken Bacon Ranch Nacho Fries",
        "calories": 350,
        "protein": 13,
        "fat": 24,
        "carbs": 22,
        "fiber": 2,
        "sodium": 870,
    },
    "tbell-cheesy-beef-burrito": {
        "name": "Taco Bell Cheesy Double Beef Burrito",
        "calories": 560,
        "protein": 21,
        "fat": 25,
        "carbs": 63,
        "fiber": 4,
        "sodium": 1350,
    },

    # === MCDONALD'S (verified via mcdonalds.com) ===
    "mcds-dqpc-meal": {
        "name": "McDonald's Double Quarter Pounder w/ Cheese Meal",
        "description": "Double QPC + Large Fries + Large Sprite",
        "calories": 1500,
        "protein": 55,
        "fat": 65,
        "carbs": 182,
        "fiber": 7,
        "sodium": 1900,
    },
    "mcds-dqpc": {
        "name": "McDonald's Double Quarter Pounder w/ Cheese",
        "calories": 740,
        "protein": 48,
        "fat": 42,
        "carbs": 43,
        "fiber": 2,
        "sodium": 1360,
    },
    "mcds-qpc": {
        "name": "McDonald's Quarter Pounder w/ Cheese",
        "calories": 520,
        "protein": 30,
        "fat": 26,
        "carbs": 42,
        "fiber": 2,
        "sodium": 1100,
    },
    "mcds-large-fries": {
        "name": "McDonald's Large Fries",
        "calories": 480,
        "protein": 7,
        "fat": 23,
        "carbs": 65,
        "fiber": 5,
        "sodium": 400,
    },
}

# Aliases for quick access
ALIASES = {
    # chipotle
    "chipotle bowl": "chipotle-bowl",
    "chipotle": "chipotle-bowl",
    "chip bowl": "chipotle-bowl",
    "chipotle double": "chipotle-bowl-double",
    "hpt": "chipotle-hpt",
    "high protein taco": "chipotle-hpt",
    "chips guac": "chipotle-chips-guac",
    "chips and guac": "chipotle-chips-guac",
    # taco bell
    "tbell cantina": "tbell-cantina-bowl",
    "cantina bowl": "tbell-cantina-bowl",
    "cantina chicken": "tbell-cantina-bowl",
    "chalupa": "tbell-chalupa",
    "dlt": "tbell-dlt-supreme",
    "doritos taco": "tbell-dlt-supreme",
    "flatbread": "tbell-flatbread",
    "flatbread melt": "tbell-flatbread",
    "nacho fries": "tbell-nacho-fries-chicken",
    "cheesy beef": "tbell-cheesy-beef-burrito",
    # mcdonalds
    "mcds meal": "mcds-dqpc-meal",
    "mcds": "mcds-dqpc-meal",
    "dqpc meal": "mcds-dqpc-meal",
    "dqpc": "mcds-dqpc",
    "qpc": "mcds-qpc",
}


def _load_user_presets() -> tuple[dict, dict]:
    """Load user-defined presets and aliases from disk."""
    from .config import USER_PRESETS_FILE
    if USER_PRESETS_FILE.exists():
        import json
        data = json.loads(USER_PRESETS_FILE.read_text())
        return data.get("presets", {}), data.get("aliases", {})
    return {}, {}


def _save_user_presets(presets: dict, aliases: dict):
    from .config import USER_PRESETS_FILE, ensure_dirs
    import json
    ensure_dirs()
    USER_PRESETS_FILE.write_text(json.dumps({"presets": presets, "aliases": aliases}, indent=2))


def get_preset(name: str) -> dict | None:
    user_presets, user_aliases = _load_user_presets()
    all_aliases = {**ALIASES, **user_aliases}
    all_presets = {**PRESETS, **user_presets}
    key = all_aliases.get(name.lower().strip(), name.lower().strip())
    return all_presets.get(key)


def list_presets() -> dict:
    user_presets, _ = _load_user_presets()
    return {**PRESETS, **user_presets}


def list_aliases() -> dict:
    _, user_aliases = _load_user_presets()
    return {**ALIASES, **user_aliases}


def add_preset(key: str, name: str, calories: int, protein: float, fat: float,
               carbs: float, aliases: list[str] | None = None) -> dict:
    """Add a user-defined preset. Returns the preset dict."""
    user_presets, user_aliases = _load_user_presets()
    preset = {"name": name, "calories": calories, "protein": protein, "fat": fat, "carbs": carbs}
    user_presets[key] = preset
    if aliases:
        for a in aliases:
            user_aliases[a.lower().strip()] = key
    _save_user_presets(user_presets, user_aliases)
    return preset


def remove_preset(key: str) -> bool:
    user_presets, user_aliases = _load_user_presets()
    if key in user_presets:
        del user_presets[key]
        user_aliases = {a: k for a, k in user_aliases.items() if k != key}
        _save_user_presets(user_presets, user_aliases)
        return True
    return False
