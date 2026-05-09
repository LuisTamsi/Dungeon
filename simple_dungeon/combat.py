# combat.py - Turn-based combat system
# Handles fighting between the player and a monster.
# Using an item skips the player's attack turn.

import random
import data


def fight(player, monster):
    """Run a fight between the player and a monster. Returns True if player wins."""

    print("\n" + "=" * 40)
    print(f"  BATTLE: {player['name']} vs {monster['name']}!")
    print("=" * 40)
    print(f"  {monster['description']}")

    while True:
        # Show current status
        print(f"\n  --- Your HP: {player['hp']}/{player['max_hp']}  MP: {player['mp']}/{player['max_mp']} ---")
        print(f"  --- {monster['name']} HP: {monster['hp']}/{monster['max_hp']} ---")

        # Player picks an action
        print("\n  1. Attack")
        print("  2. Use Skill")
        print("  3. Use Item (skips your attack)")
        choice = input("  > ").strip()

        # --- PLAYER TURN ---

        if choice == "1":
            # Basic attack
            damage = player["attack"] - monster["defense"]
            if damage < 1:
                damage = 1
            monster["hp"] = monster["hp"] - damage
            if monster["hp"] < 0:
                monster["hp"] = 0
            print(f"\n  You attack! Dealt {damage} damage.")

        elif choice == "2":
            # Use a skill
            result = use_skill(player, monster)
            if result == False:
                continue  # skill failed, pick again

        elif choice == "3":
            # Use an item (skips attack - monster still hits you)
            result = use_item_in_combat(player)
            if result == False:
                continue  # no item used, pick again
            # Skip to monster turn (player doesn't attack)
            print("  You used your turn to use an item.")

        else:
            print("  Invalid choice!")
            continue

        # Check if monster died
        if monster["hp"] <= 0:
            print(f"\n  >> You defeated {monster['name']}!")

            # Drop gold
            player["gold"] = player["gold"] + monster["gold"]
            print(f"  >> Looted {monster['gold']} gold! (Total: {player['gold']})")

            # Roll for loot drops
            for drop in monster["loot"]:
                roll = random.random()  # random number between 0.0 and 1.0
                if roll <= drop["chance"]:
                    player["inventory"].append(drop["item"])
                    print(f"  >> Item dropped: {drop['item']}!")

            return True  # player won

        # --- MONSTER TURN ---
        # Monster picks a random skill
        skill = random.choice(monster["skills"])
        damage = skill["damage"] - player["defense"]
        if damage < 1:
            damage = 1
        player["hp"] = player["hp"] - damage
        if player["hp"] < 0:
            player["hp"] = 0
        print(f"\n  {monster['name']} uses {skill['name']}! Dealt {damage} damage to you.")

        # Check if player died
        if player["hp"] <= 0:
            print("\n  You have been defeated...")
            return False  # player lost


def use_skill(player, monster):
    """Let the player pick a skill to use. Returns False if cancelled."""

    print("\n  Your skills:")
    for i in range(len(player["skills"])):
        skill = player["skills"][i]
        print(f"    {i + 1}. {skill['name']} - {skill['damage']} dmg ({skill['cost']} MP)")
    print(f"    0. Back")
    print(f"  Current MP: {player['mp']}/{player['max_mp']}")

    pick = input("  > ").strip()

    if pick == "0":
        return False

    # Check if valid number
    if not pick.isdigit():
        print("  Invalid choice!")
        return False

    index = int(pick) - 1
    if index < 0 or index >= len(player["skills"]):
        print("  Invalid choice!")
        return False

    skill = player["skills"][index]

    # Check if player has enough MP
    if player["mp"] < skill["cost"]:
        print(f"  Not enough MP! Need {skill['cost']}, you have {player['mp']}.")
        return False

    # Use the skill
    player["mp"] = player["mp"] - skill["cost"]
    damage = skill["damage"] - monster["defense"]
    if damage < 1:
        damage = 1
    monster["hp"] = monster["hp"] - damage
    if monster["hp"] < 0:
        monster["hp"] = 0
    print(f"\n  You use {skill['name']}! Dealt {damage} damage.")
    return True


def use_item_in_combat(player):
    """Let the player use a potion during combat. Returns False if cancelled."""

    # Find potions in inventory
    potions = []
    for item_name in player["inventory"]:
        item = data.ITEMS.get(item_name)
        if item and item["type"] == "potion":
            potions.append(item_name)

    if len(potions) == 0:
        print("  You have no potions to use!")
        return False

    print("\n  Potions:")
    for i in range(len(potions)):
        item = data.ITEMS[potions[i]]
        print(f"    {i + 1}. {item['name']} - {item['description']}")
    print(f"    0. Back")

    pick = input("  > ").strip()

    if pick == "0":
        return False

    if not pick.isdigit():
        print("  Invalid choice!")
        return False

    index = int(pick) - 1
    if index < 0 or index >= len(potions):
        print("  Invalid choice!")
        return False

    item_name = potions[index]
    item = data.ITEMS[item_name]

    # Apply potion effect
    if "hp_restore" in item:
        old_hp = player["hp"]
        player["hp"] = player["hp"] + item["hp_restore"]
        if player["hp"] > player["max_hp"]:
            player["hp"] = player["max_hp"]
        healed = player["hp"] - old_hp
        print(f"  Used {item['name']}! Restored {healed} HP. ({player['hp']}/{player['max_hp']})")

    if "mp_restore" in item:
        old_mp = player["mp"]
        player["mp"] = player["mp"] + item["mp_restore"]
        if player["mp"] > player["max_mp"]:
            player["mp"] = player["max_mp"]
        restored = player["mp"] - old_mp
        print(f"  Used {item['name']}! Restored {restored} MP. ({player['mp']}/{player['max_mp']})")

    # Remove used potion from inventory
    player["inventory"].remove(item_name)
    return True
