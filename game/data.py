import random
from typing import Dict, List

from models import Armor, Item, Monster, Player, Potion, Room, Skill, Weapon


EASY_MONSTERS = ["goblin", "slime"]
INTERMEDIATE_MONSTERS = ["skeleton", "orc"]
BOSS_MONSTERS = ["dragon"]


def build_items() -> Dict[str, Item]:
    return {
        "longsword": Weapon(
            name="Longsword",
            description="A sturdy blade favored by knights.",
            item_type="weapon",
            attack_bonus=3,
        ),
        "dagger": Weapon(
            name="Dagger",
            description="A small blade perfect for quick strikes.",
            item_type="weapon",
            attack_bonus=2,
        ),
        "staff": Weapon(
            name="Mage Staff",
            description="A carved staff that channels magic.",
            item_type="weapon",
            attack_bonus=2,
        ),
        "leather": Armor(
            name="Leather Armor",
            description="Light armor offering basic protection.",
            item_type="armor",
            defense_bonus=2,
        ),
        "chain": Armor(
            name="Chainmail",
            description="Heavy armor that absorbs hard hits.",
            item_type="armor",
            defense_bonus=4,
        ),
        "potion": Potion(
            name="Healing Potion",
            description="Restores 12 HP.",
            item_type="potion",
            heal_amount=12,
            cost=10,
        ),
    }


def build_skills() -> Dict[str, Skill]:
    return {
        "power_strike": Skill(
            name="Power Strike",
            description="A strong blow that deals extra damage.",
            effect_type="damage",
            effect_value=5,
            mana_cost=3,
        ),
        "shield_bash": Skill(
            name="Shield Bash",
            description="A solid hit that rattles the target.",
            effect_type="damage",
            effect_value=3,
            mana_cost=2,
        ),
        "backstab": Skill(
            name="Backstab",
            description="A precise strike that hits a weak spot.",
            effect_type="damage",
            effect_value=6,
            mana_cost=3,
        ),
        "quick_slash": Skill(
            name="Quick Slash",
            description="A fast cut that never misses.",
            effect_type="damage",
            effect_value=3,
            mana_cost=2,
        ),
        "smoke_bomb": Skill(
            name="Smoke Bomb",
            description="A trick that restores a bit of HP.",
            effect_type="heal",
            effect_value=4,
            mana_cost=3,
        ),
        "firebolt": Skill(
            name="Firebolt",
            description="A burst of flame that scorches the target.",
            effect_type="damage",
            effect_value=7,
            mana_cost=3,
        ),
        "ice_shard": Skill(
            name="Ice Shard",
            description="A sharp shard of ice.",
            effect_type="damage",
            effect_value=4,
            mana_cost=2,
        ),
        "arcane_pulse": Skill(
            name="Arcane Pulse",
            description="Magic that hits and heals the caster slightly.",
            effect_type="heal",
            effect_value=5,
            mana_cost=4,
        ),
        "dirty_trick": Skill(
            name="Dirty Trick",
            description="A cheap shot that stings.",
            effect_type="damage",
            effect_value=2,
            mana_cost=0,
        ),
        "jab": Skill(
            name="Jab",
            description="A fast poke with a sharp edge.",
            effect_type="damage",
            effect_value=3,
            mana_cost=0,
        ),
        "acid_spit": Skill(
            name="Acid Spit",
            description="A splash of acid that burns.",
            effect_type="damage",
            effect_value=3,
            mana_cost=0,
        ),
        "bone_shield": Skill(
            name="Bone Shield",
            description="A bony ward that restores health.",
            effect_type="heal",
            effect_value=5,
            mana_cost=0,
        ),
        "bone_rattle": Skill(
            name="Bone Rattle",
            description="A chilling strike from a bony grip.",
            effect_type="damage",
            effect_value=4,
            mana_cost=0,
        ),
        "feral_bite": Skill(
            name="Feral Bite",
            description="A savage bite that tears armor.",
            effect_type="damage",
            effect_value=4,
            mana_cost=0,
        ),
        "dark_claw": Skill(
            name="Dark Claw",
            description="A cursed slash from the shadows.",
            effect_type="damage",
            effect_value=5,
            mana_cost=0,
        ),
    }


def build_class_presets(items: Dict[str, Item], skills: Dict[str, Skill]) -> Dict[str, Dict]:
    return {
        "warrior": {
            "hp": 32,
            "mana": 8,
            "attack": 6,
            "defense": 3,
            "weapon": items["longsword"],
            "armor": items["leather"],
            "skills": [skills["power_strike"], skills["shield_bash"]],
        },
        "rogue": {
            "hp": 26,
            "mana": 10,
            "attack": 7,
            "defense": 2,
            "weapon": items["dagger"],
            "armor": items["leather"],
            "skills": [skills["backstab"], skills["quick_slash"], skills["smoke_bomb"]],
        },
        "mage": {
            "hp": 22,
            "mana": 14,
            "attack": 8,
            "defense": 1,
            "weapon": items["staff"],
            "armor": items["leather"],
            "skills": [skills["firebolt"], skills["ice_shard"], skills["arcane_pulse"]],
        },
    }


def create_player(name: str, class_key: str, presets: Dict[str, Dict]) -> Player:
    preset = presets[class_key]
    player = Player(
        name=name,
        class_name=class_key.title(),
        hp=preset["hp"],
        max_hp=preset["hp"],
        mana=preset["mana"],
        max_mana=preset["mana"],
        attack=preset["attack"],
        defense=preset["defense"],
        gold=0,
        skills=list(preset["skills"]),
    )
    weapon = preset["weapon"]
    armor = preset["armor"]
    player.add_item(weapon)
    player.add_item(armor)
    player.weapon = weapon
    player.armor = armor
    return player


def build_monster_templates(items: Dict[str, Item], skills: Dict[str, Skill]) -> Dict[str, Dict]:
    return {
        "goblin": {
            "name": "Goblin",
            "description": "A sneaky creature with a rusty blade.",
            "hp": 12,
            "attack": 3,
            "weapon_name": "Rusty Knife",
            "weapon_bonus": 1,
            "skills": ["dirty_trick", "jab"],
            "loot": [items["dagger"]],
            "gold": (3, 6),
            "boss": False,
        },
        "slime": {
            "name": "Slime",
            "description": "A wobbling blob that absorbs hits.",
            "hp": 18,
            "attack": 3,
            "weapon_name": "Acid Splash",
            "weapon_bonus": 1,
            "skills": ["acid_spit", "dirty_trick"],
            "loot": [items["leather"]],
            "gold": (2, 5),
            "boss": False,
        },
        "skeleton": {
            "name": "Skeleton",
            "description": "A rattling warrior held together by dark magic.",
            "hp": 20,
            "attack": 5,
            "weapon_name": "Bone Sword",
            "weapon_bonus": 2,
            "skills": ["bone_shield", "bone_rattle"],
            "loot": [items["chain"]],
            "gold": (6, 10),
            "boss": False,
        },
        "orc": {
            "name": "Orc Raider",
            "description": "A hulking brute with a heavy axe.",
            "hp": 24,
            "attack": 6,
            "weapon_name": "Heavy Axe",
            "weapon_bonus": 2,
            "skills": ["feral_bite", "jab"],
            "loot": [items["longsword"]],
            "gold": (8, 12),
            "boss": False,
        },
        "dragon": {
            "name": "Ash Dragon",
            "description": "The dungeon boss, wreathed in embers.",
            "hp": 45,
            "attack": 9,
            "weapon_name": "Flame Breath",
            "weapon_bonus": 3,
            "skills": ["dark_claw", "feral_bite", "acid_spit"],
            "loot": [items["longsword"], items["chain"]],
            "gold": (20, 30),
            "boss": True,
        },
    }


def create_monster(kind: str, templates: Dict[str, Dict], skills: Dict[str, Skill]) -> Monster:
    data = templates[kind]
    skill_list = [skills[name] for name in data["skills"]]
    gold_amount = random.randint(data["gold"][0], data["gold"][1])
    return Monster(
        name=data["name"],
        description=data["description"],
        hp=data["hp"],
        attack=data["attack"],
        weapon_name=data["weapon_name"],
        weapon_bonus=data["weapon_bonus"],
        skills=skill_list,
        loot_table=list(data["loot"]),
        gold_drop=gold_amount,
        is_boss=data["boss"],
    )


def build_rooms(items: Dict[str, Item]) -> Dict[str, Room]:
    return {
        "entrance": Room(
            name="Entrance Hall",
            description="A cold entrance with torchlight flickering on stone walls.",
            exits={"north": "armory", "east": "market"},
            tier="easy",
            spawn_count=2,
            has_shop=False,
            items=[items["potion"]],
        ),
        "armory": Room(
            name="Abandoned Armory",
            description="Old weapon racks line the walls, covered in dust.",
            exits={"south": "entrance", "north": "crypt"},
            tier="easy",
            spawn_count=2,
            has_shop=False,
            items=[items["dagger"]],
        ),
        "market": Room(
            name="Merchant Camp",
            description="A small camp where a trader sells basic supplies.",
            exits={"west": "entrance"},
            tier="easy",
            spawn_count=0,
            has_shop=True,
            items=[],
        ),
        "crypt": Room(
            name="Crypt",
            description="A silent chamber filled with ancient bones.",
            exits={"south": "armory", "north": "boss_chamber"},
            tier="intermediate",
            spawn_count=1,
            has_shop=False,
            items=[items["chain"]],
        ),
        "boss_chamber": Room(
            name="Boss Chamber",
            description="A vast room glowing with heat and ash.",
            exits={"south": "crypt"},
            tier="boss",
            spawn_count=1,
            has_shop=False,
            items=[],
        ),
    }


def spawn_room_monsters(room: Room, templates: Dict[str, Dict], skills: Dict[str, Skill]) -> None:
    if room.spawned or room.spawn_count <= 0:
        room.spawned = True
        return

    if room.tier == "easy":
        pool = EASY_MONSTERS
    elif room.tier == "intermediate":
        pool = INTERMEDIATE_MONSTERS
    else:
        pool = BOSS_MONSTERS

    for _ in range(room.spawn_count):
        kind = random.choice(pool)
        room.monsters.append(create_monster(kind, templates, skills))

    room.spawned = True
