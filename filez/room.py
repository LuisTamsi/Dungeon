# room.py
# Dungeon layout. 8 rooms: easy, intermediate, loot, and boss.
# Easy and intermediate rooms spawn random monsters from their tier pool.
# Loot rooms have chests or floor items. Boss room has a fixed boss.

import copy
import random
from items import get_item
from monster import get_random_easy, get_random_intermediate

# ---------------------------------------------------------------------------
# Room Templates
# ---------------------------------------------------------------------------
# monster_count: how many monsters to spawn (ignored for loot/boss rooms).
# loot: static item IDs found in this room (floor/chest items).
# monster_ids: fixed list (boss only). Others are generated at build time.

ROOM_TEMPLATES = {

    "entrance": {
        "id": "entrance",
        "name": "Dungeon Entrance",
        "room_type": "easy",
        "description": (
            "Stone gates creak shut behind you. Torches flicker on damp walls. "
            "The air reeks of rot. A goblin snickers from the shadows."
        ),
        "connections": {"north": "guard_hall"},
        "monster_count": 2,
        "monster_ids": [],        # filled at build time
        "loot": ["rusty_sword", "health_potion"],
        "is_boss_room": False,
    },

    "guard_hall": {
        "id": "guard_hall",
        "name": "Guard Hall",
        "room_type": "easy",
        "description": (
            "A wide hall. Broken armor lines the walls. "
            "A corridor leads west to a dusty library, "
            "north into a crypt, and south back to the entrance."
        ),
        "connections": {"south": "entrance", "west": "forgotten_library", "north": "crypt", "east": "storage_room"},
        "monster_count": 2,
        "monster_ids": [],
        "loot": ["leather_vest"],
        "is_boss_room": False,
    },

    "storage_room": {
        "id": "storage_room",
        "name": "Storage Room",
        "room_type": "loot",
        "description": (
            "Crates and barrels crowd every corner. Whoever stocked this room "
            "did not survive to retrieve its contents."
        ),
        "connections": {"west": "guard_hall"},
        "monster_count": 0,
        "monster_ids": [],
        "loot": ["health_potion", "mana_vial", "iron_axe"],
        "is_boss_room": False,
    },

    "forgotten_library": {
        "id": "forgotten_library",
        "name": "Forgotten Library",
        "room_type": "loot",
        "description": (
            "Shelves of burnt books. Strange symbols etched into the floor. "
            "Someone left valuables in a locked chest that no longer locks."
        ),
        "connections": {"east": "guard_hall"},
        "monster_count": 0,
        "monster_ids": [],
        "loot": ["oak_staff", "mage_robe", "mana_vial", "health_potion"],
        "is_boss_room": False,
    },

    "crypt": {
        "id": "crypt",
        "name": "The Crypt",
        "room_type": "intermediate",
        "description": (
            "Row upon row of stone coffins. The ground is wet. "
            "Something heavy has been pacing here. "
            "North is the deeper dungeon. South leads back to the Guard Hall."
        ),
        "connections": {"south": "guard_hall", "north": "armory", "east": "torture_chamber"},
        "monster_count": 2,
        "monster_ids": [],
        "loot": ["elixir"],
        "is_boss_room": False,
    },

    "torture_chamber": {
        "id": "torture_chamber",
        "name": "Torture Chamber",
        "room_type": "intermediate",
        "description": (
            "Rusted chains hang from the ceiling. The walls are stained dark. "
            "Whatever lived here enjoyed its work."
        ),
        "connections": {"west": "crypt"},
        "monster_count": 1,
        "monster_ids": [],
        "loot": ["chain_mail", "mana_elixir"],
        "is_boss_room": False,
    },

    "armory": {
        "id": "armory",
        "name": "Ruined Armory",
        "room_type": "loot",
        "description": (
            "Weapon racks line the walls. Most are rusted beyond use, "
            "but someone left a few pieces worth taking."
        ),
        "connections": {"south": "crypt", "north": "boss_chamber"},
        "monster_count": 0,
        "monster_ids": [],
        "loot": ["bone_sword", "iron_shield", "full_restore"],
        "is_boss_room": False,
    },

    "boss_chamber": {
        "id": "boss_chamber",
        "name": "Shadow Lord's Chamber",
        "room_type": "boss",
        "description": (
            "The air is ice cold. Walls pulse with dark energy. "
            "A throne of black stone sits at the far end. "
            "A being of pure shadow watches you approach. "
            "There is no other way forward."
        ),
        "connections": {"south": "armory"},
        "monster_count": 0,
        "monster_ids": ["shadow_lord"],
        "loot": [],
        "is_boss_room": True,
    },
}


def build_rooms():
    """
    Build a fresh dungeon. Spawn random monsters into easy/intermediate rooms.
    Returns a dict of room_id -> room state.
    """
    rooms = {}
    for room_id, template in ROOM_TEMPLATES.items():
        room = copy.deepcopy(template)
        room["cleared"]    = False
        room["loot_taken"] = False

        # Expand loot IDs to item dicts
        room["loot_items"] = []
        for item_id in room["loot"]:
            item = get_item(item_id)
            if item:
                room["loot_items"].append(item)

        # Spawn monsters
        if room["room_type"] == "easy" and room["monster_count"] > 0:
            room["monster_ids"] = get_random_easy(room["monster_count"])
        elif room["room_type"] == "intermediate" and room["monster_count"] > 0:
            room["monster_ids"] = get_random_intermediate(room["monster_count"])
        # loot and boss rooms keep their monster_ids as-is (boss) or empty (loot)

        # Loot rooms and empty rooms start cleared
        if not room["monster_ids"]:
            room["cleared"] = True

        rooms[room_id] = room

    return rooms


def describe_room(room):
    print("\n" + "=" * 55)
    tag = f"[{room['room_type'].upper()}]"
    print(f"  {room['name']}  {tag}")
    print("=" * 55)
    print(f"  {room['description']}")

    exits = list(room["connections"].keys())
    print(f"\n  Exits: {', '.join(exits)}")
    print("  (Use: go north / go south / go east / go west)")

    if not room["cleared"] and room["monster_ids"]:
        count = len(room["monster_ids"])
        print(f"\n  Enemies present: {count} enemy/enemies in this room.")

    if not room["loot_taken"] and room["loot_items"]:
        names = [i["name"] for i in room["loot_items"]]
        print(f"  Items on floor/chest: {', '.join(names)}")

    if room["cleared"] and (room["loot_taken"] or not room["loot_items"]):
        print("  (Room fully cleared)")


def collect_room_loot(room, player):
    if room["loot_taken"] or not room["loot_items"]:
        print("  Nothing to pick up here.")
        return
    if not room["cleared"]:
        print("  Defeat all enemies before looting.")
        return
    for item in room["loot_items"]:
        player["inventory"].append(item)
        print(f"  Picked up: {item['name']}")
    room["loot_items"] = []
    room["loot_taken"] = True


def mark_room_cleared(room):
    room["cleared"] = True
    room["monster_ids"] = []


def can_move(room, direction):
    return room["connections"].get(direction)
