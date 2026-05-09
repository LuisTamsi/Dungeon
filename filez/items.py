# items.py
# All item definitions. Weapons, armors, consumables (HP and mana).
# Items are plain dicts. get_item() always returns a fresh copy.

WEAPONS = {
    "rusty_sword":   {"id": "rusty_sword",   "name": "Rusty Sword",    "type": "weapon", "attack_bonus": 3,  "description": "An old blade. Better than nothing."},
    "iron_axe":      {"id": "iron_axe",      "name": "Iron Axe",       "type": "weapon", "attack_bonus": 6,  "description": "Heavy and brutal."},
    "shadow_dagger": {"id": "shadow_dagger", "name": "Shadow Dagger",  "type": "weapon", "attack_bonus": 5,  "description": "Thin blade with dark energy."},
    "oak_staff":     {"id": "oak_staff",     "name": "Oak Staff",      "type": "weapon", "attack_bonus": 4,  "description": "A mage's staff carved with runes."},
    "bone_sword":    {"id": "bone_sword",    "name": "Bone Sword",     "type": "weapon", "attack_bonus": 9,  "description": "Forged from a fallen champion's bones."},
    "serpent_bow":   {"id": "serpent_bow",   "name": "Serpent Bow",    "type": "weapon", "attack_bonus": 7,  "description": "A curved bow etched with snake scales."},
    "doom_blade":    {"id": "doom_blade",    "name": "Doom Blade",     "type": "weapon", "attack_bonus": 16, "description": "The boss's legendary weapon."},
}

ARMORS = {
    "leather_vest":  {"id": "leather_vest",  "name": "Leather Vest",   "type": "armor", "defense_bonus": 3,  "description": "Light and cheap."},
    "iron_shield":   {"id": "iron_shield",   "name": "Iron Shield",    "type": "armor", "defense_bonus": 6,  "description": "Solid iron protection."},
    "shadow_cloak":  {"id": "shadow_cloak",  "name": "Shadow Cloak",   "type": "armor", "defense_bonus": 4,  "description": "Absorbs some incoming damage."},
    "mage_robe":     {"id": "mage_robe",     "name": "Mage Robe",      "type": "armor", "defense_bonus": 2,  "description": "Thin but enchanted."},
    "dark_armor":    {"id": "dark_armor",    "name": "Dark Armor",     "type": "armor", "defense_bonus": 11, "description": "Heavy plate forged in shadow."},
    "chain_mail":    {"id": "chain_mail",    "name": "Chain Mail",     "type": "armor", "defense_bonus": 5,  "description": "Reliable mid-tier protection."},
}

CONSUMABLES = {
    "health_potion": {"id": "health_potion", "name": "Health Potion",  "type": "consumable", "heal_hp": 30,  "heal_mp": 0,  "description": "Restores 30 HP."},
    "elixir":        {"id": "elixir",        "name": "Elixir",         "type": "consumable", "heal_hp": 60,  "heal_mp": 0,  "description": "Restores 60 HP."},
    "mana_vial":     {"id": "mana_vial",     "name": "Mana Vial",      "type": "consumable", "heal_hp": 0,   "heal_mp": 25, "description": "Restores 25 MP."},
    "mana_elixir":   {"id": "mana_elixir",   "name": "Mana Elixir",    "type": "consumable", "heal_hp": 0,   "heal_mp": 50, "description": "Restores 50 MP."},
    "full_restore":  {"id": "full_restore",  "name": "Full Restore",   "type": "consumable", "heal_hp": 50,  "heal_mp": 30, "description": "Restores 50 HP and 30 MP."},
}

# Shop catalog: what the shop sells and for how much gold.
SHOP_CATALOG = [
    {"item_id": "health_potion", "price": 20},
    {"item_id": "elixir",        "price": 40},
    {"item_id": "mana_vial",     "price": 25},
    {"item_id": "mana_elixir",   "price": 45},
    {"item_id": "full_restore",  "price": 60},
]


def get_item(item_id):
    """Return a fresh copy of an item dict by ID. Returns None if not found."""
    all_items = {**WEAPONS, **ARMORS, **CONSUMABLES}
    item = all_items.get(item_id)
    return dict(item) if item else None


def describe_item(item):
    """Print a single item's details."""
    if not item:
        print("  [No item]")
        return
    tag = item["type"].capitalize()
    print(f"  [{tag}] {item['name']}: {item['description']}", end="")
    if item["type"] == "weapon":
        print(f"  (+{item['attack_bonus']} ATK)")
    elif item["type"] == "armor":
        print(f"  (+{item['defense_bonus']} DEF)")
    elif item["type"] == "consumable":
        parts = []
        if item["heal_hp"] > 0:
            parts.append(f"+{item['heal_hp']} HP")
        if item["heal_mp"] > 0:
            parts.append(f"+{item['heal_mp']} MP")
        print(f"  ({', '.join(parts)})")
    else:
        print()
