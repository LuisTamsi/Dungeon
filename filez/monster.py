# monster.py
# All monster definitions split into tiers: easy, intermediate, boss.
# Each fight gets a fresh deep copy via get_monster().

import copy
import random

# ---------------------------------------------------------------------------
# Monster Templates
# ---------------------------------------------------------------------------

MONSTER_TEMPLATES = {

    # ---- EASY TIER ----

    "goblin": {
        "id": "goblin",
        "name": "Goblin",
        "tier": "easy",
        "lore": "A cowardly little pest. Dangerous only if you ignore it.",
        "hp": 28, "max_hp": 28,
        "attack": 6, "defense": 2,
        "weapon": {"name": "Rusty Knife", "attack_bonus": 1},
        "gold_drop": (3, 8),
        "loot_table": [("rusty_sword", 0.25), ("health_potion", 0.35)],
        "is_boss": False,
        "skills": [
            {"name": "Cheap Shot",  "description": "A quick dirty hit.",      "type": "damage",  "multiplier": 1.5, "mp_cost": 0, "cooldown": 2, "current_cooldown": 0},
        ],
    },

    "bat": {
        "id": "bat",
        "name": "Giant Bat",
        "tier": "easy",
        "lore": "Blind and frantic. Its claws are sharper than they look.",
        "hp": 22, "max_hp": 22,
        "attack": 7, "defense": 1,
        "weapon": {"name": "Sharp Claws", "attack_bonus": 2},
        "gold_drop": (2, 6),
        "loot_table": [("health_potion", 0.3)],
        "is_boss": False,
        "skills": [
            {"name": "Screech",     "description": "Disorienting screech. Reduces player ATK by 2 for 2 turns.", "type": "debuff_attack", "bonus": -2, "duration": 2, "cooldown": 3, "current_cooldown": 0},
        ],
    },

    "slime": {
        "id": "slime",
        "name": "Slime",
        "tier": "easy",
        "lore": "A slow oozing blob. Hard to kill cleanly.",
        "hp": 35, "max_hp": 35,
        "attack": 5, "defense": 4,
        "weapon": {"name": "Acidic Touch", "attack_bonus": 0},
        "gold_drop": (2, 5),
        "loot_table": [("health_potion", 0.2), ("mana_vial", 0.2)],
        "is_boss": False,
        "skills": [
            {"name": "Acid Splash", "description": "Corrodes armor. Reduces player DEF by 2 for 2 turns.", "type": "debuff_defense", "bonus": -2, "duration": 2, "cooldown": 3, "current_cooldown": 0},
        ],
    },

    # ---- INTERMEDIATE TIER ----

    "skeleton": {
        "id": "skeleton",
        "name": "Skeleton Warrior",
        "tier": "intermediate",
        "lore": "A reanimated soldier. Hollow eyes, muscle memory intact.",
        "hp": 55, "max_hp": 55,
        "attack": 12, "defense": 6,
        "weapon": {"name": "Bone Blade", "attack_bonus": 3},
        "gold_drop": (8, 16),
        "loot_table": [("iron_axe", 0.3), ("leather_vest", 0.3), ("health_potion", 0.4)],
        "is_boss": False,
        "skills": [
            {"name": "Bone Slash",  "description": "Heavy swing with a decayed blade.",          "type": "damage",  "multiplier": 1.8, "cooldown": 3, "current_cooldown": 0},
            {"name": "Rattle",      "description": "Shakes bones to intimidate. Player loses 1 turn.", "type": "stun_player", "cooldown": 5, "current_cooldown": 0},
        ],
    },

    "dark_mage": {
        "id": "dark_mage",
        "name": "Dark Mage",
        "tier": "intermediate",
        "lore": "Once a scholar, now corrupted. Attacks from range and drains life.",
        "hp": 50, "max_hp": 50,
        "attack": 15, "defense": 3,
        "weapon": {"name": "Cursed Wand", "attack_bonus": 4},
        "gold_drop": (10, 20),
        "loot_table": [("oak_staff", 0.35), ("mana_vial", 0.4), ("mage_robe", 0.25)],
        "is_boss": False,
        "skills": [
            {"name": "Shadow Bolt", "description": "Dark energy bolt. Ignores defense.",          "type": "magic",   "multiplier": 2.0, "cooldown": 3, "current_cooldown": 0},
            {"name": "Drain Life",  "description": "Steals HP. Heals self for half damage dealt.", "type": "drain",   "multiplier": 1.5, "cooldown": 4, "current_cooldown": 0},
        ],
    },

    "stone_golem": {
        "id": "stone_golem",
        "name": "Stone Golem",
        "tier": "intermediate",
        "lore": "Living rock. Each step shakes the floor. Built to outlast you.",
        "hp": 85, "max_hp": 85,
        "attack": 17, "defense": 12,
        "weapon": {"name": "Stone Fist", "attack_bonus": 2},
        "gold_drop": (15, 28),
        "loot_table": [("iron_shield", 0.35), ("chain_mail", 0.3), ("bone_sword", 0.2)],
        "is_boss": False,
        "skills": [
            {"name": "Quake Slam",  "description": "Slams the ground. Massive physical damage.",  "type": "damage",  "multiplier": 2.2, "cooldown": 4, "current_cooldown": 0},
            {"name": "Stone Skin",  "description": "Hardens shell. DEF +8 for 2 turns.",          "type": "buff_defense", "bonus": 8, "duration": 2, "cooldown": 5, "current_cooldown": 0},
        ],
    },

    # ---- BOSS TIER ----

    "shadow_lord": {
        "id": "shadow_lord",
        "name": "Shadow Lord",
        "tier": "boss",
        "lore": (
            "The ruler of this dungeon. An ancient being of pure darkness "
            "that has consumed entire kingdoms. Its presence warps reality."
        ),
        "hp": 220, "max_hp": 220,
        "attack": 26, "defense": 16,
        "weapon": {"name": "Void Scepter", "attack_bonus": 8},
        "gold_drop": (60, 100),
        "loot_table": [("doom_blade", 1.0), ("dark_armor", 0.8), ("mana_elixir", 1.0)],
        "is_boss": True,
        "skills": [
            {"name": "Shadow Wave",      "description": "Wave of darkness. 2x magic damage, ignores defense.",   "type": "magic",   "multiplier": 2.0, "cooldown": 3, "current_cooldown": 0},
            {"name": "Void Crush",       "description": "Collapses a void pocket. 3x physical damage.",          "type": "damage",  "multiplier": 3.0, "cooldown": 5, "current_cooldown": 0},
            {"name": "Dark Regeneration","description": "Regenerates 25 HP.",                                     "type": "heal",    "heal_amount": 25,  "cooldown": 6, "current_cooldown": 0},
        ],
    },
}

# Tier pools for random spawning
EASY_POOL =         ["goblin", "bat", "slime"]
INTERMEDIATE_POOL = ["skeleton", "dark_mage", "stone_golem"]


def get_monster(monster_id):
    """Return a fresh copy of a monster by ID."""
    template = MONSTER_TEMPLATES.get(monster_id)
    return copy.deepcopy(template) if template else None


def get_random_easy(count=1):
    """Return a list of random easy monster IDs."""
    return [random.choice(EASY_POOL) for _ in range(count)]


def get_random_intermediate(count=1):
    """Return a list of random intermediate monster IDs."""
    return [random.choice(INTERMEDIATE_POOL) for _ in range(count)]


def is_alive(monster):
    return monster["hp"] > 0


# ---------------------------------------------------------------------------
# Monster AI
# ---------------------------------------------------------------------------

def monster_take_turn(monster, player):
    """
    Execute the monster's turn. Returns a result dict describing what happened.
    Priority: use a skill (60% if ready), else basic attack.
    """
    # Tick cooldowns
    for skill in monster.get("skills", []):
        if skill["current_cooldown"] > 0:
            skill["current_cooldown"] -= 1

    # Check if monster is stunned
    if monster.get("stunned"):
        monster["stunned"] = False
        return {"msg": f"  {monster['name']} is stunned and skips its turn!", "type": "stun_skip"}

    # Tick poison on monster
    poison_msg = ""
    if monster.get("poison_turns", 0) > 0:
        dmg = monster["poison_dmg"]
        monster["hp"] -= dmg
        monster["poison_turns"] -= 1
        poison_msg = f"  {monster['name']} takes {dmg} poison damage! ({monster['poison_turns']} turns left)"
        if not is_alive(monster):
            return {"msg": poison_msg + f"\n  {monster['name']} dies from poison!", "type": "poison_kill"}

    # Tick monster ATK buff/debuff
    if monster.get("attack_buff_turns", 0) > 0:
        monster["attack_buff_turns"] -= 1
        if monster["attack_buff_turns"] == 0:
            monster["attack_buff"] = 0

    # Tick monster DEF buff
    if monster.get("defense_buff_turns", 0) > 0:
        monster["defense_buff_turns"] -= 1
        if monster["defense_buff_turns"] == 0:
            monster["defense_buff"] = 0

    ready_skills = [s for s in monster.get("skills", []) if s["current_cooldown"] == 0]

    if ready_skills and random.random() < 0.60:
        skill = random.choice(ready_skills)
        skill["current_cooldown"] = skill["cooldown"]
        result = _use_monster_skill(monster, player, skill)
    else:
        result = _basic_attack(monster, player)

    if poison_msg:
        result["msg"] = poison_msg + "\n" + result["msg"]
    return result


def _get_effective_attack(monster):
    return monster["attack"] + monster.get("attack_buff", 0) + monster["weapon"]["attack_bonus"]


def _get_effective_defense(monster):
    return monster["defense"] + monster.get("defense_buff", 0)


def _basic_attack(monster, player):
    if player.get("evade_next"):
        player["evade_next"] = False
        return {"msg": f"  {monster['name']} attacks but you evade completely!", "type": "miss"}

    raw = _get_effective_attack(monster)
    if player.get("shield_turns", 0) > 0:
        raw = max(1, raw // 2)

    player_def = player["defense"] + player.get("defense_debuff", 0)
    damage = max(1, raw - player_def)
    player["hp"] -= damage
    return {"msg": f"  {monster['name']} attacks you for {damage} damage!", "type": "damage", "amount": damage}


def _use_monster_skill(monster, player, skill):
    stype = skill["type"]
    name  = skill["name"]
    mname = monster["name"]

    if player.get("evade_next") and stype not in ("heal", "buff_defense"):
        player["evade_next"] = False
        return {"msg": f"  {mname} uses {name} but you evade!", "type": "miss"}

    raw_atk = _get_effective_attack(monster)
    player_def = player["defense"] + player.get("defense_debuff", 0)

    if stype == "damage":
        raw = int(raw_atk * skill["multiplier"])
        if player.get("shield_turns", 0) > 0:
            raw = max(1, raw // 2)
        damage = max(1, raw - player_def)
        player["hp"] -= damage
        return {"msg": f"  {mname} uses {name}! Deals {damage} damage!", "type": "damage", "amount": damage}

    elif stype == "magic":
        damage = int(raw_atk * skill["multiplier"])
        if player.get("shield_turns", 0) > 0:
            damage = max(1, damage // 2)
        player["hp"] -= damage
        return {"msg": f"  {mname} uses {name}! Magic deals {damage} (ignores defense)!", "type": "damage", "amount": damage}

    elif stype == "drain":
        raw = int(raw_atk * skill["multiplier"])
        if player.get("shield_turns", 0) > 0:
            raw = max(1, raw // 2)
        damage = max(1, raw - player_def)
        player["hp"] -= damage
        heal = damage // 2
        monster["hp"] = min(monster["hp"] + heal, monster["max_hp"])
        return {"msg": f"  {mname} uses {name}! Drains {damage} HP and heals {heal} HP!", "type": "drain"}

    elif stype == "buff_defense":
        bonus = skill.get("bonus", 5)
        dur   = skill.get("duration", 2)
        monster["defense_buff"] = bonus
        monster["defense_buff_turns"] = dur
        return {"msg": f"  {mname} uses {name}! DEF +{bonus} for {dur} turns.", "type": "buff"}

    elif stype == "debuff_attack":
        bonus = skill.get("bonus", -2)
        dur   = skill.get("duration", 2)
        player["attack_buff"] = player.get("attack_buff", 0) + bonus
        player["attack_buff_turns"] = dur
        return {"msg": f"  {mname} uses {name}! Your ATK reduced by {abs(bonus)} for {dur} turns.", "type": "debuff"}

    elif stype == "debuff_defense":
        bonus = skill.get("bonus", -2)
        dur   = skill.get("duration", 2)
        player["defense_debuff"] = player.get("defense_debuff", 0) + abs(bonus)
        player["defense_debuff_turns"] = dur
        return {"msg": f"  {mname} uses {name}! Your DEF reduced by {abs(bonus)} for {dur} turns.", "type": "debuff"}

    elif stype == "stun_player":
        player["stunned_turns"] = 1
        return {"msg": f"  {mname} uses {name}! You are stunned and will skip your next turn!", "type": "stun"}

    elif stype == "heal":
        amount = skill.get("heal_amount", 20)
        monster["hp"] = min(monster["hp"] + amount, monster["max_hp"])
        return {"msg": f"  {mname} uses {name}! Heals {amount} HP. HP: {monster['hp']}/{monster['max_hp']}.", "type": "heal"}

    return {"msg": f"  {mname} does something strange...", "type": "unknown"}


# ---------------------------------------------------------------------------
# Loot
# ---------------------------------------------------------------------------

def roll_loot(monster):
    """Return list of item IDs that dropped based on loot_table probabilities."""
    drops = []
    for item_id, chance in monster.get("loot_table", []):
        if random.random() < chance:
            drops.append(item_id)
    return drops


def roll_gold(monster):
    low, high = monster["gold_drop"]
    return random.randint(low, high)
