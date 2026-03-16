from thefuzz import fuzz, process


def fuzzy_match(query: str, items: list[dict], threshold: int = 55) -> list[dict]:
    """Match a query string against menu item names.
    Returns list of matched items with scores, sorted by score desc.
    """
    if not items:
        return []

    name_to_items = {}
    for item in items:
        name_to_items.setdefault(item["name"], item)

    names = list(name_to_items.keys())
    results = process.extract(query, names, scorer=fuzz.token_set_ratio, limit=5)

    matched = []
    for name, score in results:
        if score >= threshold:
            item = name_to_items[name].copy()
            item["match_score"] = score
            matched.append(item)

    return matched


def match_items(queries: list[str], items: list[dict], threshold: int = 55) -> list[dict]:
    """Match multiple query strings against menu items.
    Returns best match per query.
    """
    matched = []
    for q in queries:
        results = fuzzy_match(q.strip(), items, threshold)
        if results:
            matched.append(results[0])  # best match
    return matched
