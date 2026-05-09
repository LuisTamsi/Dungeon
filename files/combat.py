# combat.py
# Handles the full turn-based combat loop between player and monster.
# Returns "win", "lose", or "flee" when combat ends.

import random
from items import get_item, describe_item
from utils import tick_cooldowns
from player import is_alive as player_alive
from monster import monster_take_turn, is_alive as monster_alive, roll_loot, roll_gold
# pyrefly: ignore [missing-import]
from utils import show_skills


def start_combat(player, monster):
    """
    Run a full combat encounter.
    Returns: "win", "lose", or "flee"
    """
    print("\n" + "=" * 50)
    if monster["is_boss"]:
        print(f"  *** BOSS ENCOUNTER ***")
    print(f"  {monster['name']} appears!")
    print(f"  [{monster['type']}] {monster['lore']}")
    print(f"  HP: {monster['hp']}  ATK: {monster['attack']}  DEF: {monster['defense']}")
    print("=" * 50)

    while player_alive(player) and monster_alive(monster):
        _show_combat_status(player, monster)
        action = _player_turn(player, monster)

        if action == "flee":
            print("\n  You flee from combat!")
            return "flee"

        if not monster_alive(monster):
            break

        # Monster's turn
        result = monster_take_turn(monster, player)
        print(f"\n{result}")

        # Tick player cooldowns at end of turn
        tick_cooldowns(player)

        # Tick player shield
        if player.get("shield_turns", 0) > 0:
            player["shield_turns"] -= 1

        if not player_alive(player):
            break

    if not player_alive(player):
        print(f"\n  You have been defeated by {monster['name']}.")
        return "lose"

    # Player won
    print(f"\n  {monster['name']} has been defeated!")
    _distribute_rewards(player, monster)
    return "win"


def _show_combat_status(player, monster):
    """Print a short status line for both sides."""
    print("\n" + "-" * 40)
    print(f"  You ({player['class']}): {player['hp']}/{player['max_hp']} HP")
    print(f"  {monster['name']}: {monster['hp']}/{monster['max_hp']} HP")
    print("-" * 40)


def _player_turn(player, monster):
    """
    Ask the player for their action this turn.
    Returns "flee" if they choose to flee, otherwise None.
    """
    print("\n  What do you do?")
    print("  [1] Attack")
    print("  [2] Use Skill")
    print("  [3] Use Item")
    print("  [4] Flee")

    choice = input("  > ").strip()

    if choice == "1":
        _player_attack(player, monster)

    elif choice == "2":
        _player_use_skill(player, monster)

    elif choice == "3":
        _player_use_item_in_combat(player)

    elif choice == "4":
        # 50% chance to flee
        if random.random() < 0.5:
            return "flee"
        else:
            print("  You failed to flee!")

    else:
        print("  Invalid choice. You hesitate and lose your turn.")

    return None


def _player_attack(player, monster):
    """Basic player attack."""
    raw = player["attack"]

    # Check if monster has a shield active
    monster_defense = monster["defense"]
    if monster.get("shield_turns", 0) > 0:
        monster_defense = int(monster_defense * 1.5)
        monster["shield_turns"] -= 1

    damage = max(1, raw - monster_defense)
    monster["hp"] -= damage
    print(f"\n  You attack {monster['name']} for {damage} damage!")


def _player_use_skill(player, monster):
    """Let the player pick and use a skill."""
    show_skills(player)
    print("  Choose a skill number (or 0 to cancel):")
    choice = input("  > ").strip()

    if choice == "0":
        print("  Cancelled.")
        return

    try:
        idx = int(choice) - 1
        skill = player["skills"][idx]
    except (ValueError, IndexError):
        print("  Invalid skill.")
        return

    if skill["current_cooldown"] > 0:
        print(f"  {skill['name']} is on cooldown for {skill['current_cooldown']} more turn(s).")
        return

    # Set cooldown
    skill["current_cooldown"] = skill["cooldown"]
    stype = skill["type"]

    monster_defense = monster["defense"]
    if monster.get("shield_turns", 0) > 0:
        monster_defense = int(monster_defense * 1.5)

    if stype == "damage":
        raw = int(player["attack"] * skill["multiplier"])
        damage = max(1, raw - monster_defense)
        monster["hp"] -= damage
        print(f"\n  You use {skill['name']}! Deals {damage} damage!")

    elif stype == "magic":
        # Ignores defense
        damage = int(player["attack"] * skill["multiplier"])
        monster["hp"] -= damage
        print(f"\n  You use {skill['name']}! Magic deals {damage} damage (ignores defense)!")

    elif stype == "stun":
        raw = int(player["attack"] * skill["multiplier"])
        damage = max(1, raw - monster_defense)
        monster["hp"] -= damage
        monster["stunned"] = True
        print(f"\n  You use {skill['name']}! Deals {damage} damage and stuns {monster['name']}!")
        # On a stun, the monster skips its next turn
        print(f"  {monster['name']} is stunned and will skip its next turn!")
        _skip_monster_turn(monster)

    elif stype == "evade":
        player["evade_next"] = True
        print(f"\n  You use {skill['name']}! You will evade the next attack!")

    elif stype == "shield":
        duration = skill.get("duration", 2)
        player["shield_turns"] = duration
        print(f"\n  You use {skill['name']}! Incoming damage reduced by 50% for {duration} turn(s)!")

    else:
        print(f"\n  You use {skill['name']}! Nothing happens... (unknown skill type)")


def _skip_monster_turn(monster):
    """Force monster to skip its next turn by consuming its turn here."""
    # We simulate this by doing nothing and letting the caller know.
    # The monster's turn is already about to execute in start_combat,
    # so we mark the monster stunned and check it in monster_take_turn.
    pass  # Stun is handled in monster.py's monster_take_turn via monster["stunned"]


def _player_use_item_in_combat(player):
    """Use a consumable from inventory during combat."""
    inv = player["inventory"]
    consumables = [(i, item) for i, item in enumerate(inv) if item["type"] == "consumable"]

    if not consumables:
        print("  No usable consumables in inventory.")
        return

    print("  Consumables:")
    for idx, (inv_idx, item) in enumerate(consumables):
        print(f"    [{idx + 1}] {item['name']}: {item['description']}")

    choice = input("  Use which? (0 to cancel): ").strip()
    if choice == "0":
        return

    try:
        chosen_idx = int(choice) - 1
        inv_idx, item = consumables[chosen_idx]
    except (ValueError, IndexError):
        print("  Invalid choice.")
        return

    heal = item.get("heal_amount", 0)
    player["hp"] = min(player["hp"] + heal, player["max_hp"])
    player["inventory"].pop(inv_idx)
    print(f"  Used {item['name']}. Restored {heal} HP. HP: {player['hp']}/{player['max_hp']}")


def _distribute_rewards(player, monster):
    """Give the player gold and loot after winning a fight."""
    gold = roll_gold(monster)
    player["gold"] += gold
    print(f"  You loot {gold} gold.")

    drops = roll_loot(monster)
    if drops:
        for item_id in drops:
            item = get_item(item_id)
            if item:
                player["inventory"].append(item)
                print(f"  Item dropped: {item['name']} - {item['description']}")
    else:
        print("  No items dropped.")
