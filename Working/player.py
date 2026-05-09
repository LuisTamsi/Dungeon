# =============================================================================
# player.py — Player Creation and Player Actions
# Handles character setup: name input, class selection, starting equipment.
# Player-specific actions: inventory, equip, use, discard, stats display.
# =============================================================================

import copy
import sys

import data
import utils
import items as item_module


# -----------------------------------------------------------------------------
# Player Creation
# -----------------------------------------------------------------------------

def new_player() -> dict:
    """
    Interactively create a new player:
    1. Enter name
    2. Select class (shows stats and skills for each option)
    3. Build player dict with deepcopy of skills (see items.py for why)
    4. Auto-equip starting weapon

    Returns a fully initialised player dict.
    """
    utils.header("WELCOME TO THE DUNGEON")
    print()
    print("  A dark realm of monsters and forgotten treasure awaits.")
    print("  Only the strong survive. Many have tried. Most have failed.")
    print()

    # --- Name ---
    player_name = input("  Enter your name, adventurer: ").strip()
    if not player_name:
        player_name = "Adventurer"

    # --- Class Selection ---
    utils.header("CHOOSE YOUR CLASS")
    for key, cls in data.CLASSES.items():
        print(f"\n  [{key}] {cls['name']}")
        print(f"      {cls['description']}")
        print(f"      HP: {cls['max_hp']}  MP: {cls['max_mp']}  "
              f"ATK: {cls['base_attack']}  DEF: {cls['base_defense']}")
        print(f"      Starting Weapon: {cls['starting_weapon']}")
        print(f"      Skills:")
        for sk in cls["skills"]:
            cost = sk.get("mana_cost", 0)
            if sk["type"] == "attack":
                effect = f"{sk.get('damage', 0)} dmg"
            else:
                effect = f"+{sk.get('defense_bonus', 0)} DEF (1 turn)"
            print(f"        - {sk['name']} [{cost} MP] — {effect}")

    print()
    valid = list(data.CLASSES.keys())
    choice = utils.get_valid_input(
        f"  Enter your choice ({'/'.join(valid)}): ", valid
    )
    class_data = data.CLASSES[choice]

    # --- Build player dict ---
    player = {
        "name": player_name,
        "class": class_data["name"],
        "hp": class_data["hp"],
        "max_hp": class_data["max_hp"],
        "mp": class_data["mp"],
        "max_mp": class_data["max_mp"],
        # base_attack and base_defense track the class baseline.
        # 'attack' and 'defense' are the effective values (base + equipment).
        "base_attack": class_data["base_attack"],
        "base_defense": class_data["base_defense"],
        "attack": class_data["base_attack"],
        "defense": class_data["base_defense"],
        "skills": copy.deepcopy(class_data["skills"]),
        "inventory": [],
        "weapon": "",
        "armor": "",
        "gold": 0,
    }

    # --- Auto-equip starting weapon ---
    starting_weapon = class_data["starting_weapon"]
    player["inventory"].append(starting_weapon)
    item_module.equip_item(player, starting_weapon)

    utils.blank()
    print(f"  Welcome, {player['name']} the {player['class']}!")
    print("  Your journey into the dungeon begins now. Good luck.\n")

    return player


# -----------------------------------------------------------------------------
# Status Display
# -----------------------------------------------------------------------------

def show_stats(player: dict):
    """Display the player's current stats, class, and equipment."""
    utils.subheader(f"  {player['name']} — {player['class']}")
    utils.display_stats(player)
    weapon = player["weapon"] if player["weapon"] else "None"
    armor  = player["armor"]  if player["armor"]  else "None"
    print(f"  Weapon : {weapon}")
    print(f"  Armor  : {armor}")
    print(f"  Gold   : {player['gold']} g")


def show_skills(player: dict):
    """Display the player's skills with mana costs."""
    utils.subheader("  YOUR SKILLS")
    for i, skill in enumerate(player["skills"], 1):
        cost = skill.get("mana_cost", 0)
        if skill["type"] == "attack":
            effect = f"{skill.get('damage', 0)} damage"
        else:
            effect = f"+{skill.get('defense_bonus', 0)} DEF for 1 turn"
        print(f"  [{i}] {skill['name']} — {effect}  (Cost: {cost} MP)")
    print(f"\n  Current MP: {player['mp']}/{player['max_mp']}")


# -----------------------------------------------------------------------------
# Alive Check
# -----------------------------------------------------------------------------

def is_alive(player: dict) -> bool:
    """Return True if the player's HP is above 0."""
    return player["hp"] > 0


def die(player: dict):
    """Handle player death: print game-over screen and exit."""
    utils.header("YOU HAVE FALLEN")
    print()
    print(f"  {player['name']} the {player['class']} has perished in the dungeon.")
    print("  The darkness swallows you whole.")
    print()
    print("  ╔═══════════════════════════════╗")
    print("  ║         G A M E  O V E R      ║")
    print("  ╚═══════════════════════════════╝")
    print()
    sys.exit(0)