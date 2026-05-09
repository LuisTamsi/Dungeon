from items import describe_item, get_item, SHOP_CATALOG


def _valid_index(inventory, index):
    if not (0 <= index < len(inventory)):
        print("  Invalid item number.")
        return False
    return True

def show_stats(player):
    print("\n--- Player Stats ---")
    print(f"  {player['name']} the {player['class']}")
    print(f"  HP : {player['hp']} / {player['max_hp']}")
    print(f"  MP : {player['mp']} / {player['max_mp']}")
    eff_atk = player["attack"] + player.get("attack_buff", 0)
    print(f"  ATK: {eff_atk}  DEF: {player['defense']}")
    print(f"  Weapon: {player['weapon']['name'] if player['weapon'] else 'None'}")
    print(f"  Armor : {player['armor']['name'] if player['armor'] else 'None'}")
    print(f"  Gold  : {player['gold']}")


def show_inventory(player):
    print("\n--- Inventory ---")
    if not player["inventory"]:
        print("  (empty)")
        return
    for i, item in enumerate(player["inventory"]):
        print(f"  [{i + 1}] ", end="")
        describe_item(item)


def show_skills(player):
    print("\n--- Skills ---")
    for i, skill in enumerate(player["skills"]):
        cost = skill["mp_cost"]
        affordable = "OK" if player["mp"] >= cost else "NO MP"
        print(f"  [{i + 1}] {skill['name']}  (MP Cost: {cost}) [{affordable}]")
        print(f"       {skill['description']}")


# ---------------------------------------------------------------------------
# Inventory actions
# ---------------------------------------------------------------------------

def pick_up_item(player, item):
    player["inventory"].append(item)
    print(f"  Picked up: {item['name']}")


def discard_item(player, index):
    if not _valid_index(player["inventory"], index):
        return
    removed = player["inventory"].pop(index)
    print(f"  Discarded: {removed['name']}")


def equip_item(player, index):
    if not _valid_index(player["inventory"], index):
        return
    item = player["inventory"][index]

    if item["type"] == "weapon":
        if player["weapon"]:
            player["inventory"].append(player["weapon"])
            print(f"  Unequipped: {player['weapon']['name']}")
        player["weapon"] = player["inventory"].pop(index)
        player["attack"] = player["base_attack"] + player["weapon"]["attack_bonus"]
        print(f"  Equipped: {player['weapon']['name']}  (ATK now {player['attack']})")

    elif item["type"] == "armor":
        if player["armor"]:
            player["inventory"].append(player["armor"])
            print(f"  Unequipped: {player['armor']['name']}")
        player["armor"] = player["inventory"].pop(index)
        player["defense"] = player["base_defense"] + player["armor"]["defense_bonus"]
        print(f"  Equipped: {player['armor']['name']}  (DEF now {player['defense']})")

    else:
        print("  You can't equip that. Use consumables with 'use <number>'.")


def use_consumable(player, index):
    if not _valid_index(player["inventory"], index):
        return
    item = player["inventory"][index]
    if item["type"] != "consumable":
        print("  That item is not a consumable. Try 'equip <number>'.")
        return
    _apply_consumable(player, item)
    player["inventory"].pop(index)


def use_consumable_in_combat(player, index):
    """Same as use_consumable but returns True on success so combat can track the turn."""
    if not _valid_index(player["inventory"], index):
        return False
    item = player["inventory"][index]
    if item["type"] != "consumable":
        print("  That item is not a consumable.")
        return False
    _apply_consumable(player, item)
    player["inventory"].pop(index)
    return True


def _apply_consumable(player, item):
    hp_gain = item.get("heal_hp", 0)
    mp_gain = item.get("heal_mp", 0)
    if hp_gain > 0:
        actual = min(hp_gain, player["max_hp"] - player["hp"])
        player["hp"] += actual
        print(f"  Used {item['name']}. Restored {actual} HP.  HP: {player['hp']}/{player['max_hp']}")
    if mp_gain > 0:
        actual = min(mp_gain, player["max_mp"] - player["mp"])
        player["mp"] += actual
        print(f"  Used {item['name']}. Restored {actual} MP.  MP: {player['mp']}/{player['max_mp']}")
    if hp_gain == 0 and mp_gain == 0:
        print(f"  Used {item['name']}. Nothing happened.")


# ---------------------------------------------------------------------------
# Shop
# ---------------------------------------------------------------------------

def open_shop(player):
    print("\n" + "=" * 45)
    print("  TRAVELING MERCHANT")
    print(f"  Your gold: {player['gold']}")
    print("=" * 45)
    print("  What would you like to buy?\n")

    for i, entry in enumerate(SHOP_CATALOG):
        item = get_item(entry["item_id"])
        if item:
            print(f"  [{i + 1}] {item['name']}  -  {entry['price']}g  -  {item['description']}")

    print("  [0] Leave shop\n")
    choice = input("  > ").strip()

    if choice == "0" or not choice.isdigit():
        print("  You leave the merchant.")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(SHOP_CATALOG):
        print("  Invalid selection.")
        return

    entry = SHOP_CATALOG[idx]
    item = get_item(entry["item_id"])
    if player["gold"] < entry["price"]:
        print(f"  Not enough gold. You need {entry['price']}g.")
        return

    player["gold"] -= entry["price"]
    player["inventory"].append(item)
    print(f"  Bought {item['name']} for {entry['price']}g.  Gold remaining: {player['gold']}")
