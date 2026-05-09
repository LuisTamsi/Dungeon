# player.py
# Handles everything about the player:
# creation, stats, inventory, skills, and equipped items.

from items import get_item, describe_item

# --- Class Definitions ---
# Each class is a dictionary of base stats and a list of skills.
# Skills are referenced by name and handled in combat.py.

CLASSES = {
    "1": {
        "name": "Warrior",
        "hp": 120,
        "max_hp": 120,
        "attack": 15,
        "defense": 10,
        "description": "Tough and hard-hitting. Built for the front line.",
        "skills": [
            {
                "name": "Power Strike",
                "description": "Deal 2x your attack as damage.",
                "cooldown": 3,
                "current_cooldown": 0,
                "type": "damage",
                "multiplier": 2.0,
            },
            {
                "name": "Shield Bash",
                "description": "Deal 1x attack and stun the enemy for 1 turn.",
                "cooldown": 4,
                "current_cooldown": 0,
                "type": "stun",
                "multiplier": 1.0,
            },
        ],
    },
    "2": {
        "name": "Rogue",
        "hp": 90,
        "max_hp": 90,
        "attack": 18,
        "defense": 6,
        "description": "Fast and precise. High damage, low defense.",
        "skills": [
            {
                "name": "Backstab",
                "description": "Deal 2.5x your attack as damage.",
                "cooldown": 4,
                "current_cooldown": 0,
                "type": "damage",
                "multiplier": 2.5,
            },
            {
                "name": "Smoke Bomb",
                "description": "Evade the next enemy attack entirely.",
                "cooldown": 5,
                "current_cooldown": 0,
                "type": "evade",
                "multiplier": 0,
            },
        ],
    },
    "3": {
        "name": "Mage",
        "hp": 80,
        "max_hp": 80,
        "attack": 20,
        "defense": 4,
        "description": "Powerful spells, fragile body. High risk, high reward.",
        "skills": [
            {
                "name": "Fireball",
                "description": "Deal 3x your attack as magic damage. Ignores defense.",
                "cooldown": 4,
                "current_cooldown": 0,
                "type": "magic",
                "multiplier": 3.0,
            },
            {
                "name": "Frost Shield",
                "description": "Reduce incoming damage by 50% for 2 turns.",
                "cooldown": 5,
                "current_cooldown": 0,
                "type": "shield",
                "multiplier": 0,
                "duration": 2,
            },
        ],
    },
}


def create_player():
    """Walk the player through character creation and return a player dict."""
    print("\n" + "=" * 50)
    print("  DUNGEON OF SHADOWS")
    print("=" * 50)
    print("\nEnter your character's name:")
    name = input("  > ").strip()
    if not name:
        name = "Adventurer"

    print("\nChoose your class:")
    for key, cls in CLASSES.items():
        print(f"  [{key}] {cls['name']} - {cls['description']}")
        print(f"       HP: {cls['hp']}  ATK: {cls['attack']}  DEF: {cls['defense']}")

    choice = ""
    while choice not in CLASSES:
        choice = input("\n  > ").strip()
        if choice not in CLASSES:
            print("  Pick 1, 2, or 3.")

    chosen = CLASSES[choice]

    # Build the player dict from the chosen class.
    # We do a deep copy of skills so cooldowns are independent per game.
    import copy
    player = {
        "name": name,
        "class": chosen["name"],
        "hp": chosen["hp"],
        "max_hp": chosen["max_hp"],
        "attack": chosen["attack"],
        "defense": chosen["defense"],
        "base_attack": chosen["attack"],
        "base_defense": chosen["defense"],
        "skills": copy.deepcopy(chosen["skills"]),
        "inventory": [],
        "weapon": None,   # currently equipped weapon
        "armor": None,    # currently equipped armor
        "gold": 0,
        "shield_turns": 0,     # tracks Frost Shield duration
        "evade_next": False,   # tracks Smoke Bomb evade
        "stunned": False,      # not used for player, but kept for symmetry
    }

    print(f"\nWelcome, {player['name']} the {player['class']}!")
    print("Your journey begins...\n")
    return player

def is_alive(player):
    """Return True if the player is still alive."""
    return player["hp"] > 0

