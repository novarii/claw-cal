"""Blue Cactus build-your-own bowls.
USDA FoodData Central estimates per component.
"""

BASES = {
    "cilantro lime rice": {"calories": 210, "protein": 4, "fat": 3, "carbs": 40, "fiber": 1},
    "brown rice": {"calories": 210, "protein": 5, "fat": 2, "carbs": 44, "fiber": 3},
    "fiesta potato": {"calories": 230, "protein": 4, "fat": 9, "carbs": 33, "fiber": 3},
}

BEANS = {
    "black beans": {"calories": 130, "protein": 8, "fat": 0.5, "carbs": 22, "fiber": 8},
    "no beans": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0},
}

PROTEINS = {
    "pollo asado": {"calories": 210, "protein": 32, "fat": 8, "carbs": 1, "fiber": 0},
    "birria beef": {"calories": 250, "protein": 28, "fat": 14, "carbs": 3, "fiber": 0},
    "vegan sofrito": {"calories": 150, "protein": 8, "fat": 7, "carbs": 14, "fiber": 3},
    "no protein": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0},
}

EXTRA_PROTEINS = {
    "extra pollo asado": {"calories": 210, "protein": 32, "fat": 8, "carbs": 1, "fiber": 0},
    "extra birria beef": {"calories": 250, "protein": 28, "fat": 14, "carbs": 3, "fiber": 0},
    "extra vegan sofrito": {"calories": 150, "protein": 8, "fat": 7, "carbs": 14, "fiber": 3},
}

TOPPINGS = {
    "queso": {"calories": 120, "protein": 5, "fat": 9, "carbs": 4, "fiber": 0},
    "fajita peppers and onions": {"calories": 25, "protein": 1, "fat": 0, "carbs": 5, "fiber": 1},
    "shredded lettuce": {"calories": 5, "protein": 0, "fat": 0, "carbs": 1, "fiber": 0},
    "fiesta cheese blend": {"calories": 110, "protein": 7, "fat": 9, "carbs": 1, "fiber": 0},
    "cotija": {"calories": 100, "protein": 7, "fat": 8, "carbs": 1, "fiber": 0},
    "pickled red onion": {"calories": 10, "protein": 0, "fat": 0, "carbs": 2, "fiber": 0},
    "cilantro": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0},
    "salsa verde": {"calories": 15, "protein": 0, "fat": 0, "carbs": 3, "fiber": 0},
    "salsa roja": {"calories": 15, "protein": 0, "fat": 0, "carbs": 3, "fiber": 0},
    "pico": {"calories": 15, "protein": 0, "fat": 0, "carbs": 3, "fiber": 1},
    "pineapple salsa": {"calories": 20, "protein": 0, "fat": 0, "carbs": 5, "fiber": 0},
    "sour cream": {"calories": 60, "protein": 1, "fat": 5, "carbs": 2, "fiber": 0},
    "avocado crema": {"calories": 70, "protein": 1, "fat": 6, "carbs": 3, "fiber": 1},
    "chipotle ranch": {"calories": 110, "protein": 1, "fat": 11, "carbs": 2, "fiber": 0},
}

BEVERAGES = {
    "horchata": {"calories": 160, "protein": 1, "fat": 3, "carbs": 33, "fiber": 0},
    "jamaica": {"calories": 90, "protein": 0, "fat": 0, "carbs": 23, "fiber": 0},
    "mango agua fresca": {"calories": 120, "protein": 0, "fat": 0, "carbs": 30, "fiber": 0},
    "guava agua fresca": {"calories": 120, "protein": 0, "fat": 0, "carbs": 30, "fiber": 0},
    "mango lemonade": {"calories": 130, "protein": 0, "fat": 0, "carbs": 33, "fiber": 0},
    "strawberry watermelon": {"calories": 110, "protein": 0, "fat": 0, "carbs": 28, "fiber": 0},
    "homestyle lemonade": {"calories": 120, "protein": 0, "fat": 0, "carbs": 31, "fiber": 0},
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
