# main.py - Main game loop
# This is the entry point. Run this file to play the game.
# Handles room navigation, inventory, equipping, and win/lose conditions.

import copy
import random
import data
import player as player_module
import combat


def setup_rooms():
    """Create a copy of all rooms and spawn monsters inside them."""
    # Deep copy so we don't change the original data
    rooms = copy.deepcopy(data.ROOMS)

    # Replace monster name strings with actual monster dicts
    for room_key in rooms:
        room = rooms[room_key]
        monster_names = room["monsters"]
        room["monsters"] = []
        for name in monster_names:
            # Copy each monster so killing one doesn't affect the template
            monster = copy.deepcopy(data.MONSTERS[name])
            room["monsters"].append(monster)
        room["cleared"] = False

    return rooms


def show_room(room):
    """Display room info: name, description, monsters, items, exits."""
    print("\n" + "=" * 40)
    print(f"  {room['name']}")
    print("=" * 40)
    print(f"  {room['description']}")

    # Show alive monsters
    alive = []
    for m in room["monsters"]:
        if m["hp"] > 0:
            alive.append(m)

    if len(alive) > 0:
        print(f"\n  Monsters here ({len(alive)}):")
        for m in alive:
            boss_tag = " [BOSS]" if m["is_boss"] else ""
            print(f"    - {m['name']}{boss_tag} (HP: {m['hp']}/{m['max_hp']})")

    # Show chest
    if room["chest"] is not None and len(room["chest"]) > 0:
        print("\n  A chest is here! Type 'open' to open it.")

    # Show exits
    print("\n  Exits:")
    for direction, room_key in room["exits"].items():
        dest_name = data.ROOMS[room_key]["name"]
        print(f"    {direction} -> {dest_name}")


def show_inventory(player):
    """Show the player's inventory, equipment, and gold."""
    print("\n" + "-" * 40)
    print(f"  {player['name']}'s Inventory")
    print("-" * 40)
    print(f"  Weapon: {player['weapon'] if player['weapon'] else 'None'}")
    print(f"  Armor:  {player['armor'] if player['armor'] else 'None'}")
    print(f"  Gold:   {player['gold']}")

    if len(player["inventory"]) == 0:
        print("  Bag: (empty)")
    else:
        print(f"  Bag ({len(player['inventory'])} items):")
        for i in range(len(player["inventory"])):
            item_name = player["inventory"][i]
            item = data.ITEMS.get(item_name)
            if item:
                print(f"    {i + 1}. {item['name']} [{item['type']}] - {item['description']}")
            else:
                print(f"    {i + 1}. {item_name}")


def equip_item(player):
    """Let the player equip a weapon or armor from their inventory."""
    # Find equippable items
    equippable = []
    for item_name in player["inventory"]:
        item = data.ITEMS.get(item_name)
        if item and (item["type"] == "weapon" or item["type"] == "armor"):
            equippable.append(item_name)

    if len(equippable) == 0:
        print("  You have no weapons or armor to equip.")
        return

    print("\n  Equippable items:")
    for i in range(len(equippable)):
        item = data.ITEMS[equippable[i]]
        print(f"    {i + 1}. {item['name']} [{item['type']}] - {item['description']}")
    print(f"    0. Cancel")

    pick = input("  > ").strip()
    if pick == "0":
        return

    if not pick.isdigit():
        print("  Invalid choice!")
        return

    index = int(pick) - 1
    if index < 0 or index >= len(equippable):
        print("  Invalid choice!")
        return

    item_name = equippable[index]
    item = data.ITEMS[item_name]

    if item["type"] == "weapon":
        # Unequip current weapon first (remove its bonus)
        if player["weapon"] != "":
            old_weapon = data.ITEMS[player["weapon"]]
            player["attack"] = player["attack"] - old_weapon["attack"]
            player["inventory"].append(player["weapon"])
            print(f"  Unequipped {player['weapon']}.")

        # Equip new weapon
        player["weapon"] = item_name
        player["attack"] = player["attack"] + item["attack"]
        player["inventory"].remove(item_name)
        print(f"  Equipped {item_name}! ATK is now {player['attack']}.")

    elif item["type"] == "armor":
        # Unequip current armor first
        if player["armor"] != "":
            old_armor = data.ITEMS[player["armor"]]
            player["defense"] = player["defense"] - old_armor["defense"]
            player["inventory"].append(player["armor"])
            print(f"  Unequipped {player['armor']}.")

        # Equip new armor
        player["armor"] = item_name
        player["defense"] = player["defense"] + item["defense"]
        player["inventory"].remove(item_name)
        print(f"  Equipped {item_name}! DEF is now {player['defense']}.")


def use_item(player):
    """Let the player use a potion outside of combat."""
    potions = []
    for item_name in player["inventory"]:
        item = data.ITEMS.get(item_name)
        if item and item["type"] == "potion":
            potions.append(item_name)

    if len(potions) == 0:
        print("  You have no potions to use.")
        return

    print("\n  Potions:")
    for i in range(len(potions)):
        item = data.ITEMS[potions[i]]
        print(f"    {i + 1}. {item['name']} - {item['description']}")
    print(f"    0. Cancel")

    pick = input("  > ").strip()
    if pick == "0":
        return
    if not pick.isdigit():
        print("  Invalid choice!")
        return

    index = int(pick) - 1
    if index < 0 or index >= len(potions):
        print("  Invalid choice!")
        return

    item_name = potions[index]
    item = data.ITEMS[item_name]

    if "hp_restore" in item:
        player["hp"] = min(player["hp"] + item["hp_restore"], player["max_hp"])
        print(f"  Used {item['name']}! HP: {player['hp']}/{player['max_hp']}")
    if "mp_restore" in item:
        player["mp"] = min(player["mp"] + item["mp_restore"], player["max_mp"])
        print(f"  Used {item['name']}! MP: {player['mp']}/{player['max_mp']}")

    player["inventory"].remove(item_name)


def discard_item(player):
    """Let the player throw away an item from their inventory."""
    if len(player["inventory"]) == 0:
        print("  Your inventory is empty.")
        return

    print("\n  Which item to discard?")
    for i in range(len(player["inventory"])):
        print(f"    {i + 1}. {player['inventory'][i]}")
    print(f"    0. Cancel")

    pick = input("  > ").strip()
    if pick == "0":
        return
    if not pick.isdigit():
        print("  Invalid choice!")
        return

    index = int(pick) - 1
    if index < 0 or index >= len(player["inventory"]):
        print("  Invalid choice!")
        return

    item_name = player["inventory"][index]
    confirm = input(f"  Discard {item_name}? (y/n): ").strip().lower()
    if confirm == "y":
        player["inventory"].remove(item_name)
        print(f"  Discarded {item_name}.")
    else:
        print("  Cancelled.")


def show_stats(player):
    """Show the player's current stats."""
    print("\n" + "-" * 40)
    print(f"  {player['name']} the {player['class']}")
    print("-" * 40)
    print(f"  HP:  {player['hp']}/{player['max_hp']}")
    print(f"  MP:  {player['mp']}/{player['max_mp']}")
    print(f"  ATK: {player['attack']}  DEF: {player['defense']}")
    print(f"  Gold: {player['gold']}")
    print(f"  Skills:")
    for s in player["skills"]:
        print(f"    - {s['name']} ({s['damage']} dmg, {s['cost']} MP)")


def open_chest(player, room):
    """Open a chest in the current room and add items to inventory."""
    if room["chest"] is None or len(room["chest"]) == 0:
        print("  There is no chest to open here.")
        return

    print("\n  You open the chest! Inside you find:")
    for item_name in room["chest"]:
        player["inventory"].append(item_name)
        item = data.ITEMS.get(item_name)
        if item:
            print(f"    + {item['name']} [{item['type']}] - {item['description']}")
        else:
            print(f"    + {item_name}")

    room["chest"] = []  # chest is now empty
    print("  All items added to your inventory!")


def check_boss_defeated(rooms):
    """Check if the boss has been defeated. Returns True if yes."""
    for room_key in rooms:
        room = rooms[room_key]
        for monster in room["monsters"]:
            if monster["is_boss"] and monster["hp"] > 0:
                return False
    return True


# ===== MAIN GAME LOOP =====

def main():
    # Create the player
    hero = player_module.create_player()

    # Set up the dungeon rooms
    rooms = setup_rooms()
    current_room = "entrance"

    print("\n  Type 'help' to see all commands.")

    # Main game loop
    while True:
        room = rooms[current_room]
        show_room(room)

        # Show available commands
        print("\n  Commands: move | fight | pickup | open | inventory | equip | use | discard | stats | help | quit")
        command = input("\n  > ").strip().lower()

        # --- MOVE ---
        if command == "move":
            print("\n  Where do you want to go?")
            exits = room["exits"]
            directions = list(exits.keys())
            for i in range(len(directions)):
                direction = directions[i]
                dest_name = data.ROOMS[exits[direction]]["name"]
                print(f"    {i + 1}. {direction} -> {dest_name}")
            print(f"    0. Cancel")

            pick = input("  > ").strip()
            if pick == "0":
                continue
            if pick.isdigit():
                index = int(pick) - 1
                if 0 <= index < len(directions):
                    direction = directions[index]
                    current_room = exits[direction]
                    print(f"\n  You move {direction}...")
                else:
                    print("  Invalid choice!")
            else:
                # Also allow typing the direction name directly
                if pick in exits:
                    current_room = exits[pick]
                    print(f"\n  You move {pick}...")
                else:
                    print("  Invalid direction!")

        # --- FIGHT ---
        elif command == "fight":
            # Find alive monsters in the room
            alive = []
            for m in room["monsters"]:
                if m["hp"] > 0:
                    alive.append(m)

            if len(alive) == 0:
                print("  No monsters to fight here.")
                continue

            # Pick which monster to fight
            if len(alive) == 1:
                target = alive[0]
            else:
                print("\n  Which monster do you want to fight?")
                for i in range(len(alive)):
                    print(f"    {i + 1}. {alive[i]['name']} (HP: {alive[i]['hp']})")
                pick = input("  > ").strip()
                if not pick.isdigit():
                    print("  Invalid choice!")
                    continue
                index = int(pick) - 1
                if index < 0 or index >= len(alive):
                    print("  Invalid choice!")
                    continue
                target = alive[index]

            # Start combat
            won = combat.fight(hero, target)

            if not won:
                # Player died - game over
                print("\n" + "=" * 40)
                print("       G A M E   O V E R")
                print("=" * 40)
                print(f"  {hero['name']} the {hero['class']} has fallen.")
                print("  The dungeon claims another soul.\n")
                return  # end the program

            # Check if boss was defeated (win condition)
            if check_boss_defeated(rooms):
                print("\n" + "=" * 40)
                print("  DUNGEON CLEARED!")
                print("=" * 40)
                print(f"\n  Congratulations, {hero['name']} the {hero['class']}!")
                print("  You have defeated the Dragon Lord!")
                print("  The dungeon is free from evil.")
                print(f"\n  Final Stats:")
                print(f"    HP: {hero['hp']}/{hero['max_hp']}")
                print(f"    Gold: {hero['gold']}")
                print(f"    Items: {len(hero['inventory'])}")
                print("\n  Thanks for playing!\n")
                return  # end the program

        # --- PICK UP ITEMS ---
        elif command == "pickup":
            # Check for items on the ground (dropped by monsters in this room)
            # In this simple version, loot goes directly to inventory during combat
            print("  There are no items on the ground.")
            print("  (Items from monsters go to your inventory automatically.)")
            print("  (Use 'open' to open chests.)")

        # --- OPEN CHEST ---
        elif command == "open":
            open_chest(hero, room)

        # --- INVENTORY ---
        elif command == "inventory":
            show_inventory(hero)

        # --- EQUIP ---
        elif command == "equip":
            equip_item(hero)

        # --- USE ITEM ---
        elif command == "use":
            use_item(hero)

        # --- DISCARD ---
        elif command == "discard":
            discard_item(hero)

        # --- STATS ---
        elif command == "stats":
            show_stats(hero)

        # --- HELP ---
        elif command == "help":
            print("\n  === COMMANDS ===")
            print("  move      - Move to another room")
            print("  fight     - Fight a monster")
            print("  pickup    - Pick up items from the ground")
            print("  open      - Open a chest")
            print("  inventory - See your items")
            print("  equip     - Equip a weapon or armor")
            print("  use       - Use a potion")
            print("  discard   - Throw away an item")
            print("  stats     - See your stats")
            print("  quit      - Quit the game")

        # --- QUIT ---
        elif command == "quit":
            confirm = input("  Are you sure? (y/n): ").strip().lower()
            if confirm == "y":
                print("  Goodbye, adventurer!")
                return

        else:
            print("  Unknown command. Type 'help' for a list of commands.")


# Run the game
if __name__ == "__main__":
    main()
