# =============================================================================
# data.py — Game Data Constants
# All static game data lives here. No logic, no functions — only definitions.
# Every other module imports from this file. Change stats/loot here, not in code.
# =============================================================================

# -----------------------------------------------------------------------------
# CLASSES — Player class templates
# Each class defines base stats and starting skills.
# deepcopy is done in player.py so changes to a player never affect this template.
# -----------------------------------------------------------------------------
CLASSES = {
    "1": {
        "name": "Warrior",
        "description": "A battle-hardened fighter. High HP and defense, strong melee skills.",
        "hp": 120,
        "max_hp": 120,
        "mp": 40,
        "max_mp": 40,
        "base_attack": 15,
        "base_defense": 12,
        "starting_weapon": "Rusty Longsword",
        "skills": [
            {
                "name": "Power Strike",
                "description": "A heavy blow that deals massive damage.",
                "damage": 25,
                "mana_cost": 15,
                "type": "attack"
            },
            {
                "name": "Shield Wall",
                "description": "Raise your shield to absorb the next hit.",
                "defense_bonus": 15,
                "mana_cost": 10,
                "type": "defense"
            },
            {
                "name": "Battle Cry",
                "description": "A thunderous roar that empowers your strike.",
                "damage": 30,
                "mana_cost": 15,
                "type": "attack"
            }
        ]
    },
    "2": {
        "name": "Mage",
        "description": "A master of the arcane. Fragile body, devastating magic, huge mana pool.",
        "hp": 70,
        "max_hp": 70,
        "mp": 150,
        "max_mp": 150,
        "base_attack": 5,
        "base_defense": 6,
        "starting_weapon": "Wooden Staff",
        "skills": [
            {
                "name": "Fireball",
                "description": "Hurl a blazing ball of fire at the enemy.",
                "damage": 35,
                "mana_cost": 20,
                "type": "attack"
            },
            {
                "name": "Ice Shield",
                "description": "Encase yourself in magical ice to reduce damage.",
                "defense_bonus": 20,
                "mana_cost": 15,
                "type": "defense"
            },
            {
                "name": "Lightning Bolt",
                "description": "Call down a bolt of lightning for massive damage.",
                "damage": 45,
                "mana_cost": 30,
                "type": "attack"
            }
        ]
    },
    "3": {
        "name": "Archer",
        "description": "A nimble ranger. Balanced stats with a variety of ranged skills.",
        "hp": 90,
        "max_hp": 90,
        "mp": 80,
        "max_mp": 80,
        "base_attack": 12,
        "base_defense": 8,
        "starting_weapon": "Shortbow",
        "skills": [
            {
                "name": "Arrow Shot",
                "description": "A precise arrow aimed at a weak spot.",
                "damage": 20,
                "mana_cost": 10,
                "type": "attack"
            },
            {
                "name": "Poison Arrow",
                "description": "An arrow coated in venom. Deals extra damage.",
                "damage": 25,
                "mana_cost": 15,
                "type": "attack"
            },
            {
                "name": "Evasive Trap",
                "description": "Set a trap and fall back, boosting your defense.",
                "defense_bonus": 15,
                "mana_cost": 20,
                "type": "defense"
            }
        ]
    }
}

# -----------------------------------------------------------------------------
# ITEMS — All items in the game
# item_type: "weapon" | "armor" | "consumable"
# Weapons and armors are equip-and-persist; consumables are use-and-gone.
# -----------------------------------------------------------------------------
ITEMS = {
    # --- Consumables ---
    "Health Potion": {
        "name": "Health Potion",
        "description": "A red vial that restores 40 HP.",
        "item_type": "consumable",
        "hp_restore": 40,
        "mp_restore": 0,
        "value": 15
    },
    "Mana Potion": {
        "name": "Mana Potion",
        "description": "A blue vial that restores 30 MP.",
        "item_type": "consumable",
        "hp_restore": 0,
        "mp_restore": 30,
        "value": 20
    },

    # --- Starting Weapons (weaker — loot upgrades these) ---
    "Rusty Longsword": {
        "name": "Rusty Longsword",
        "description": "An old sword, still sharp enough to hurt.",
        "item_type": "weapon",
        "attack_bonus": 5,
        "value": 0
    },
    "Wooden Staff": {
        "name": "Wooden Staff",
        "description": "A gnarled staff that channels magical energy.",
        "item_type": "weapon",
        "attack_bonus": 3,
        "value": 0
    },
    "Shortbow": {
        "name": "Shortbow",
        "description": "A compact bow suited for close-quarters dungeon combat.",
        "item_type": "weapon",
        "attack_bonus": 4,
        "value": 0
    },

    # --- Loot Weapons ---
    "Iron Sword": {
        "name": "Iron Sword",
        "description": "A sturdy iron blade. A solid upgrade.",
        "item_type": "weapon",
        "attack_bonus": 8,
        "value": 30
    },
    "Steel Sword": {
        "name": "Steel Sword",
        "description": "A finely forged steel sword. Deadly in skilled hands.",
        "item_type": "weapon",
        "attack_bonus": 15,
        "value": 60
    },

    # --- Loot Armors ---
    "Leather Armor": {
        "name": "Leather Armor",
        "description": "Light leather padding that offers basic protection.",
        "item_type": "armor",
        "defense_bonus": 5,
        "value": 25
    },
    "Iron Armor": {
        "name": "Iron Armor",
        "description": "Heavy iron plating. Excellent protection, but slow.",
        "item_type": "armor",
        "defense_bonus": 12,
        "value": 80
    }
}

# -----------------------------------------------------------------------------
# MONSTERS — All monster templates
# tier: "easy" | "intermediate" | "boss"
# loot_table: list of {"item": item_name, "chance": 0.0-1.0}
# gold_drop: [min, max] range rolled on defeat
# deepcopy is done in monster.py when spawning so each fight is independent.
# -----------------------------------------------------------------------------
MONSTERS = {
    # --- Easy Tier ---
    "Goblin": {
        "name": "Goblin",
        "description": "A cowardly little pest. Dangerous only in numbers.",
        "tier": "easy",
        "hp": 40,
        "max_hp": 40,
        "mp": 10,
        "max_mp": 10,
        "attack": 8,
        "defense": 2,
        "gold_drop": [8, 15],
        "is_boss": False,
        "loot_table": [],
        "skills": [
            {
                "name": "Cheap Shot",
                "description": "A sneaky, underhanded strike.",
                "damage": 10,
                "mana_cost": 0,
                "type": "attack"
            },
            {
                "name": "Quick Slash",
                "description": "A rapid slash with a rusty blade.",
                "damage": 12,
                "mana_cost": 0,
                "type": "attack"
            }
        ]
    },
    "Slime": {
        "name": "Slime",
        "description": "A gelatinous blob. Weak, but can drop useful items.",
        "tier": "easy",
        "hp": 30,
        "max_hp": 30,
        "mp": 0,
        "max_mp": 0,
        "attack": 5,
        "defense": 1,
        "gold_drop": [5, 12],
        "is_boss": False,
        "loot_table": [
            {"item": "Health Potion", "chance": 0.35}
        ],
        "skills": [
            {
                "name": "Acid Splash",
                "description": "Spits corrosive acid.",
                "damage": 8,
                "mana_cost": 0,
                "type": "attack"
            },
            {
                "name": "Body Slam",
                "description": "Hurls its gelatinous body at you.",
                "damage": 10,
                "mana_cost": 0,
                "type": "attack"
            }
        ]
    },

    # --- Intermediate Tier ---
    "Skeleton": {
        "name": "Skeleton",
        "description": "Reanimated by dark magic. Rattles with every step.",
        "tier": "intermediate",
        "hp": 80,
        "max_hp": 80,
        "mp": 20,
        "max_mp": 20,
        "attack": 13,
        "defense": 8,
        "gold_drop": [18, 28],
        "is_boss": False,
        "loot_table": [
            {"item": "Iron Sword", "chance": 0.25}
        ],
        "skills": [
            {
                "name": "Bone Smash",
                "description": "Slams you with a skeletal fist.",
                "damage": 18,
                "mana_cost": 0,
                "type": "attack"
            },
            {
                "name": "Dark Arrow",
                "description": "Fires a cursed arrow from a bone bow.",
                "damage": 22,
                "mana_cost": 10,
                "type": "attack"
            },
            {
                "name": "Bone Shield",
                "description": "Assembles loose bones into a makeshift shield.",
                "defense_bonus": 10,
                "mana_cost": 10,
                "type": "defense"
            }
        ]
    },
    "Dark Elf": {
        "name": "Dark Elf",
        "description": "A treacherous elf from the underdark. Quick and cunning.",
        "tier": "intermediate",
        "hp": 90,
        "max_hp": 90,
        "mp": 40,
        "max_mp": 40,
        "attack": 16,
        "defense": 10,
        "gold_drop": [22, 35],
        "is_boss": False,
        "loot_table": [
            {"item": "Leather Armor", "chance": 0.25},
            {"item": "Mana Potion", "chance": 0.20}
        ],
        "skills": [
            {
                "name": "Shadow Blade",
                "description": "Strikes from the shadows with enchanted daggers.",
                "damage": 24,
                "mana_cost": 10,
                "type": "attack"
            },
            {
                "name": "Hex Bolt",
                "description": "Fires a bolt of dark magic.",
                "damage": 28,
                "mana_cost": 15,
                "type": "attack"
            },
            {
                "name": "Dark Veil",
                "description": "Wraps in shadow to deflect attacks.",
                "defense_bonus": 12,
                "mana_cost": 10,
                "type": "defense"
            }
        ]
    },
    "Orc Warrior": {
        "name": "Orc Warrior",
        "description": "A massive green-skinned brute. Slow but hits like a boulder.",
        "tier": "intermediate",
        "hp": 110,
        "max_hp": 110,
        "mp": 15,
        "max_mp": 15,
        "attack": 18,
        "defense": 12,
        "gold_drop": [28, 40],
        "is_boss": False,
        "loot_table": [
            {"item": "Steel Sword", "chance": 0.20},
            {"item": "Health Potion", "chance": 0.25}
        ],
        "skills": [
            {
                "name": "Brutal Cleave",
                "description": "A wide, devastating swing of an axe.",
                "damage": 30,
                "mana_cost": 0,
                "type": "attack"
            },
            {
                "name": "War Shout",
                "description": "Lets out a terrifying battlecry before striking.",
                "damage": 26,
                "mana_cost": 0,
                "type": "attack"
            },
            {
                "name": "Iron Skin",
                "description": "Flexes, hardening skin against blows.",
                "defense_bonus": 15,
                "mana_cost": 15,
                "type": "defense"
            }
        ]
    },

    # --- Boss Tier ---
    "Dungeon Lord": {
        "name": "Dungeon Lord",
        "description": (
            "The supreme ruler of this dungeon. Ancient, cunning, and merciless. "
            "Defeat it and you are free."
        ),
        "tier": "boss",
        "hp": 220,
        "max_hp": 220,
        "mp": 80,
        "max_mp": 80,
        "attack": 22,
        "defense": 15,
        "gold_drop": [100, 100],
        "is_boss": True,
        "loot_table": [
            {"item": "Iron Armor", "chance": 1.0}
        ],
        "skills": [
            {
                "name": "Void Crush",
                "description": "Channels dark energy into a devastating smash.",
                "damage": 35,
                "mana_cost": 0,
                "type": "attack"
            },
            {
                "name": "Soul Drain",
                "description": "Siphons life force to restore own health.",
                "damage": 20,
                "heal": 20,
                "mana_cost": 20,
                "type": "drain"
            },
            {
                "name": "Cataclysm",
                "description": "Unleashes a wave of pure destructive force.",
                "damage": 45,
                "mana_cost": 30,
                "type": "attack"
            }
        ]
    }
}

# -----------------------------------------------------------------------------
# ROOMS — Dungeon layout
# difficulty: "easy" | "intermediate" | "boss" | "empty"
# monster_tier maps to a tier in MONSTERS for random spawning.
# cleared: False by default; set to True once all monsters in the room are dead.
# chest_opened: only relevant for the Treasure Vault.
# -----------------------------------------------------------------------------
ROOMS = {
    "entrance": {
        "name": "Dungeon Entrance",
        "description": (
            "You stand at the crumbling stone entrance of the dungeon. "
            "Torches flicker on the walls, casting long shadows. "
            "The air smells of damp stone and old blood."
        ),
        "difficulty": "easy",
        "monster_tier": "easy",
        "monster_count": 2,
        "exits": {
            "north": "goblin_tunnels"
        },
        "items": [],
        "monsters": [],
        "cleared": False,
        "is_boss_room": False
    },
    "goblin_tunnels": {
        "name": "Goblin Tunnels",
        "description": (
            "Narrow tunnels carved by goblin hands wind through the rock. "
            "Crude drawings smear the walls. Discarded bones crunch under your feet."
        ),
        "difficulty": "easy",
        "monster_tier": "easy",
        "monster_count": 2,
        "exits": {
            "south": "entrance",
            "east": "treasure_vault"
        },
        "items": [],
        "monsters": [],
        "cleared": False,
        "is_boss_room": False
    },
    "treasure_vault": {
        "name": "Treasure Vault",
        "description": (
            "A heavy iron door opens into a dusty vault. "
            "Gold coins glint in the corners. A large iron chest sits in the center of the room. "
            "No monsters — just forgotten riches."
        ),
        "difficulty": "empty",
        "monster_tier": None,
        "monster_count": 0,
        "exits": {
            "west": "goblin_tunnels",
            "east": "dark_corridor"
        },
        "items": [],
        "monsters": [],
        "cleared": True,
        "chest": {
            "opened": False,
            "contents": ["Health Potion", "Mana Potion", "Leather Armor"]
        },
        "is_boss_room": False
    },
    "dark_corridor": {
        "name": "Dark Corridor",
        "description": (
            "An oppressive darkness fills this long corridor. "
            "Strange runes glow faintly on the floor. "
            "The temperature drops sharply — something powerful is close."
        ),
        "difficulty": "intermediate",
        "monster_tier": "intermediate",
        "monster_count": 2,
        "exits": {
            "west": "treasure_vault",
            "north": "boss_chamber"
        },
        "items": [],
        "monsters": [],
        "cleared": False,
        "is_boss_room": False
    },
    "boss_chamber": {
        "name": "Boss Chamber",
        "description": (
            "Massive stone doors slam shut behind you. "
            "The chamber is vast, lit by an eerie green light. "
            "A colossal throne sits at the far end, and upon it sits the Dungeon Lord — "
            "watching you with ancient, merciless eyes."
        ),
        "difficulty": "boss",
        "monster_tier": "boss",
        "monster_count": 1,
        "exits": {
            "south": "dark_corridor"
        },
        "items": [],
        "monsters": [],
        "cleared": False,
        "is_boss_room": True
    }
}