---
name: track-calories
description: "Track calories and macros from meals. Triggers when user mentions food they ate, dining halls (Douglass, Pit, Blue Cactus), chain restaurants (Chipotle, Taco Bell, McDonald's), calories, macros, or daily intake. Even casual like 'had eggs at doug' or 'chipotle today'."
metadata: {"openclaw":{"requires":{"bins":["claw-cal"]},"emoji":"🔥"}}
---

# track-calories

CLI tool: `claw-cal`. Translate what the user says about food into the right command and run it.

## Dining halls (fuzzy match against daily menu)
```bash
claw-cal log douglass "scrambled eggs, bacon"
claw-cal log pit "chicken, rice"
claw-cal menu douglass              # show today's menu
claw-cal menu douglass -s "chicken" # search
```

## Blue Cactus (build-your-own bowl)
```bash
claw-cal log bc --base "brown rice" --protein "pollo asado" --toppings "queso,pico,lettuce"
```
Bases: cilantro lime rice, brown rice, fiesta potato. Proteins: pollo asado, birria beef, vegan sofrito. Toppings: queso, fajita peppers and onions, shredded lettuce, fiesta cheese blend, cotija, pickled red onion, cilantro, salsa verde, salsa roja, pico, pineapple salsa, sour cream, avocado crema, chipotle ranch. Drinks: horchata, jamaica, mango agua fresca, guava agua fresca, mango lemonade, strawberry watermelon, homestyle lemonade.

## Chain presets
| Says | Command |
|---|---|
| chipotle / chipotle bowl | `claw-cal log chipotle bowl` |
| hpt / high protein taco | `claw-cal log hpt` |
| chips guac | `claw-cal log chips guac` |
| cantina bowl | `claw-cal log cantina bowl` |
| chalupa | `claw-cal log chalupa` |
| flatbread | `claw-cal log flatbread` |
| mcds / mcdonalds | `claw-cal log mcds` |

Multiple items = separate log commands.

## Quick-add (one-off, any food)
For snacks, drinks, random food not in dining hall or presets. Interactive — searches USDA, user picks or retries.
```bash
claw-cal quick "greek yogurt"            # search USDA, pick from results
claw-cal quick "protein bar" -s 2        # 2 servings
claw-cal quick "coffee" -d 2026-03-15    # backdate
```
Inside the prompt: pick [1-5], [r]etry search, or [m]anual entry.

## New items / custom presets
When the user orders something repeatedly, save it:
```bash
claw-cal add tbell-griller "Beefy Potato Griller" --cal 470 -p 15 -f 20 -c 55 -a "griller"
claw-cal remove tbell-griller
```

## Status
```bash
claw-cal status          # today
claw-cal status -d 7     # last 7 days
claw-cal target 1800     # set goal
claw-cal presets          # list all presets
```

Show CLI output directly. No extra commentary unless way over target.
