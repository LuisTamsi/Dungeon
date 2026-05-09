# player.py
# Player creation, stats, mana, inventory, skills, equip, and shop.

import copy
from items import get_item

# ---------------------------------------------------------------------------
# Class Definitions
# Each class has: hp, mana (mp), attack, defense, and 2-3 skills.
# Skills cost mana. No mana = no skills. Only items restore mana.
# ---------------------------------------------------------------------------

CLASSES = {
    "1": {
        "name": "Warrior",
        "hp": 130, "max_hp": 130,
        "mp": 60,  "max_mp": 60,
        "attack": 15, "defense": 10,
        "description": "Tough front-liner. Reliable damage, high survivability.",
        "skills": [
            {
                "name": "Power Strike",
                "description": "Deal 2x ATK as physical damage.",
                "mp_cost": 10,
                "type": "damage",
                "multiplier": 2.0,
            },
            {
                "name": "Shield Bash",
                "description": "Deal 1x ATK and stun the enemy for 1 turn.",
                "mp_cost": 15,
                "type": "stun",
                "multiplier": 1.0,
            },
            {
                "name": "War Cry",
                "description": "Boost your ATK by 5 for 3 turns.",
                "mp_cost": 20,
                "type": "buff_attack",
                "bonus": 5,
                "duration": 3,
            },
        ],
    },

    "2": {
        "name": "Rogue",
        "hp": 95,  "max_hp": 95,
        "mp": 70,  "max_mp": 70,
        "attack": 18, "defense": 6,
        "description": "Fast and precise. High damage, fragile body.",
        "skills": [
            {
                "name": "Backstab",
                "description": "Deal 2.5x ATK as physical damage.",
                "mp_cost": 12,
                "type": "damage",
                "multiplier": 2.5,
            },
            {
                "name": "Smoke Bomb",
                "description": "Evade the next enemy attack entirely.",
                "mp_cost": 15,
                "type": "evade",
                "multiplier": 0,
            },
            {
                "name": "Poison Blade",
                "description": "Deal 1x ATK and poison the enemy (5 dmg/turn for 3 turns).",
                "mp_cost": 18,
                "type": "poison",
                "multiplier": 1.0,
                "poison_dmg": 5,
                "poison_turns": 3,
            },
        ],
    },

    "3": {
        "name": "Mage",
        "hp": 80,  "max_hp": 80,
        "mp": 100, "max_mp": 100,
        "attack": 20, "defense": 4,
        "description": "Powerful magic, fragile body. Biggest mana pool.",
        "skills": [
            {
                "name": "Fireball",
                "description": "Deal 3x ATK as magic damage (ignores defense).",
                "mp_cost": 20,
                "type": "magic",
                "multiplier": 3.0,
            },
            {
                "name": "Frost Shield",
                "description": "Reduce all incoming damage by 50% for 2 turns.",
                "mp_cost": 15,
                "type": "shield",
                "duration": 2,
            },
            {
                "name": "Chain Lightning",
                "description": "Deal 2x ATK as magic damage twice (ignores defense).",
                "mp_cost": 25,
                "type": "magic_double",
                "multiplier": 2.0,
            },
        ],
    },
}


def create_player():
    """Walk the player through character creation and return a player dict."""
    print("\n" + "=" * 55)
    print("       DUNGEON OF SHADOWS")
    print("=" * 55)
    print("\nEnter your character's name:")
    name = input("  > ").strip() or "Adventurer"

    print("\nChoose your class:\n")
    for key, cls in CLASSES.items():
        print(f"  [{key}] {cls['name']}  -  {cls['description']}")
        print(f"       HP: {cls['hp']}  MP: {cls['mp']}  ATK: {cls['attack']}  DEF: {cls['defense']}")
        print(f"       Skills: {', '.join(s['name'] for s in cls['skills'])}\n")

    choice = ""
    while choice not in CLASSES:
        choice = input("  Pick a class (1/2/3): ").strip()

    chosen = CLASSES[choice]
    player = {
        "name": name,
        "class": chosen["name"],
        "hp": chosen["hp"],
        "max_hp": chosen["max_hp"],
        "mp": chosen["mp"],
        "max_mp": chosen["max_mp"],
        "attack": chosen["attack"],
        "defense": chosen["defense"],
        "base_attack": chosen["attack"],
        "base_defense": chosen["defense"],
        "skills": copy.deepcopy(chosen["skills"]),
        "inventory": [],
        "weapon": None,
        "armor": None,
        "gold": 0,
        # Combat state flags
        "shield_turns": 0,
        "evade_next": False,
        "attack_buff": 0,
        "attack_buff_turns": 0,
    }

    print(f"\n  Welcome, {player['name']} the {player['class']}!")
    print("  Your journey into the dungeon begins.\n")
    return player


# ---------------------------------------------------------------------------
# Combat state helpers
# ---------------------------------------------------------------------------

def tick_combat_state(player):
    """Call at end of each combat turn to tick buff durations."""
    if player.get("shield_turns", 0) > 0:
        player["shield_turns"] -= 1

    if player.get("attack_buff_turns", 0) > 0:
        player["attack_buff_turns"] -= 1
        if player["attack_buff_turns"] == 0:
            player["attack_buff"] = 0
            print("  Your War Cry buff fades.")


def is_alive(player):
    return player["hp"] > 0


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _valid_index(lst, index):
    if index < 0 or index >= len(lst):
        print("  Invalid number.")
        return False
    return True
