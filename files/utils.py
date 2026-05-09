from items import describe_item

def show_stats(player):
    """Print current player stats."""
    print("\n--- Player Stats ---")
    print(f"  Name  : {player['name']} the {player['class']}")
    print(f"  HP    : {player['hp']} / {player['max_hp']}")
    print(f"  Attack: {player['attack']}  Defense: {player['defense']}")
    weapon_name = player["weapon"]["name"] if player["weapon"] else "None"
    armor_name = player["armor"]["name"] if player["armor"] else "None"
    print(f"  Weapon: {weapon_name}")
    print(f"  Armor : {armor_name}")
    print(f"  Gold  : {player['gold']}")


def show_inventory(player):
    """Print player inventory."""
    print("\n--- Inventory ---")
    if not player["inventory"]:
        print("  (empty)")
        return
    for i, item in enumerate(player["inventory"]):
        print(f"  [{i + 1}] ", end="")
        describe_item(item)


def show_skills(player):
    """Print player skills and their cooldowns."""
    print("\n--- Skills ---")
    for i, skill in enumerate(player["skills"]):
        cd = skill["current_cooldown"]
        status = "Ready" if cd == 0 else f"Cooldown: {cd} turn(s)"
        print(f"  [{i + 1}] {skill['name']} ({status})")
        print(f"       {skill['description']}")


def pick_up_item(player, item):
    """Add an item to the player's inventory."""
    player["inventory"].append(item)
    print(f"  Picked up: {item['name']}")


def discard_item(player, index):
    """Remove an item from inventory by index (0-based)."""
    if index < 0 or index >= len(player["inventory"]):
        print("  Invalid item number.")
        return
    removed = player["inventory"].pop(index)
    print(f"  Discarded: {removed['name']}")


def equip_item(player, index):
    """Equip a weapon or armor from inventory."""
    if index < 0 or index >= len(player["inventory"]):
        print("  Invalid item number.")
        return

    item = player["inventory"][index]

    if item["type"] == "weapon":
        # Unequip current weapon back to inventory if any
        if player["weapon"]:
            player["inventory"].append(player["weapon"])
            print(f"  Unequipped: {player['weapon']['name']}")
        player["weapon"] = item
        player["inventory"].pop(index)
        # Recalculate attack
        player["attack"] = player["base_attack"] + item["attack_bonus"]
        print(f"  Equipped: {item['name']} (Attack now {player['attack']})")

    elif item["type"] == "armor":
        if player["armor"]:
            player["inventory"].append(player["armor"])
            print(f"  Unequipped: {player['armor']['name']}")
        player["armor"] = item
        player["inventory"].pop(index)
        player["defense"] = player["base_defense"] + item["defense_bonus"]
        print(f"  Equipped: {item['name']} (Defense now {player['defense']})")

    elif item["type"] == "consumable":
        print("  You cannot equip a consumable. Use it instead.")

    else:
        print("  Cannot equip that.")


def use_consumable(player, index):
    """Use a consumable item from inventory."""
    if index < 0 or index >= len(player["inventory"]):
        print("  Invalid item number.")
        return

    item = player["inventory"][index]

    if item["type"] != "consumable":
        print("  That item is not usable. Try equipping it instead.")
        return

    heal = item.get("heal_amount", 0)
    player["hp"] = min(player["hp"] + heal, player["max_hp"])
    player["inventory"].pop(index)
    print(f"  Used {item['name']}. Restored {heal} HP. HP is now {player['hp']}/{player['max_hp']}.")


def tick_cooldowns(player):
    """Reduce all skill cooldowns by 1 at the end of a turn."""
    for skill in player["skills"]:
        if skill["current_cooldown"] > 0:
            skill["current_cooldown"] -= 1


