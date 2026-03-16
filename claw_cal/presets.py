"""Hardcoded chain restaurant presets based on actual order history."""

PRESETS = {
    # === CHIPOTLE ===
    "chipotle-bowl": {
        "name": "Chipotle Burrito Bowl",
        "description": "Chicken, Brown Rice, Black Beans, Cheese, Corn Salsa, Sour Cream, Fajita Veggies",
        "calories": 870,
        "protein": 55,
        "fat": 30.5,
        "carbs": 93,
        "fiber": 13,
        "sodium": 2050,
    },
    "chipotle-bowl-double": {
        "name": "Chipotle Burrito Bowl (Double Chicken)",
        "description": "Double Chicken, Brown Rice, Black Beans, Queso, Cheese, Lettuce, Corn Salsa",
        "calories": 1045,
        "protein": 80,
        "fat": 37,
        "carbs": 99,
        "fiber": 13,
        "sodium": 2500,
    },
    "chipotle-hpt": {
        "name": "Chipotle HIGH PROTEIN TACO",
        "calories": 480,
        "protein": 54,
        "fat": 19,
        "carbs": 23,
        "fiber": 3,
        "sodium": 1200,
    },
    "chipotle-chips-guac": {
        "name": "Chipotle Chips & Guacamole",
        "calories": 770,
        "protein": 8,
        "fat": 43,
        "carbs": 83,
        "fiber": 11,
        "sodium": 420,
    },
    "chipotle-tortilla": {
        "name": "Chipotle Tortilla On The Side",
        "calories": 320,
        "protein": 5,
        "fat": 9,
        "carbs": 50,
        "fiber": 2,
        "sodium": 690,
    },

    # === TACO BELL ===
    "tbell-cantina-bowl": {
        "name": "Taco Bell Cantina Chicken Bowl",
        "description": "Slow-Roasted Chicken, Avocado Ranch, Black Beans, Cheese, Guac, Lettuce, Pico, Purple Cabbage, Sour Cream, Seasoned Rice",
        "calories": 580,
        "protein": 29,
        "fat": 22,
        "carbs": 68,
        "fiber": 8,
        "sodium": 1310,
    },
    "tbell-chalupa": {
        "name": "Taco Bell Chalupa Supreme (Beef)",
        "calories": 350,
        "protein": 14,
        "fat": 21,
        "carbs": 30,
        "fiber": 3,
        "sodium": 580,
    },
    "tbell-dlt-supreme": {
        "name": "Taco Bell Doritos Locos Taco Supreme",
        "calories": 200,
        "protein": 9,
        "fat": 11,
        "carbs": 16,
        "fiber": 2,
        "sodium": 370,
    },
    "tbell-flatbread": {
        "name": "Taco Bell 3 Cheese Chicken Flatbread Melt",
        "calories": 490,
        "protein": 22,
        "fat": 23,
        "carbs": 48,
        "fiber": 3,
        "sodium": 1050,
    },
    "tbell-nacho-fries-chicken": {
        "name": "Taco Bell Chicken Bacon Ranch Nacho Fries",
        "calories": 670,
        "protein": 22,
        "fat": 38,
        "carbs": 58,
        "fiber": 5,
        "sodium": 1540,
    },
    "tbell-cheesy-beef-burrito": {
        "name": "Taco Bell Cheesy Double Beef Burrito",
        "calories": 470,
        "protein": 19,
        "fat": 20,
        "carbs": 53,
        "fiber": 5,
        "sodium": 1170,
    },

    # === MCDONALD'S ===
    "mcds-dqpc-meal": {
        "name": "McDonald's Double Quarter Pounder w/ Cheese Meal",
        "description": "Double QPC + Large Fries + Large Sprite",
        "calories": 1320,
        "protein": 55,
        "fat": 60,
        "carbs": 147,
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
        "protein": 6,
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


def get_preset(name: str) -> dict | None:
    key = ALIASES.get(name.lower().strip(), name.lower().strip())
    return PRESETS.get(key)


def list_presets() -> dict:
    return PRESETS
