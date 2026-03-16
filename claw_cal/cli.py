import click
from datetime import date

from .config import load_config, save_config, LOCATIONS
from .scraper import scrape_menu
from .matcher import match_items
from .presets import get_preset, list_presets, list_aliases, add_preset, remove_preset
from .blue_cactus import build_bowl, list_menu as bc_menu
from .tracker import log_entry, get_status, get_history


def _fmt_macros(cal, p, f, c):
    return f"{cal} cal | {p}g P | {f}g F | {c}g C"


def _print_status(s):
    bar_len = 30
    pct = min(s["calories"] / s["target"], 1.0) if s["target"] else 0
    filled = int(bar_len * pct)
    bar = "█" * filled + "░" * (bar_len - filled)

    click.echo(f"\n  {s['date']}")
    click.echo(f"  [{bar}] {s['calories']}/{s['target']} cal")
    click.echo(f"  {_fmt_macros(s['calories'], s['protein'], s['fat'], s['carbs'])}")
    remaining = s["remaining"]
    if remaining > 0:
        click.echo(f"  {remaining} cal remaining")
    else:
        click.echo(f"  {abs(remaining)} cal OVER target")
    click.echo()


@click.group()
def cli():
    """claw-cal — calorie tracker for UofR dining + chains"""
    pass


@cli.command()
@click.argument("location")
@click.option("--date", "-d", "dt", default=None, help="Date (YYYY-MM-DD), default today")
@click.option("--search", "-s", default=None, help="Search/filter items")
def menu(location, dt, search):
    """Show today's menu for a dining location."""
    d = date.fromisoformat(dt) if dt else date.today()
    loc = location.lower()

    if loc in ("blue-cactus", "bc"):
        m = bc_menu()
        click.echo("\n  Blue Cactus — Build Your Own Bowl\n")
        for category, items in m.items():
            click.echo(f"  {category.upper()}: {', '.join(items)}")
        click.echo()
        return

    items = scrape_menu(loc, d)
    if not items:
        click.echo(f"No menu data for {location} on {d.isoformat()}")
        return

    if search:
        from .matcher import fuzzy_match
        items = fuzzy_match(search, items, threshold=40)

    click.echo(f"\n  {location.upper()} — {d.isoformat()} ({len(items)} items)\n")

    current_station = ""
    for item in items:
        if item.get("station") and item["station"] != current_station:
            current_station = item["station"]
            click.echo(f"\n  --- {current_station} ---")
        cal = item["calories"]
        p = item["protein"]
        click.echo(f"  {item['name']:40s} {cal:>4} cal  {p}g P")

    click.echo()


@cli.command()
@click.argument("source")
@click.argument("items_str", nargs=-1)
@click.option("--base", default=None, help="Bowl base (blue cactus)")
@click.option("--protein", default=None, help="Bowl protein (blue cactus)")
@click.option("--toppings", "-t", default=None, help="Bowl toppings, comma-separated (blue cactus)")
@click.option("--beans", default=None, help="Bowl beans (blue cactus)")
@click.option("--extra-protein", default=None, help="Extra protein (blue cactus)")
@click.option("--drink", default=None, help="Beverage (blue cactus)")
def log(source, items_str, base, protein, toppings, beans, extra_protein, drink):
    """Log food. Source: douglass, pit, blue-cactus/bc, or a preset name."""
    source_lower = source.lower()

    # check if it's a preset (e.g., "claw-cal log chipotle bowl")
    preset_query = " ".join([source_lower] + list(items_str)).strip()
    preset = get_preset(preset_query)
    if not preset and items_str:
        preset = get_preset(" ".join(items_str))
    if preset:
        status = log_entry([preset], source_lower)
        click.echo(f"\n  + {preset['name']}")
        click.echo(f"    {_fmt_macros(preset['calories'], preset['protein'], preset['fat'], preset['carbs'])}")
        _print_status(status)
        return

    # blue cactus bowl builder
    if source_lower in ("blue-cactus", "bc"):
        if not base or not protein:
            click.echo("Need --base and --protein for Blue Cactus bowl")
            click.echo("Example: claw-cal log bc --base 'brown rice' --protein 'pollo asado' --toppings 'queso,pico,lettuce'")
            return

        topping_list = [t.strip() for t in toppings.split(",")] if toppings else []
        bowl = build_bowl(base, protein, topping_list, beans=beans,
                         extra_protein=extra_protein, beverage=drink)
        status = log_entry([bowl], "blue-cactus")
        click.echo(f"\n  + Blue Cactus Bowl")
        for comp in bowl["components"]:
            click.echo(f"    - {comp['name']:30s} {comp['calories']:>4} cal")
        click.echo(f"    {'TOTAL':>30s}  {_fmt_macros(bowl['calories'], bowl['protein'], bowl['fat'], bowl['carbs'])}")
        _print_status(status)
        return

    # dining hall — scrape + fuzzy match
    if source_lower not in LOCATIONS:
        click.echo(f"Unknown source: {source}. Use: {', '.join(LOCATIONS.keys())} or a preset name.")
        return

    if not items_str:
        click.echo("What did you eat? e.g.: claw-cal log douglass \"eggs, bacon, pancakes\"")
        return

    query = " ".join(items_str)
    queries = [q.strip() for q in query.split(",")]

    menu_items = scrape_menu(source_lower)
    if not menu_items:
        click.echo(f"No menu data for {source} today")
        return

    matched = match_items(queries, menu_items)
    if not matched:
        click.echo(f"Couldn't match any items. Try: claw-cal menu {source}")
        return

    click.echo(f"\n  Matched {len(matched)} items:")
    for item in matched:
        score = item.pop("match_score", 0)
        click.echo(f"    {item['name']:40s} {item['calories']:>4} cal  (match: {score}%)")

    status = log_entry(matched, source_lower)
    _print_status(status)


@cli.command()
@click.option("--days", "-d", default=1, help="Show last N days")
def status(days):
    """Show today's calorie status (or last N days)."""
    if days == 1:
        _print_status(get_status())
    else:
        for s in get_history(days):
            if s["entries"] > 0:
                _print_status(s)


@cli.command()
@click.argument("calories", type=int)
def target(calories):
    """Set daily calorie target."""
    cfg = load_config()
    cfg["target"] = calories
    save_config(cfg)
    click.echo(f"  Target set to {calories} cal/day")


@cli.command("presets")
def show_presets():
    """List all chain restaurant presets."""
    click.echo("\n  Chain Restaurant Presets\n")
    for key, p in list_presets().items():
        click.echo(f"  {key:30s} {p['calories']:>5} cal  {p.get('protein', 0):>3}g P")

    click.echo(f"\n  Aliases:")
    for alias, key in sorted(list_aliases().items()):
        click.echo(f"    {alias:25s} → {key}")
    click.echo()


@cli.command("add")
@click.argument("key")
@click.argument("name")
@click.option("--cal", type=int, required=True, help="Calories")
@click.option("--protein", "-p", type=float, default=0, help="Protein (g)")
@click.option("--fat", "-f", type=float, default=0, help="Fat (g)")
@click.option("--carbs", "-c", type=float, default=0, help="Carbs (g)")
@click.option("--alias", "-a", multiple=True, help="Short alias(es) for this preset")
@click.option("--lookup", "-l", is_flag=True, help="Auto-lookup nutrition from USDA")
def add_preset_cmd(key, name, cal, protein, fat, carbs, alias, lookup):
    """Add a custom preset. Example: claw-cal add tbell-griller "Beefy Potato Griller" --cal 470 -p 15 -f 20 -c 55"""
    if lookup:
        click.echo(f"  Looking up '{name}' on USDA...")
        from .usda import lookup_food
        result = lookup_food(name)
        if result:
            cal = cal or result["calories"]
            protein = protein or result["protein"]
            fat = fat or result["fat"]
            carbs = carbs or result["carbs"]
            click.echo(f"  Found: {result['description']} — {cal} cal")
        else:
            click.echo(f"  No USDA match. Using provided values.")

    preset = add_preset(key, name, cal, protein, fat, carbs, list(alias) if alias else None)
    click.echo(f"\n  + Added preset: {key}")
    click.echo(f"    {name}")
    click.echo(f"    {_fmt_macros(preset['calories'], preset['protein'], preset['fat'], preset['carbs'])}")
    if alias:
        click.echo(f"    Aliases: {', '.join(alias)}")
    click.echo()


@cli.command("remove")
@click.argument("key")
def remove_preset_cmd(key):
    """Remove a custom preset."""
    if remove_preset(key):
        click.echo(f"  Removed preset: {key}")
    else:
        click.echo(f"  Preset '{key}' not found (can only remove user-added presets)")


if __name__ == "__main__":
    cli()
