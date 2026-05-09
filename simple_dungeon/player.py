# player.py - Player creation
# Asks for name, picks a class, gives starting weapon.

import copy
import data


def create_player():
    """Ask the player for their name and class, then return a player dict."""

    print("\n" + "=" * 40)
    print("  WELCOME TO THE DUNGEON")
    print("=" * 40)

    # Get name
    name = input("\n  Enter your name: ").strip()
    if name == "":
        name = "Adventurer"

    # Show classes
    print("\n  Choose your class:")
    for key, cls in data.CLASSES.items():
        print(f"    {key}. {cls['name']} - HP:{cls['hp']} MP:{cls['mp']} ATK:{cls['attack']} DEF:{cls['defense']}")
        skill_names = ", ".join(s["name"] for s in cls["skills"])
        print(f"       Skills: {skill_names}")

    # Pick a class
    while True:
        choice = input("\n  Pick a class (1/2/3): ").strip()
        if choice in data.CLASSES:
            break
        print("  Invalid choice. Try again.")

    chosen = data.CLASSES[choice]

    # Build the player dict
    # copy.deepcopy makes a copy so we don't change the original data
    player = {
        "name": name,
        "class": chosen["name"],
        "hp": chosen["hp"],
        "max_hp": chosen["max_hp"],
        "mp": chosen["mp"],
        "max_mp": chosen["max_mp"],
        "attack": chosen["attack"],
        "defense": chosen["defense"],
        "skills": copy.deepcopy(chosen["skills"]),
        "inventory": [],
        "weapon": "",
        "armor": "",
        "gold": 0
    }

    # Give starting weapon and equip it
    weapon_name = chosen["starting_weapon"]
    weapon_data = data.ITEMS[weapon_name]
    player["weapon"] = weapon_name
    player["attack"] = player["attack"] + weapon_data["attack"]

    print(f"\n  Welcome, {name} the {player['class']}!")
    print(f"  Weapon equipped: {weapon_name} ({weapon_data['description']})")
    print("  Your adventure begins...\n")

    return player
