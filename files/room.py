# room.py
# Defines all rooms in the dungeon.
# Each room is a dictionary with a name, description,
# connections to other rooms, monsters, and loot.

from items import get_item

# --- Room Definitions ---
# "connections" maps direction strings to room IDs.
# "monsters" is a list of monster IDs that spawn in this room.
# "loot" is a list of item IDs that can be found lying in the room.
# "cleared" tracks whether all monsters have been defeated.
# "loot_taken" tracks whether the room loot has been collected.

ROOM_TEMPLATES = {
    "entrance": {
        "id": "entrance",
        "name": "Dungeon Entrance",
        "description": (
            "The stone gate creaks behind you. Torches flicker on the walls. "
            "The air smells of mold and old blood. "
            "To the north, a dark corridor leads deeper into the dungeon."
        ),
        "connections": {
            "north": "guard_hall",
        },
        "monsters": ["goblin", "goblin"],
        "loot": ["rusty_sword", "health_potion"],
        "is_boss_room": False,
    },

    "guard_hall": {
        "id": "guard_hall",
        "name": "Guard Hall",
        "description": (
            "A wide hall with broken armor lining the walls. "
            "Skeletons of former guards sit slumped at their posts. "
            "A corridor to the west leads to a library. "
            "The south passage leads back to the entrance. "
            "To the north, heavy doors open into a crypt."
        ),
        "connections": {
            "south": "entrance",
            "west": "dark_library",
            "north": "crypt",
        },
        "monsters": ["skeleton", "goblin"],
        "loot": ["leather_vest"],
        "is_boss_room": False,
    },

    "dark_library": {
        "id": "dark_library",
        "name": "Dark Library",
        "description": (
            "Shelves of charred books surround you. "
            "Strange symbols are etched into the floor. "
            "A dark mage was clearly at work here. "
            "The east passage returns to the Guard Hall."
        ),
        "connections": {
            "east": "guard_hall",
        },
        "monsters": ["dark_mage"],
        "loot": ["oak_staff", "mage_robe", "health_potion"],
        "is_boss_room": False,
    },

    "crypt": {
        "id": "crypt",
        "name": "The Crypt",
        "description": (
            "Row upon row of stone coffins fill this massive chamber. "
            "The ground is wet. Something large has been moving through here. "
            "South leads back to the Guard Hall. "
            "To the north lies the Shadow Lord's chamber."
        ),
        "connections": {
            "south": "guard_hall",
            "north": "boss_chamber",
        },
        "monsters": ["stone_golem", "skeleton"],
        "loot": ["iron_shield", "elixir"],
        "is_boss_room": False,
    },

    "boss_chamber": {
        "id": "boss_chamber",
        "name": "Shadow Lord's Chamber",
        "description": (
            "The air is ice cold. The walls pulse with dark energy. "
            "A throne of black stone sits at the far end. "
            "On it sits a being of pure shadow, watching you. "
            "There is no way forward. Only through."
        ),
        "connections": {
            "south": "crypt",
        },
        "monsters": ["shadow_lord"],
        "loot": [],
        "is_boss_room": True,
    },
}


def build_rooms():
    """
    Build a fresh dungeon from templates.
    Returns a dict of room_id -> room state dict.
    """
    import copy
    rooms = {}
    for room_id, template in ROOM_TEMPLATES.items():
        room = copy.deepcopy(template)
        room["cleared"] = False     # monsters defeated?
        room["loot_taken"] = False  # floor loot collected?
        # Expand loot IDs to actual item dicts
        room["loot_items"] = []
        for item_id in room["loot"]:
            item = get_item(item_id)
            if item:
                room["loot_items"].append(item)
        rooms[room_id] = room
    return rooms


def describe_room(room):
    """Print the room name and description."""
    print("\n" + "=" * 50)
    print(f"  {room['name'].upper()}")
    print("=" * 50)
    print(f"  {room['description']}")

    # Show exits
    exits = list(room["connections"].keys())
    print(f"\n  Exits: {', '.join(exits)}")

    # Show monsters if not cleared
    if not room["cleared"] and room["monsters"]:
        print(f"  Enemies present! ({len(room['monsters'])} remaining)")

    # Show floor loot if available
    if not room["loot_taken"] and room["loot_items"]:
        names = [item["name"] for item in room["loot_items"]]
        print(f"  Items on the floor: {', '.join(names)}")

    if room["cleared"]:
        print("  (Room cleared)")


def get_room_monsters(room):
    """Return the list of monster IDs still in the room."""
    if room["cleared"]:
        return []
    return room["monsters"]


def mark_room_cleared(room):
    """Mark a room as cleared (no more monsters)."""
    room["cleared"] = True
    room["monsters"] = []


def collect_room_loot(room, player):
    """Move all floor loot into the player's inventory."""
    if room["loot_taken"] or not room["loot_items"]:
        print("  Nothing to pick up here.")
        return
    for item in room["loot_items"]:
        player["inventory"].append(item)
        print(f"  Picked up: {item['name']}")
    room["loot_items"] = []
    room["loot_taken"] = True


def can_move(room, direction):
    """Return the destination room ID if the direction is valid, else None."""
    return room["connections"].get(direction)
