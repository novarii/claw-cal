"""Blue Cactus build-your-own bowls.
Nutrition per typical serving. Sources: USDA FoodData Central, Open Food Facts.
Serving sizes: base ~200g, beans ~130g, protein ~113g (4oz), toppings ~30g, drinks 20oz (590ml).
"""

# USDA: cilantro lime rice 215cal/100g (Branded), brown rice 124cal/100g (FNDDS), potato 126cal/100g (FNDDS)
BASES = {
    "cilantro lime rice": {"calories": 430, "protein": 7, "fat": 15, "carbs": 66, "fiber": 1},
    "brown rice": {"calories": 248, "protein": 5, "fat": 2, "carbs": 52, "fiber": 3},
    "fiesta potato": {"calories": 252, "protein": 4, "fat": 9, "carbs": 41, "fiber": 3},
}

# USDA SR Legacy: black beans cooked 132cal/100g
BEANS = {
    "black beans": {"calories": 172, "protein": 12, "fat": 1, "carbs": 31, "fiber": 11},
    "no beans": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0},
}

# USDA FNDDS: chicken thigh grilled 233cal/100g, beef braised 191cal/100g
PROTEINS = {
    "pollo asado": {"calories": 263, "protein": 21, "fat": 16, "carbs": 8, "fiber": 0},
    "birria beef": {"calories": 216, "protein": 33, "fat": 6, "carbs": 6, "fiber": 0},
    "vegan sofrito": {"calories": 101, "protein": 2, "fat": 0, "carbs": 23, "fiber": 0},
    "no protein": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0},
}

EXTRA_PROTEINS = {
    "extra pollo asado": {"calories": 263, "protein": 21, "fat": 16, "carbs": 8, "fiber": 0},
    "extra birria beef": {"calories": 216, "protein": 33, "fat": 6, "carbs": 6, "fiber": 0},
    "extra vegan sofrito": {"calories": 101, "protein": 2, "fat": 0, "carbs": 23, "fiber": 0},
}

# USDA verified per 100g, scaled to serving. Topping ~30g, cheese ~28g, sauce ~30g.
# sour cream 200cal/100g, lettuce ~0cal/100g (Foundation), salsa verde 31cal/100g,
# salsa roja 34cal/100g (FNDDS), pico 24cal/100g, cheese blend 362cal/100g (FNDDS),
# cotija ~350cal/100g (Foundation), ranch 430cal/100g (FNDDS), queso 143cal/100g (SR Legacy)
TOPPINGS = {
    "queso": {"calories": 43, "protein": 1, "fat": 3, "carbs": 3, "fiber": 0},
    "fajita peppers and onions": {"calories": 20, "protein": 1, "fat": 0, "carbs": 4, "fiber": 1},
    "shredded lettuce": {"calories": 0, "protein": 0, "fat": 0, "carbs": 1, "fiber": 0},
    "fiesta cheese blend": {"calories": 101, "protein": 6, "fat": 8, "carbs": 1, "fiber": 0},
    "cotija": {"calories": 98, "protein": 7, "fat": 8, "carbs": 1, "fiber": 0},
    "pickled red onion": {"calories": 5, "protein": 0, "fat": 0, "carbs": 1, "fiber": 0},
    "cilantro": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0},
    "salsa verde": {"calories": 9, "protein": 0, "fat": 0, "carbs": 2, "fiber": 1},
    "salsa roja": {"calories": 10, "protein": 0, "fat": 0, "carbs": 2, "fiber": 1},
    "pico": {"calories": 7, "protein": 0, "fat": 0, "carbs": 2, "fiber": 0},
    "pineapple salsa": {"calories": 11, "protein": 0, "fat": 0, "carbs": 2, "fiber": 1},
    "sour cream": {"calories": 60, "protein": 1, "fat": 5, "carbs": 2, "fiber": 0},
    "avocado crema": {"calories": 128, "protein": 1, "fat": 13, "carbs": 2, "fiber": 0},
    "chipotle ranch": {"calories": 129, "protein": 0, "fat": 13, "carbs": 2, "fiber": 0},
}

# USDA: horchata 58cal/100g (Branded), hibiscus tea ~0cal/100g (sweetened ~19cal/100g),
# mango drink 10cal/100g (FNDDS), lemonade 42cal/100g (Branded), guava 33cal/100g (SR Legacy).
# All 20oz (590ml).
BEVERAGES = {
    "horchata": {"calories": 342, "protein": 7, "fat": 7, "carbs": 64, "fiber": 0},
    "jamaica": {"calories": 112, "protein": 0, "fat": 0, "carbs": 18, "fiber": 0},
    "mango agua fresca": {"calories": 59, "protein": 0, "fat": 0, "carbs": 15, "fiber": 0},
    "guava agua fresca": {"calories": 195, "protein": 0, "fat": 0, "carbs": 46, "fiber": 0},
    "mango lemonade": {"calories": 130, "protein": 0, "fat": 0, "carbs": 33, "fiber": 0},
    "strawberry watermelon": {"calories": 120, "protein": 0, "fat": 0, "carbs": 30, "fiber": 0},
    "homestyle lemonade": {"calories": 248, "protein": 0, "fat": 0, "carbs": 69, "fiber": 0},
}

ALL_COMPONENTS = {}
for group in [BASES, BEANS, PROTEINS, EXTRA_PROTEINS, TOPPINGS, BEVERAGES]:
    ALL_COMPONENTS.update(group)


def build_bowl(base: str, protein: str, toppings: list[str],
               beans: str | None = None, extra_protein: str | None = None,
               beverage: str | None = None) -> dict:
    """Build a Blue Cactus bowl and return totals."""
    components = []
    totals = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0}

    def add(name: str, lookup: dict):
        key = name.lower().strip()
        for k, v in lookup.items():
            if key in k or k in key:
                components.append({"name": k, **v})
                for macro in totals:
                    totals[macro] += v.get(macro, 0)
                return True
        return False

    add(base, BASES)
    if beans:
        add(beans, BEANS)
    add(protein, PROTEINS)
    if extra_protein:
        add(extra_protein, EXTRA_PROTEINS)
    for t in toppings:
        add(t, TOPPINGS)
    if beverage:
        add(beverage, BEVERAGES)

    return {
        "name": "Blue Cactus Bowl",
        "components": components,
        **totals,
    }


def list_menu() -> dict:
    return {
        "bases": list(BASES.keys()),
        "beans": list(BEANS.keys()),
        "proteins": list(PROTEINS.keys()),
        "extra_proteins": list(EXTRA_PROTEINS.keys()),
        "toppings": list(TOPPINGS.keys()),
        "beverages": list(BEVERAGES.keys()),
    }
