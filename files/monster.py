# monster.py
# Defines all monster types.
# Monsters are returned as dictionaries so each encounter
# is a fresh independent copy (no shared state between fights).

import copy
import random

# --- Monster Templates ---
# These are blueprints. get_monster() returns a fresh copy.

MONSTER_TEMPLATES = {

    # --- Common Monsters ---

    "goblin": {
        "id": "goblin",
        "name": "Goblin",
        "type": "Common",
        "lore": "A small, cowardly creature that travels in packs. Dangerous only in numbers.",
        "hp": 30,
        "max_hp": 30,
        "attack": 6,
        "defense": 2,
        "gold_drop": (2, 8),
        "loot_table": ["rusty_sword", "health_potion"],
        "loot_chance": 0.4,
        "skills": [
            {
                "name": "Cheap Shot",
                "description": "A quick dirty hit.",
                "cooldown": 3,
                "current_cooldown": 0,
                "type": "damage",
                "multiplier": 1.5,
            }
        ],
        "is_boss": False,
    },

    "skeleton": {
        "id": "skeleton",
        "name": "Skeleton Warrior",
        "type": "Undead",
        "lore": "A reanimated soldier. Hollow eyes, hollow purpose. Still knows how to fight.",
        "hp": 45,
        "max_hp": 45,
        "attack": 10,
        "defense": 5,
        "gold_drop": (5, 12),
        "loot_table": ["iron_axe", "leather_vest", "health_potion"],
        "loot_chance": 0.5,
        "skills": [
            {
                "name": "Bone Slash",
                "description": "Swings its decayed blade with surprising force.",
                "cooldown": 3,
                "current_cooldown": 0,
                "type": "damage",
                "multiplier": 1.8,
            }
        ],
        "is_boss": False,
    },

    "dark_mage": {
        "id": "dark_mage",
        "name": "Dark Mage",
        "type": "Caster",
        "lore": "Once a scholar, now corrupted by forbidden texts. Extremely dangerous at range.",
        "hp": 55,
        "max_hp": 55,
        "attack": 14,
        "defense": 3,
        "gold_drop": (8, 18),
        "loot_table": ["oak_staff", "mage_robe", "elixir"],
        "loot_chance": 0.6,
        "skills": [
            {
                "name": "Shadow Bolt",
                "description": "A bolt of pure dark energy. Ignores defense.",
                "cooldown": 3,
                "current_cooldown": 0,
                "type": "magic",
                "multiplier": 2.0,
            },
            {
                "name": "Drain Life",
                "description": "Steals HP from the target.",
                "cooldown": 5,
                "current_cooldown": 0,
                "type": "drain",
                "multiplier": 1.5,
            },
        ],
        "is_boss": False,
    },

    "stone_golem": {
        "id": "stone_golem",
        "name": "Stone Golem",
        "type": "Elite",
        "lore": "A creature of living rock. Slow, but each hit feels like a falling boulder.",
        "hp": 90,
        "max_hp": 90,
        "attack": 18,
        "defense": 12,
        "gold_drop": (15, 30),
        "loot_table": ["iron_shield", "dark_armor", "bone_sword"],
        "loot_chance": 0.7,
        "skills": [
            {
                "name": "Quake Slam",
                "description": "Slams the ground. Deals massive damage.",
                "cooldown": 4,
                "current_cooldown": 0,
                "type": "damage",
                "multiplier": 2.2,
            },
            {
                "name": "Stone Skin",
                "description": "Hardens its shell. Reduces incoming damage for 2 turns.",
                "cooldown": 5,
                "current_cooldown": 0,
                "type": "shield",
                "multiplier": 0,
                "duration": 2,
            },
        ],
        "is_boss": False,
    },

    # --- Boss ---

    "shadow_lord": {
        "id": "shadow_lord",
        "name": "Shadow Lord",
        "type": "BOSS",
        "lore": (
            "The ruler of this dungeon. An ancient being of pure darkness "
            "that has consumed entire kingdoms. Its presence warps reality itself."
        ),
        "hp": 200,
        "max_hp": 200,
        "attack": 25,
        "defense": 15,
        "gold_drop": (50, 100),
        "loot_table": ["doom_blade", "dark_armor", "elixir"],
        "loot_chance": 1.0,  # boss always drops loot
        "skills": [
            {
                "name": "Shadow Wave",
                "description": "A wave of darkness. Deals 2x attack. Ignores defense.",
                "cooldown": 3,
                "current_cooldown": 0,
                "type": "magic",
                "multiplier": 2.0,
            },
            {
                "name": "Void Crush",
                "description": "Crushes the target in a pocket of void. Deals 3x attack.",
                "cooldown": 5,
                "current_cooldown": 0,
                "type": "damage",
                "multiplier": 3.0,
            },
            {
                "name": "Dark Regeneration",
                "description": "Regenerates 20 HP.",
                "cooldown": 6,
                "current_cooldown": 0,
                "type": "heal",
                "heal_amount": 20,
            },
        ],
        "is_boss": True,
    },
}


def get_monster(monster_id):
    """Return a fresh copy of a monster by ID."""
    template = MONSTER_TEMPLATES.get(monster_id)
    if template:
        return copy.deepcopy(template)
    return None


def is_alive(monster):
    """Return True if the monster still has HP."""
    return monster["hp"] > 0


def monster_take_turn(monster, player):
    """
    Decide and execute the monster's action for this turn.
    Returns a description string of what happened.
    Priority: use a skill if cooldown is ready, else basic attack.
    """
    # Tick down monster skill cooldowns
    for skill in monster.get("skills", []):
        if skill["current_cooldown"] > 0:
            skill["current_cooldown"] -= 1

    # Find a usable skill (cooldown == 0)
    ready_skills = [s for s in monster.get("skills", []) if s["current_cooldown"] == 0]

    # Random chance to use a skill vs basic attack (60% skill if available)
    if ready_skills and random.random() < 0.6:
        skill = random.choice(ready_skills)
        skill["current_cooldown"] = skill["cooldown"]
        return _use_monster_skill(monster, player, skill)
    else:
        return _basic_attack(monster, player)


def _basic_attack(monster, player):
    """Monster performs a basic attack on the player."""
    # Check if player is evading
    if player.get("evade_next"):
        player["evade_next"] = False
        return f"  {monster['name']} attacks but you evade completely!"

    raw = monster["attack"]
    defense = player["defense"]

    # Apply player shield if active
    if player.get("shield_turns", 0) > 0:
        raw = int(raw * 0.5)
        player["shield_turns"] -= 1

    damage = max(1, raw - defense)
    player["hp"] -= damage
    return f"  {monster['name']} attacks you for {damage} damage!"


def _use_monster_skill(monster, player, skill):
    """Execute a specific monster skill."""
    if player.get("evade_next") and skill["type"] != "heal":
        player["evade_next"] = False
        return f"  {monster['name']} uses {skill['name']} but you evade!"

    stype = skill["type"]

    if stype == "damage":
        raw = int(monster["attack"] * skill["multiplier"])
        if player.get("shield_turns", 0) > 0:
            raw = int(raw * 0.5)
            player["shield_turns"] -= 1
        damage = max(1, raw - player["defense"])
        player["hp"] -= damage
        return f"  {monster['name']} uses {skill['name']}! Deals {damage} damage!"

    elif stype == "magic":
        # Magic ignores defense
        raw = int(monster["attack"] * skill["multiplier"])
        if player.get("shield_turns", 0) > 0:
            raw = int(raw * 0.5)
            player["shield_turns"] -= 1
        player["hp"] -= raw
        return f"  {monster['name']} uses {skill['name']}! Magic deals {raw} damage (ignores defense)!"

    elif stype == "drain":
        raw = int(monster["attack"] * skill["multiplier"])
        damage = max(1, raw - player["defense"])
        player["hp"] -= damage
        heal = damage // 2
        monster["hp"] = min(monster["hp"] + heal, monster["max_hp"])
        return (
            f"  {monster['name']} uses {skill['name']}! "
            f"Drains {damage} HP from you and heals {heal} HP!"
        )

    elif stype == "shield":
        monster["shield_turns"] = skill.get("duration", 2)
        return f"  {monster['name']} uses {skill['name']}! Damage reduced for {monster['shield_turns']} turn(s)."

    elif stype == "heal":
        heal = skill.get("heal_amount", 0)
        monster["hp"] = min(monster["hp"] + heal, monster["max_hp"])
        return f"  {monster['name']} uses {skill['name']}! Heals {heal} HP. HP now {monster['hp']}/{monster['max_hp']}."

    return f"  {monster['name']} does something strange..."


def roll_loot(monster):
    """
    Roll for item drops from a monster.
    Returns a list of item IDs that dropped.
    """
    drops = []
    if not monster["loot_table"]:
        return drops
    if random.random() < monster["loot_chance"]:
        drop_id = random.choice(monster["loot_table"])
        drops.append(drop_id)
    return drops


def roll_gold(monster):
    """Return a random gold amount in the monster's drop range."""
    low, high = monster["gold_drop"]
    return random.randint(low, high)
