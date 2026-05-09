# =============================================================================
# monster.py — Monster Spawning and Monster Actions
# Handles creating independent monster instances and the monster's combat AI.
# =============================================================================

import copy
import random

import data
import utils


# -----------------------------------------------------------------------------
# Spawning
# -----------------------------------------------------------------------------

def spawn_monster(tier: str) -> dict:
    """
    Pick a random monster of the given tier from data.MONSTERS and return
    a deep copy so that each fight is independent — killing a goblin does not
    modify the template and future goblins spawn at full HP.

    Why deepcopy: the monster dict contains mutable lists (skills). Without
    deepcopy, changes to one monster instance (e.g. tracking cooldowns later)
    would bleed into every other monster of the same type.
    """
    pool = [
        m for m in data.MONSTERS.values()
        if m["tier"] == tier
    ]
    if not pool:
        raise ValueError(f"No monsters found for tier: '{tier}'")

    template = random.choice(pool)
    monster = copy.deepcopy(template)
    return monster


def spawn_boss() -> dict:
    """Spawn the unique boss monster (Dungeon Lord)."""
    template = data.MONSTERS["Dungeon Lord"]
    return copy.deepcopy(template)


def is_alive(monster: dict) -> bool:
    """Return True if the monster still has HP > 0."""
    return monster["hp"] > 0


# -----------------------------------------------------------------------------
# Monster Combat AI
# -----------------------------------------------------------------------------

def choose_skill(monster: dict) -> dict:
    """
    Randomly select a skill the monster can afford (has enough MP for).
    Falls back to the first skill (always 0 mana cost for easy monsters) if
    none are affordable — ensuring the monster always acts.

    Why random: Unpredictability keeps fights interesting. If the monster always
    used the same skill, the player would solve the fight once and it would never
    be interesting again.
    """
    affordable = [
        s for s in monster["skills"]
        if monster["mp"] >= s.get("mana_cost", 0)
    ]
    if not affordable:
        # Safety fallback — use cheapest skill regardless
        affordable = sorted(monster["skills"], key=lambda s: s.get("mana_cost", 0))
        return affordable[0]

    return random.choice(affordable)


def execute_turn(monster: dict, player: dict):
    """
    Execute the monster's turn:
    1. Choose a skill
    2. Apply its effect (attack, defense buff, or drain)
    3. Deduct mana cost
    4. Print the action narrative

    Defense buffs on monsters last only one turn — we apply a temp bonus
    and it resets at the start of the next monster turn (handled here).
    """
    # Reset any temporary defense bonus from the last turn
    if monster.get("_temp_defense", 0) > 0:
        monster["defense"] -= monster["_temp_defense"]
        monster["_temp_defense"] = 0

    skill = choose_skill(monster)
    monster["mp"] = max(0, monster["mp"] - skill.get("mana_cost", 0))

    stype = skill.get("type", "attack")

    utils.blank()
    print(f"  ⚔  {monster['name']} uses {skill['name']}!")
    print(f"     \"{skill['description']}\"")

    if stype == "defense":
        bonus = skill.get("defense_bonus", 0)
        monster["defense"] += bonus
        monster["_temp_defense"] = bonus
        utils.info(f"{monster['name']}'s defense increased by {bonus} this turn!")

    elif stype == "drain":
        # Soul Drain: deals damage AND heals the monster
        raw_damage = skill.get("damage", 0)
        damage = max(1, raw_damage - player["defense"])
        player["hp"] = max(0, player["hp"] - damage)
        heal = skill.get("heal", 0)
        monster["hp"] = min(monster["max_hp"], monster["hp"] + heal)
        utils.info(
            f"{monster['name']} drains your life for {damage} damage "
            f"and heals {heal} HP!"
        )

    else:  # attack
        raw_damage = skill.get("damage", 0)
        damage = max(1, raw_damage - player["defense"])
        player["hp"] = max(0, player["hp"] - damage)
        utils.info(f"You take {damage} damage! (HP: {player['hp']}/{player['max_hp']})")


# -----------------------------------------------------------------------------
# Loot
# -----------------------------------------------------------------------------

def roll_loot(monster: dict) -> list[str]:
    """
    Roll against each entry in the monster's loot_table.
    Returns a list of item names that dropped (can be empty).

    Why per-item rolls: each loot entry is independent, so a monster could
    theoretically drop multiple items (e.g. Dark Elf drops armor AND a potion).
    """
    drops = []
    for entry in monster.get("loot_table", []):
        if random.random() <= entry["chance"]:
            drops.append(entry["item"])
    return drops


def roll_gold(monster: dict) -> int:
    """Roll a random gold amount within the monster's gold_drop range."""
    low, high = monster.get("gold_drop", [0, 0])
    return random.randint(low, high)


# -----------------------------------------------------------------------------
# Display
# -----------------------------------------------------------------------------

def display_monster(monster: dict):
    """Print monster name, lore description, and current stats."""
    utils.subheader(f"  {monster['name']}")
    utils.info(monster["description"])
    utils.separator()
    utils.display_stats(monster)
