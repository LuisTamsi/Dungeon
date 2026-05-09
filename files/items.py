# items.py
# Defines all items in the game: weapons and armors.
# Items are plain dictionaries to keep things simple.

WEAPONS = {
    "rusty_sword": {
        "id": "rusty_sword",
        "name": "Rusty Sword",
        "type": "weapon",
        "attack_bonus": 3,
        "description": "An old blade. Better than nothing.",
    },
    "iron_axe": {
        "id": "iron_axe",
        "name": "Iron Axe",
        "type": "weapon",
        "attack_bonus": 6,
        "description": "Heavy and brutal. Favored by berserkers.",
    },
    "shadow_dagger": {
        "id": "shadow_dagger",
        "name": "Shadow Dagger",
        "type": "weapon",
        "attack_bonus": 5,
        "description": "A thin blade that glints with dark energy.",
    },
    "oak_staff": {
        "id": "oak_staff",
        "name": "Oak Staff",
        "type": "weapon",
        "attack_bonus": 4,
        "description": "A mage's walking stick, carved with runes.",
    },
    "bone_sword": {
        "id": "bone_sword",
        "name": "Bone Sword",
        "type": "weapon",
        "attack_bonus": 8,
        "description": "Forged from the bones of a fallen champion.",
    },
    "doom_blade": {
        "id": "doom_blade",
        "name": "Doom Blade",
        "type": "weapon",
        "attack_bonus": 15,
        "description": "The boss's legendary weapon. Radiates dark power.",
    },
}

ARMORS = {
    "leather_vest": {
        "id": "leather_vest",
        "name": "Leather Vest",
        "type": "armor",
        "defense_bonus": 3,
        "description": "Light protection. Cheap and common.",
    },
    "iron_shield": {
        "id": "iron_shield",
        "name": "Iron Shield",
        "type": "armor",
        "defense_bonus": 6,
        "description": "A solid iron shield. Slows you down a bit.",
    },
    "shadow_cloak": {
        "id": "shadow_cloak",
        "name": "Shadow Cloak",
        "type": "armor",
        "defense_bonus": 4,
        "description": "A cloak that absorbs some incoming damage.",
    },
    "mage_robe": {
        "id": "mage_robe",
        "name": "Mage Robe",
        "type": "armor",
        "defense_bonus": 2,
        "description": "Thin fabric with protective enchantments.",
    },
    "dark_armor": {
        "id": "dark_armor",
        "name": "Dark Armor",
        "type": "armor",
        "defense_bonus": 10,
        "description": "Heavy plate forged in shadow. Rarely seen.",
    },
}

CONSUMABLES = {
    "health_potion": {
        "id": "health_potion",
        "name": "Health Potion",
        "type": "consumable",
        "heal_amount": 30,
        "description": "Restores 30 HP when used.",
    },
    "elixir": {
        "id": "elixir",
        "name": "Elixir",
        "type": "consumable",
        "heal_amount": 60,
        "description": "A powerful brew. Restores 60 HP.",
    },
}


def get_item(item_id):
    """Return a copy of an item by its ID."""
    all_items = {**WEAPONS, **ARMORS, **CONSUMABLES}
    item = all_items.get(item_id)
    if item:
        return dict(item)  # return a copy so original is not mutated
    return None


def describe_item(item):
    """Print item details."""
    if not item:
        print("  [No item]")
        return
    itype = item["type"].capitalize()
    print(f"  [{itype}] {item['name']}: {item['description']}")
    if item["type"] == "weapon":
        print(f"    Attack Bonus: +{item['attack_bonus']}")
    elif item["type"] == "armor":
        print(f"    Defense Bonus: +{item['defense_bonus']}")
    elif item["type"] == "consumable":
        print(f"    Heal Amount: {item['heal_amount']} HP")
