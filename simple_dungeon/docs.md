# Simple Dungeon — Complete Documentation

## Table of Contents
1. [Program Overview](#program-overview)
2. [File Structure & Data Flow](#file-structure--data-flow)
3. [data.py — Line-by-Line Breakdown](#datapy)
4. [player.py — Line-by-Line Breakdown](#playerpy)
5. [combat.py — Line-by-Line Breakdown](#combatpy)
6. [main.py — Line-by-Line Breakdown](#mainpy)
7. [How Everything Connects](#how-everything-connects)

---

## Program Overview

This is a text-based dungeon adventure game with 4 files, 4 rooms, 5 monster types, 3 player classes, and 8 items. The player types commands to explore rooms, fight monsters, collect loot, and win by defeating the Dragon Lord boss.

**Why text-based?** No graphics libraries needed. Everything uses `print()` and `input()` — the two most basic Python functions.

**Why dictionaries instead of classes (OOP)?** Dictionaries are simpler. A dict like `{"name": "Goblin", "hp": 30}` is easy to read, print, and debug. OOP would add complexity without gameplay benefit at this scale.

---

## File Structure & Data Flow

```
simple_dungeon/
├── data.py      — Stores all game data (no logic)
├── player.py    — Creates the player (reads from data.py)
├── combat.py    — Runs fights (modifies player & monster dicts)
└── main.py      — Game loop (uses all other files)
```

### How data flows between files:

```
                    data.py
                   /   |   \
                  /    |    \
          player.py  combat.py  main.py
              \        |        /
               \       |       /
                main.py (ties everything together)
```

**Step-by-step flow:**
1. `main.py` starts → calls `player.py` to create a player dict
2. `main.py` copies room data from `data.py` and spawns monster dicts inside rooms
3. Player types a command → `main.py` routes it to the right function
4. If "fight" → `main.py` calls `combat.py`, passing the player dict and monster dict
5. `combat.py` modifies both dicts directly (HP goes down, items added to inventory)
6. Control returns to `main.py` → checks if player died or boss defeated
7. Loop repeats until win or lose

**Why does this work?** In Python, dictionaries are passed by reference. When `combat.py` does `player["hp"] = player["hp"] - 10`, it changes the SAME dict that `main.py` is holding. No need to return an updated copy.

---

## data.py

**Purpose:** Store all game constants. No functions, no logic — just data. Every other file imports this.

**Why a separate file?** If you want to change the Goblin's HP from 30 to 50, you open ONE file and change ONE number. You don't have to search through combat logic or room code.

### Line-by-Line

```
Line 1: # data.py - All game data (classes, items, monsters, rooms)
Line 2: # This file just stores data. No logic here.
```
Comments explaining the file's purpose. Good practice so anyone reading knows what this file does.

```
Line 4: # ===== PLAYER CLASSES =====
Line 5: CLASSES = {
```
`CLASSES` is a dictionary. The keys are `"1"`, `"2"`, `"3"` (strings, not integers). **Why strings?** Because `input()` returns a string. When the player types "1", we can directly check `if choice in CLASSES` without converting to int.

```
Line 6:     "1": {
Line 7:         "name": "Warrior",
Line 8:         "hp": 100, "max_hp": 100,
```
Each class is a nested dict. `hp` is current health, `max_hp` is the cap. **Why both?** `hp` changes during combat (goes down when hit, up when healed). `max_hp` stays the same — it's the ceiling so potions can't heal above the limit.

```
Line 9:         "mp": 30, "max_mp": 30,
Line 10:        "attack": 12, "defense": 8,
```
`mp` = mana points for skills. `attack` = base damage. `defense` = damage reduction. **Why does Warrior have low MP (30)?** Balance — Warriors are strong with basic attacks, so they shouldn't also spam skills endlessly. Mages get 100 MP because skills are their main damage source.

```
Line 11:        "starting_weapon": "Iron Sword",
```
The name of the weapon this class starts with. This string matches a key in the `ITEMS` dict. **Why store the name instead of the item data?** To avoid duplicating item data inside the class. We look it up from `ITEMS` when needed.

```
Line 12-15:    "skills": [
                   {"name": "Heavy Slash", "damage": 20, "cost": 10},
                   {"name": "War Cry", "damage": 28, "cost": 15}
               ]
```
Skills are a list of dicts. Each skill has a name, damage value, and MP cost. **Why a list?** So we can loop through them with `for i in range(len(skills))` and show numbered options. **Why cost?** To prevent spamming — the player must choose between using MP on skills or saving it.

**Class balance idea:**
- **Warrior** (HP:100, ATK:12): Tank. Survives long fights. Low MP means skills are a bonus, not the main strategy.
- **Mage** (HP:60, ATK:5): Glass cannon. Low HP and ATK, but skills hit hard (30-45 damage) and has 100 MP to use them.
- **Archer** (HP:80, ATK:10): Middle ground. Decent at everything, not the best at anything.

```
Line 41-52: ITEMS = { ... }
```
Items are keyed by their name string (e.g., `"Iron Sword"`). Each item has a `"type"` field: `"weapon"`, `"armor"`, or `"potion"`.

**Why type matters:** The code uses `if item["type"] == "weapon"` to decide what to do. Weapons add to `attack`, armors add to `defense`, potions restore `hp` or `mp`. One dict, three behaviors — the `type` field acts as a router.

```
Line 54-101: MONSTERS = { ... }
```
Each monster has stats (hp, attack, defense), a loot table, gold reward, and skills.

```
Line 62:        "loot": [{"item": "Health Potion", "chance": 0.3}],
```
**Loot table idea:** Each entry has an item name and a drop chance (0.0 to 1.0). `0.3` means 30% chance. In `combat.py`, we roll `random.random()` (gives 0.0-1.0) and check if the roll is <= the chance. This makes loot feel rewarding because it's not guaranteed.

```
Line 89-100: "Dragon Lord": { ... "is_boss": True ... }
```
The boss has `"is_boss": True`. This flag is checked by `check_boss_defeated()` in `main.py`. **Why a flag instead of checking the name?** If you add more bosses later, just set `"is_boss": True` — no code changes needed.

```
Line 103-135: ROOMS = { ... }
```
Each room has: `name`, `description`, `exits` (direction → room key), `monsters` (list of monster names), `chest` (list of items or None).

```
Line 110:       "exits": {"north": "hallway"},
```
**Why a dictionary for exits?** Each key is a direction, each value is a room key. This makes navigation simple: `next_room = exits["north"]`. Adding a new exit is just adding a key-value pair.

```
Line 111:       "monsters": ["Goblin", "Slime"],
```
**Why store monster names (strings) instead of monster dicts?** Because `data.py` is a template. When the game starts, `main.py` converts these strings into actual monster dicts using `copy.deepcopy()`. This way, the template is never modified.

**Room layout and why:**
```
[Entrance] --north--> [Dark Hallway] --east--> [Treasure Room]
   (easy)                (intermediate)  |         (safe/loot)
                                         north
                                         |
                                    [Boss Chamber]
                                       (boss)
```
- **Entrance** has weak monsters (Goblin + Slime) so the player learns combat safely.
- **Dark Hallway** is the hub — connects to 3 rooms. Harder monsters here (Skeleton + Dark Knight).
- **Treasure Room** has no monsters, just a chest. Reward for exploring. Player can gear up before the boss.
- **Boss Chamber** has only the Dragon Lord. One-way pressure — beat the boss or die.

---

## player.py

**Purpose:** Handle player creation (name + class selection). Returns a player dict that gets passed everywhere.

### Line-by-Line

```
Line 4: import copy
Line 5: import data
```
`copy` is needed for `copy.deepcopy()` on skills. `data` gives us access to `CLASSES` and `ITEMS`.

```
Line 8: def create_player():
```
One function, one job: ask for input, build a player dict, return it.

```
Line 11-13: print("=" * 40) ...
```
`"=" * 40` creates a string of 40 equal signs. This is a simple way to make a visual header in the terminal. **Why 40?** Wide enough to look like a banner, short enough to fit any terminal.

```
Line 16: name = input("\n  Enter your name: ").strip()
```
`input()` pauses and waits for the player to type. `.strip()` removes extra spaces from both ends. **Why strip?** If the player accidentally types " hero  ", we want "hero", not " hero  ".

```
Line 17-18: if name == "":
                name = "Adventurer"
```
**Default name.** If the player just presses Enter without typing anything, we give them a name instead of having a blank.

```
Line 22: for key, cls in data.CLASSES.items():
```
`.items()` loops through the dictionary giving both the key (`"1"`, `"2"`, `"3"`) and the value (the class dict). We use `cls` as the variable name because `class` is a reserved word in Python.

```
Line 24: skill_names = ", ".join(s["name"] for s in cls["skills"])
```
This creates a comma-separated string from all skill names. `", ".join(...)` takes a list and puts `", "` between each item. Example result: `"Heavy Slash, War Cry"`.

```
Line 28-32: while True: / choice = input(...) / if choice in data.CLASSES: break
```
**Input validation loop.** Keeps asking until the player types a valid option. `if choice in data.CLASSES` checks if the typed string is a key in the CLASSES dict. If yes, `break` exits the loop. If no, print error and loop again.

```
Line 34: chosen = data.CLASSES[choice]
```
Now `chosen` points to the full class dict (e.g., the Warrior dict with all its stats).

```
Line 38-52: player = { ... }
```
Building the player dict. Most values come directly from the chosen class.

```
Line 47: "skills": copy.deepcopy(chosen["skills"]),
```
**Why deepcopy?** `chosen["skills"]` is a list of dicts. If we just did `player["skills"] = chosen["skills"]`, both the player and the class template would share the SAME list. Changing one would change the other. `deepcopy` creates a completely independent copy.

```
Line 48-51: "inventory": [], "weapon": "", "armor": "", "gold": 0
```
Player starts with empty inventory, no equipped armor, and 0 gold. The weapon gets equipped in the next block.

```
Line 55-58: weapon_name = chosen["starting_weapon"]
            weapon_data = data.ITEMS[weapon_name]
            player["weapon"] = weapon_name
            player["attack"] = player["attack"] + weapon_data["attack"]
```
**Auto-equip starting weapon:**
1. Get the weapon name from the class (e.g., `"Iron Sword"`)
2. Look up its data in `ITEMS` (e.g., `{"attack": 5, ...}`)
3. Set the weapon slot to the weapon name
4. Add the weapon's attack bonus to the player's attack

```
Line 64: return player
```
The completed player dict goes back to `main.py`, where it's stored as `hero`.

---

## combat.py

**Purpose:** Run turn-based fights. Player picks action → monster responds → repeat until one dies.

### Line-by-Line

```
Line 5: import random
Line 6: import data
```
`random` is used for monster skill selection (`random.choice`) and loot drops (`random.random`). `data` is used to look up item info when using potions.

```
Line 9: def fight(player, monster):
```
Takes the player dict and a monster dict. Both are modified directly (HP goes down, items added). **Returns `True`** if player wins, **`False`** if player dies.

```
Line 17: while True:
```
The combat loop. Runs forever until someone's HP hits 0, at which point `return True` or `return False` exits the function.

```
Line 30-38: if choice == "1": (Basic Attack)
```
**Damage formula:** `damage = player["attack"] - monster["defense"]`

This is the simplest possible formula. Your attack minus their defense = damage dealt. **Why `if damage < 1: damage = 1`?** If the monster's defense is higher than your attack, the formula gives 0 or negative. Minimum 1 damage ensures fights always end — no infinite stalemates.

```
Line 35-37: monster["hp"] = monster["hp"] - damage
            if monster["hp"] < 0:
                monster["hp"] = 0
```
Subtract damage from HP, then clamp to 0. **Why clamp?** So the display never shows negative HP like "-5/30", which looks broken.

```
Line 40-44: elif choice == "2": (Use Skill)
            result = use_skill(player, monster)
            if result == False:
                continue
```
Calls the `use_skill` function. If it returns `False` (player cancelled or couldn't afford), `continue` restarts the loop WITHOUT advancing to the monster's turn. **Why?** If the player picked a skill they can't afford, it's unfair to let the monster hit them for a non-action.

```
Line 46-52: elif choice == "3": (Use Item — skips attack)
```
Same pattern, but with a key difference: **using an item skips the player's attack**. The player heals but deals no damage. The monster still gets its turn. **Why?** Balance — if the player could heal AND attack, they'd be nearly invincible.

```
Line 58-73: Monster death → loot drops
```
When `monster["hp"] <= 0`:
1. Add the monster's gold to the player
2. Loop through the loot table, roll `random.random()` for each entry
3. If the roll <= the chance value, add the item to inventory
4. `return True` — fight is over, player won

```
Line 67-71: for drop in monster["loot"]:
                roll = random.random()
                if roll <= drop["chance"]:
                    player["inventory"].append(drop["item"])
```
**How loot probability works:** `random.random()` returns a float between 0.0 and 1.0. If `chance` is 0.3, the roll needs to be <= 0.3 — that's a 30% probability. If `chance` is 1.0, the item ALWAYS drops.

```
Line 75-89: Monster Turn
```

```
Line 77: skill = random.choice(monster["skills"])
```
`random.choice()` picks a random item from a list. The monster doesn't strategize — it just picks a random skill. **Why random?** Keeps fights unpredictable. Simple to code, and the player never knows what's coming next.

```
Line 78-83: damage = skill["damage"] - player["defense"]
            if damage < 1: damage = 1
            player["hp"] -= damage
            if player["hp"] < 0: player["hp"] = 0
```
Same damage formula as the player's attack, but reversed. Monster's skill damage minus player's defense.

```
Line 87-89: if player["hp"] <= 0:
                return False
```
Player died. Return `False` to `main.py`, which shows the Game Over screen.

### use_skill() function (Lines 92-133)

```
Line 96-98: for i in range(len(player["skills"])):
                skill = player["skills"][i]
                print(f"    {i + 1}. {skill['name']} ...")
```
Shows numbered skill list. `i + 1` makes it 1-indexed (humans count from 1, not 0).

```
Line 108: if not pick.isdigit():
```
`.isdigit()` checks if the string is all numbers. Prevents crashes from `int("abc")`.

```
Line 112: index = int(pick) - 1
```
Convert to int and subtract 1 to go from 1-indexed (what the player sees) to 0-indexed (what Python uses).

```
Line 120: if player["mp"] < skill["cost"]:
```
**MP check before using skill.** If not enough mana, return `False` so the player picks again.

### use_item_in_combat() function (Lines 136-192)

```
Line 140-144: Filter potions from inventory
```
Loops through inventory, checks each item's type in `data.ITEMS`. Only potions are usable in combat.

```
Line 174: if "hp_restore" in item:
```
**Why check with `in`?** Health Potions have `"hp_restore"` but not `"mp_restore"`. Mana Potions have `"mp_restore"` but not `"hp_restore"`. Using `in` handles both cases safely.

```
Line 175-179: old_hp = player["hp"]
              player["hp"] = player["hp"] + item["hp_restore"]
              if player["hp"] > player["max_hp"]:
                  player["hp"] = player["max_hp"]
              healed = player["hp"] - old_hp
```
**Clamping to max_hp:** Add the restore amount, but cap at `max_hp`. Then calculate actual amount healed. This prevents over-healing above the maximum.

```
Line 191: player["inventory"].remove(item_name)
```
`.remove()` deletes the FIRST occurrence of that string from the list. Potion is consumed — gone forever.

---

## main.py

**Purpose:** Entry point. Sets up the game, runs the command loop, handles win/lose.

### Imports (Lines 5-9)

- `copy` — for `deepcopy` when setting up rooms
- `random` — imported but used indirectly
- `data` — room and item data
- `player as player_module` — **why the alias?** To avoid `player = player.create_player()` which would overwrite the module name with the dict
- `combat` — for the `fight()` function

### setup_rooms() (Lines 12-28)

```
Line 15: rooms = copy.deepcopy(data.ROOMS)
```
**Critical line.** Makes a completely independent copy of all room data. Without this, killing a monster would permanently modify `data.ROOMS`.

```
Line 18-25: for room_key in rooms: ...
```
**Monster spawning:** Replaces string names (e.g., `"Goblin"`) with actual monster dicts. Each monster is deepcopied so killing it only affects that specific instance.

### equip_item() (Lines 83-144)

**Why unequip old item first?** If the player has Iron Sword (+5) equipped and equips Steel Sword (+10), we need to remove the +5 first, THEN add +10. Otherwise the player would have +15 (both bonuses stacked), which is a bug.

### check_boss_defeated() (Lines 255-262)

Scans ALL rooms for ANY boss with HP > 0. If found → `False`. If no living boss → `True`. **Why check all rooms?** Future-proof — if you add more bosses, this still works.

### main() Game Loop (Lines 267-431)

```
Line 269: hero = player_module.create_player()
```
Stored as `hero` (not `player`) to avoid shadowing the module name.

```
Line 278: while True:
```
**The main game loop.** Every iteration: show the room, ask for a command, execute it.

```
Line 284: command = input("\n  > ").strip().lower()
```
`.lower()` makes input case-insensitive.

```
Line 346: won = combat.fight(hero, target)
```
**This is where combat.py connects to main.py.** The `fight()` function modifies `hero` and `target` directly.

```
Line 430-431: if __name__ == "__main__": main()
```
**Python entry point pattern.** Only runs `main()` when the file is executed directly, not when imported.

---

## How Everything Connects

### Complete Data Flow

```
GAME START
    |
    v
main.py: main()
    |
    |-- player_module.create_player()  --> player.py reads data.CLASSES
    |       |                              and data.ITEMS
    |       v
    |   Returns: hero dict  <-- {"name", "hp", "mp", "attack",
    |                             "defense", "skills", "inventory",
    |                             "weapon", "armor", "gold"}
    |
    |-- setup_rooms()  --> copies data.ROOMS
    |       |              converts monster names to monster dicts
    |       v              (using data.MONSTERS + deepcopy)
    |   Returns: rooms dict
    |
    v
GAME LOOP (while True)
    |
    |-- show_room(room) --> displays room info
    |
    |-- input() --> player types a command
    |
    |-- "move"  --> changes current_room variable
    |
    |-- "fight" --> combat.fight(hero, target)
    |                   |
    |                   |-- Player turn: attack / skill / item
    |                   |-- Monster turn: random skill
    |                   |-- Monster dies: loot -> player["inventory"]
    |                   |-- Returns True (won) or False (died)
    |
    |               False -> GAME OVER (return)
    |               True  -> check_boss_defeated()
    |                          True  -> YOU WIN (return)
    |                          False -> continue loop
    |
    |-- "open"      --> chest items -> player["inventory"]
    |-- "equip"     --> item: inventory -> weapon/armor slot
    |-- "use"       --> potion consumed, HP or MP restored
    |-- "discard"   --> item removed from inventory
    |-- "quit"      --> return (end program)
```

### The Player Dict — Central Data Hub

The `hero` dict is the single source of truth. Every function reads or writes to it:

| Field | Set by | Modified by |
|---|---|---|
| name, class | player.py | never changes |
| hp | player.py | combat.py (damage, potions), main.py (potions) |
| max_hp | player.py | never changes |
| mp | player.py | combat.py (skills, potions), main.py (potions) |
| attack | player.py | main.py (equip_item) |
| defense | player.py | main.py (equip_item) |
| skills | player.py | read by combat.py |
| inventory | player.py (empty) | combat.py (loot), main.py (equip/use/discard/chest) |
| weapon, armor | player.py | main.py (equip_item) |
| gold | player.py (0) | combat.py (monster gold drop) |

### Why This Architecture Works

1. **data.py is never modified at runtime.** It's read-only. All live state exists in `hero` and `rooms` (created via deepcopy).

2. **Dicts are passed by reference.** When combat.py subtracts HP, main.py sees the change automatically.

3. **Each file has one job:** data.py = definitions, player.py = setup, combat.py = fighting, main.py = game flow.

4. **No circular imports.** Dependencies are one-way: `data.py <- player.py <- main.py` and `data.py <- combat.py <- main.py`.
