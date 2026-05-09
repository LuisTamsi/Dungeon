# =============================================================================
# rooms.py — Room Navigation and Exploration
#
# Handles:
#   - Displaying room descriptions
#   - Spawning monsters on first entry (no respawning)
#   - Navigating between rooms
#   - Picking up floor items
#   - Opening the Treasure Vault chest
# =============================================================================

import copy

import data
import monster as monster_module
import combat
import items as item_module
import utils


# -----------------------------------------------------------------------------
# Room Entry
# -----------------------------------------------------------------------------

def enter_room(current_player: dict, room: dict):
    """
    Called every time the player enters a room.
    - Prints the room description
    - Spawns monsters on first visit (if not cleared)
    - Shows exits, floor items, and any monsters present
    """
    utils.header(room["name"].upper())
    utils.blank()
    print(f"  {room['description']}")
    utils.blank()

    # Spawn monsters only on the first visit (cleared == False)
    if not room["cleared"] and room["difficulty"] != "empty":
        _spawn_room_monsters(room)

    _display_room_contents(room)


def _display_room_contents(room: dict):
    """Print exits, floor items, and living monsters."""
    # Exits
    exits = room.get("exits", {})
    if exits:
        exit_str = "  ".join(
            f"[{direction.upper()}] → {data.ROOMS[dest]['name']}"
            for direction, dest in exits.items()
        )
        utils.info(f"Exits: {exit_str}")
    else:
        utils.info("Exits: None (dead end)")

    utils.blank()

    # Chest (Treasure Vault only)
    if "chest" in room:
        chest = room["chest"]
        if not chest["opened"]:
            utils.info("A large iron chest sits in the center of the room.")
            utils.info("  → Type 'open chest' to open it.")
        else:
            utils.info("An empty, open chest. You've already taken everything.")

    # Floor items
    if room.get("items"):
        utils.info("Items on the ground:")
        for item_name in room["items"]:
            item = item_module.get_item(item_name)
            if item:
                print(f"    - {item_module.describe_item(item)}")
        utils.info("  → Type 'pickup <item name>' to pick something up.")

    # Monsters
    living = [m for m in room.get("monsters", []) if monster_module.is_alive(m)]
    if living:
        utils.blank()
        utils.warn(f"{len(living)} monster(s) in this room!")
        for m in living:
            print(f"    - {m['name']} (HP: {m['hp']}/{m['max_hp']})")
        utils.info("  → Type 'fight' to engage, or 'fight <name>' for a specific enemy.")
    elif room["cleared"] and room["difficulty"] != "empty":
        utils.info("This room has been cleared.")


# -----------------------------------------------------------------------------
# Monster Spawning
# -----------------------------------------------------------------------------

def _spawn_room_monsters(room: dict):
    """
    Spawn monsters into the room based on its difficulty tier.
    Only called once per room (on first entry while cleared == False).
    After spawning, monsters persist in room["monsters"] — when they die
    in combat, their hp drops to 0 and the room is marked cleared.

    No respawning: once a room is cleared it stays cleared forever.
    """
    tier = room.get("monster_tier")
    count = room.get("monster_count", 1)

    if tier == "boss":
        # Boss rooms always spawn the unique boss
        room["monsters"] = [monster_module.spawn_boss()]
    elif tier in ("easy", "intermediate"):
        room["monsters"] = [
            monster_module.spawn_monster(tier) for _ in range(count)
        ]


def _check_room_cleared(room: dict):
    """Mark room as cleared if all monsters are dead."""
    if not room["cleared"]:
        living = [m for m in room.get("monsters", []) if monster_module.is_alive(m)]
        if not living:
            room["cleared"] = True


# -----------------------------------------------------------------------------
# Navigation
# -----------------------------------------------------------------------------

def navigate(rooms: dict, current_key: str, direction: str) -> str | None:
    """
    Attempt to move in the given direction from the current room.
    Returns the key of the destination room, or None if the exit doesn't exist.

    'rooms' is the live game state dict (not data.ROOMS directly) so that
    the cleared/monsters state persists across navigation.
    """
    current_room = rooms[current_key]
    exits = current_room.get("exits", {})
    direction = direction.lower()

    destination_key = exits.get(direction)
    if destination_key is None:
        utils.warn(f"You can't go {direction} from here.")
        return None

    return destination_key


# -----------------------------------------------------------------------------
# Fight Command
# -----------------------------------------------------------------------------

def fight(current_player: dict, room: dict, target_name: str = "") -> bool:
    """
    Engage a monster in the current room.
    If target_name is given, fight that specific monster.
    Otherwise, fight the first living monster in the room.
    Returns True if the room ends up cleared after the fight.
    """
    living = [m for m in room.get("monsters", []) if monster_module.is_alive(m)]

    if not living:
        utils.info("There are no monsters here to fight.")
        return False

    # Find target
    if target_name:
        target = next(
            (m for m in living if m["name"].lower() == target_name.lower()),
            None
        )
        if target is None:
            utils.warn(f"No monster named '{target_name}' here.")
            utils.info(f"Monsters present: {', '.join(m['name'] for m in living)}")
            return False
    else:
        target = living[0]

    combat.start_combat(current_player, target)

    _check_room_cleared(room)
    return room["cleared"]


# -----------------------------------------------------------------------------
# Item Pickup
# -----------------------------------------------------------------------------

def pickup_item(current_player: dict, room: dict, item_name: str):
    """
    Move an item from the room's floor list into the player's inventory.
    Case-insensitive matching.
    """
    target = item_name.lower()
    match = next(
        (name for name in room.get("items", []) if name.lower() == target),
        None
    )
    if match is None:
        utils.warn(f"'{item_name}' is not on the ground here.")
        return

    room["items"].remove(match)
    current_player["inventory"].append(match)
    item = item_module.get_item(match)
    if item:
        utils.success(f"Picked up: {item_module.describe_item(item)}")
    else:
        utils.success(f"Picked up: {match}")


# -----------------------------------------------------------------------------
# Treasure Vault Chest
# -----------------------------------------------------------------------------

def open_chest(current_player: dict, room: dict):
    """
    Open the Treasure Vault chest.
    Adds all chest contents to the player's inventory.
    Can only be opened once — chest["opened"] is set to True.
    """
    if "chest" not in room:
        utils.warn("There is no chest in this room.")
        return

    chest = room["chest"]
    if chest["opened"]:
        utils.info("The chest is already open and empty.")
        return

    utils.header("TREASURE VAULT — CHEST OPENED")
    utils.blank()
    print("  The heavy lid creaks open. Inside, you find:")
    utils.blank()

    for item_name in chest["contents"]:
        current_player["inventory"].append(item_name)
        item = item_module.get_item(item_name)
        if item:
            print(f"    + {item_module.describe_item(item)}")
        else:
            print(f"    + {item_name}")

    chest["opened"] = True
    utils.blank()
    utils.success("All items added to your inventory!")
    utils.info("  → Type 'inventory' to see what you have.")
    utils.info("  → Type 'equip <item name>' to equip weapons or armor.")
