# data.py - All game data (classes, items, monsters, rooms)
# This file just stores data. No logic here.

# ===== PLAYER CLASSES =====
CLASSES = {
    "1": {
        "name": "Warrior",
        "hp": 100, "max_hp": 100,
        "mp": 30, "max_mp": 30,
        "attack": 12, "defense": 8,
        "starting_weapon": "Iron Sword",
        "skills": [
            {"name": "Heavy Slash", "damage": 20, "cost": 10},
            {"name": "War Cry", "damage": 28, "cost": 15}
        ]
    },
    "2": {
        "name": "Mage",
        "hp": 60, "max_hp": 60,
        "mp": 100, "max_mp": 100,
        "attack": 5, "defense": 4,
        "starting_weapon": "Wooden Staff",
        "skills": [
            {"name": "Fireball", "damage": 30, "cost": 15},
            {"name": "Lightning", "damage": 45, "cost": 25}
        ]
    },
    "3": {
        "name": "Archer",
        "hp": 80, "max_hp": 80,
        "mp": 50, "max_mp": 50,
        "attack": 10, "defense": 6,
        "starting_weapon": "Short Bow",
        "skills": [
            {"name": "Power Shot", "damage": 22, "cost": 10},
            {"name": "Rain of Arrows", "damage": 32, "cost": 20}
        ]
    }
}

# ===== ITEMS =====
# type: "weapon", "armor", or "potion"
ITEMS = {
    "Health Potion": {"name": "Health Potion", "type": "potion", "hp_restore": 30, "description": "Restores 30 HP"},
    "Mana Potion": {"name": "Mana Potion", "type": "potion", "mp_restore": 25, "description": "Restores 25 MP"},
    "Iron Sword": {"name": "Iron Sword", "type": "weapon", "attack": 5, "description": "+5 ATK"},
    "Steel Sword": {"name": "Steel Sword", "type": "weapon", "attack": 10, "description": "+10 ATK"},
    "Wooden Staff": {"name": "Wooden Staff", "type": "weapon", "attack": 3, "description": "+3 ATK"},
    "Short Bow": {"name": "Short Bow", "type": "weapon", "attack": 4, "description": "+4 ATK"},
    "Leather Armor": {"name": "Leather Armor", "type": "armor", "defense": 4, "description": "+4 DEF"},
    "Iron Armor": {"name": "Iron Armor", "type": "armor", "defense": 8, "description": "+8 DEF"},
}

# ===== MONSTERS =====
# loot = list of possible drops. "chance" is probability from 0.0 to 1.0
MONSTERS = {
    "Goblin": {
        "name": "Goblin",
        "description": "A small green creature with a rusty dagger.",
        "hp": 30, "max_hp": 30, "attack": 7, "defense": 2,
        "is_boss": False, "gold": 10,
        "loot": [{"item": "Health Potion", "chance": 0.3}],
        "skills": [{"name": "Stab", "damage": 10}, {"name": "Scratch", "damage": 8}]
    },
    "Slime": {
        "name": "Slime",
        "description": "A wobbly blob of green goo. Weak but annoying.",
        "hp": 25, "max_hp": 25, "attack": 5, "defense": 1,
        "is_boss": False, "gold": 8,
        "loot": [{"item": "Mana Potion", "chance": 0.3}],
        "skills": [{"name": "Acid Spit", "damage": 8}, {"name": "Body Slam", "damage": 10}]
    },
    "Skeleton": {
        "name": "Skeleton",
        "description": "A pile of bones held together by dark magic.",
        "hp": 60, "max_hp": 60, "attack": 12, "defense": 6,
        "is_boss": False, "gold": 20,
        "loot": [{"item": "Iron Sword", "chance": 0.25}],
        "skills": [{"name": "Bone Strike", "damage": 15}, {"name": "Dark Slash", "damage": 18}]
    },
    "Dark Knight": {
        "name": "Dark Knight",
        "description": "A fallen warrior corrupted by darkness. Strong and armored.",
        "hp": 80, "max_hp": 80, "attack": 16, "defense": 10,
        "is_boss": False, "gold": 30,
        "loot": [{"item": "Leather Armor", "chance": 0.25}, {"item": "Steel Sword", "chance": 0.15}],
        "skills": [{"name": "Heavy Blow", "damage": 22}, {"name": "Shield Bash", "damage": 16}]
    },
    "Dragon Lord": {
        "name": "Dragon Lord",
        "description": "The ancient ruler of this dungeon. Massive, fire-breathing, and deadly.",
        "hp": 150, "max_hp": 150, "attack": 20, "defense": 12,
        "is_boss": True, "gold": 100,
        "loot": [{"item": "Iron Armor", "chance": 1.0}],
        "skills": [
            {"name": "Fire Breath", "damage": 28},
            {"name": "Tail Whip", "damage": 20},
            {"name": "Dark Flame", "damage": 35}
        ]
    }
}

# ===== ROOMS =====
# monsters = list of monster names to spawn when player first enters
# chest = list of items inside a chest (or None if no chest)
ROOMS = {
    "entrance": {
        "name": "Dungeon Entrance",
        "description": "A dark, cold entrance. Torches flicker on the stone walls.",
        "exits": {"north": "hallway"},
        "monsters": ["Goblin", "Slime"],
        "chest": None
    },
    "hallway": {
        "name": "Dark Hallway",
        "description": "A long, narrow corridor. Strange sounds echo from the shadows.",
        "exits": {"south": "entrance", "east": "treasure_room", "north": "boss_room"},
        "monsters": ["Skeleton", "Dark Knight"],
        "chest": None
    },
    "treasure_room": {
        "name": "Treasure Room",
        "description": "A hidden vault filled with dusty shelves and a large iron chest.",
        "exits": {"west": "hallway"},
        "monsters": [],
        "chest": ["Health Potion", "Mana Potion", "Leather Armor"]
    },
    "boss_room": {
        "name": "Boss Chamber",
        "description": "A massive cave. A terrifying Dragon Lord sits on a throne of bones.",
        "exits": {"south": "hallway"},
        "monsters": ["Dragon Lord"],
        "chest": None
    }
}
