# =============================================================================
# items.py — Item & Equipment Logic
# Handles equipping, unequipping, using, and discarding items.
# Used by player.py (inventory management) and combat.py (use during fight).
# Centralised here to avoid circular imports between player/combat/rooms.
# =============================================================================

import data
import utils


# -----------------------------------------------------------------------------
# Lookup
# -----------------------------------------------------------------------------

def get_item(name: str) -> dict | None:
    """
    Case-insensitive lookup of an item in data.ITEMS.
    Returns the item dict or None if not found.
    """
    for key, item in data.ITEMS.items():
        if key.lower() == name.lower():
            return item
    return None


def describe_item(item: dict) -> str:
    """Return a one-line description string for an item."""
    itype = item["item_type"]
    if itype == "weapon":
        return f"{item['name']} [Weapon | +{item['attack_bonus']} ATK] — {item['description']}"
    elif itype == "armor":
        return f"{item['name']} [Armor  | +{item['defense_bonus']} DEF] — {item['description']}"
    elif itype == "consumable":
        parts = []
        if item.get("hp_restore", 0) > 0:
            parts.append(f"+{item['hp_restore']} HP")
        if item.get("mp_restore", 0) > 0:
            parts.append(f"+{item['mp_restore']} MP")
        effect = ", ".join(parts) if parts else "no effect"
        return f"{item['name']} [Consumable | {effect}] — {item['description']}"
    return f"{item['name']} — {item['description']}"


# -----------------------------------------------------------------------------
# Equipment
# -----------------------------------------------------------------------------

def equip_item(player: dict, item_name: str) -> bool:
    """
    Equip a weapon or armor from the player's inventory.
    Applies the item's stat bonus to the player.
    If something is already equipped in that slot, unequips it first.
    Returns True on success, False if item not found in inventory.
    """
    # Find the item in inventory (case-insensitive)
    item = _find_in_inventory(player, item_name)
    if item is None:
        utils.warn(f"'{item_name}' is not in your inventory.")
        return False

    itype = item["item_type"]
    if itype not in ("weapon", "armor"):
        utils.warn(f"You cannot equip '{item['name']}'. It is a {itype}.")
        return False

    slot = "weapon" if itype == "weapon" else "armor"

    # Unequip existing item in the same slot first
    if player[slot]:
        unequip_item(player, slot)

    # Apply bonus and equip
    player[slot] = item["name"]
    if itype == "weapon":
        player["attack"] += item["attack_bonus"]
        utils.success(
            f"Equipped {item['name']}. ATK is now {player['attack']}."
        )
    else:
        player["defense"] += item["defense_bonus"]
        utils.success(
            f"Equipped {item['name']}. DEF is now {player['defense']}."
        )

    # Remove from inventory (it is now tracked via the slot key)
    player["inventory"].remove(item["name"])
    return True


def unequip_item(player: dict, slot: str) -> bool:
    """
    Unequip the item currently in 'weapon' or 'armor' slot.
    Reverses the stat bonus and puts the item back in inventory.
    Returns True on success, False if the slot is empty.

    Why unequip reverts stats: we track bonuses via the item definition,
    not via a separate 'bonus' field on the player, keeping the player dict simple.
    """
    if slot not in ("weapon", "armor"):
        utils.warn(f"Unknown slot '{slot}'. Use 'weapon' or 'armor'.")
        return False

    item_name = player[slot]
    if not item_name:
        utils.warn(f"Nothing is equipped in the {slot} slot.")
        return False

    item = get_item(item_name)
    if item is None:
        # Data inconsistency safety net
        player[slot] = ""
        return False

    # Revert bonus
    if slot == "weapon":
        player["attack"] -= item["attack_bonus"]
    else:
        player["defense"] -= item["defense_bonus"]

    player["inventory"].append(item_name)
    player[slot] = ""
    utils.success(f"Unequipped {item_name}.")
    return True


# -----------------------------------------------------------------------------
# Consumables
# -----------------------------------------------------------------------------

def use_item(player: dict, item_name: str) -> bool:
    """
    Use a consumable from the player's inventory.
    Restores HP and/or MP. Removes the item from inventory on use.
    Returns True on success, False if item not found or not a consumable.
    """
    item = _find_in_inventory(player, item_name)
    if item is None:
        utils.warn(f"'{item_name}' is not in your inventory.")
        return False

    if item["item_type"] != "consumable":
        utils.warn(f"'{item['name']}' cannot be used. Try 'equip' instead.")
        return False

    hp_gain = item.get("hp_restore", 0)
    mp_gain = item.get("mp_restore", 0)

    if hp_gain > 0:
        old_hp = player["hp"]
        player["hp"] = min(player["hp"] + hp_gain, player["max_hp"])
        actual = player["hp"] - old_hp
        utils.success(f"Used {item['name']}. Restored {actual} HP. ({player['hp']}/{player['max_hp']})")

    if mp_gain > 0:
        old_mp = player["mp"]
        player["mp"] = min(player["mp"] + mp_gain, player["max_mp"])
        actual = player["mp"] - old_mp
        utils.success(f"Used {item['name']}. Restored {actual} MP. ({player['mp']}/{player['max_mp']})")

    player["inventory"].remove(item["name"])
    return True


# -----------------------------------------------------------------------------
# Discard
# -----------------------------------------------------------------------------

def discard_item(player: dict, item_name: str) -> bool:
    """
    Permanently discard an item from the inventory.
    Asks for confirmation before removing.
    Returns True if discarded, False if cancelled or not found.
    """
    item = _find_in_inventory(player, item_name)
    if item is None:
        utils.warn(f"'{item_name}' is not in your inventory.")
        return False

    if utils.confirm(f"Discard {item['name']} permanently?"):
        player["inventory"].remove(item["name"])
        utils.info(f"You dropped {item['name']}. It is gone forever.")
        return True

    utils.info("Discard cancelled.")
    return False


# -----------------------------------------------------------------------------
# Inventory Display
# -----------------------------------------------------------------------------

def show_inventory(player: dict):
    """Display the player's full inventory, equipment, and gold."""
    utils.subheader(f"  {player['name']}'s Inventory")

    # Equipment slots
    weapon = player["weapon"] if player["weapon"] else "None"
    armor  = player["armor"]  if player["armor"]  else "None"
    print(f"  Weapon : {weapon}")
    print(f"  Armor  : {armor}")
    print(f"  Gold   : {player['gold']} g")
    utils.separator()

    if not player["inventory"]:
        utils.info("Your bag is empty.")
        return

    print(f"  Items ({len(player['inventory'])}):")
    for i, item_name in enumerate(player["inventory"], 1):
        item = get_item(item_name)
        if item:
            print(f"    {i}. {describe_item(item)}")
        else:
            print(f"    {i}. {item_name} (unknown item)")


# -----------------------------------------------------------------------------
# Internal Helpers
# -----------------------------------------------------------------------------

def _find_in_inventory(player: dict, item_name: str) -> dict | None:
    """
    Find an item in the player's inventory by name (case-insensitive).
    Returns the full item dict from data.ITEMS, or None.
    """
    target = item_name.lower()
    for name in player["inventory"]:
        if name.lower() == target:
            return data.ITEMS.get(name)
    return None
