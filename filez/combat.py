# combat.py
# Full turn-based combat loop. Returns "win", "lose", or "flee".
# Skills cost mana. No mana = no skills. Consumables usable mid-fight.

import random
from player import show_skills, tick_combat_state, is_alive as player_alive, use_consumable_in_combat
from monster import monster_take_turn, is_alive as monster_alive, roll_loot, roll_gold
from items import get_item


def start_combat(player, monster):
    """Run a full combat encounter. Returns 'win', 'lose', or 'flee'."""
    print("\n" + "=" * 55)
    if monster["is_boss"]:
        print("  *** B O S S  E N C O U N T E R ***")
    print(f"  {monster['name']} appears!")
    print(f"  [{monster['tier'].upper()}] {monster['lore']}")
    print(f"  Weapon: {monster['weapon']['name']}")
    print(f"  HP: {monster['hp']}  ATK: {monster['attack']}  DEF: {monster['defense']}")
    print("=" * 55)

    while player_alive(player) and monster_alive(monster):
        _print_status(player, monster)

        # Check if player is stunned
        if player.get("stunned_turns", 0) > 0:
            player["stunned_turns"] -= 1
            print("\n  You are stunned! You lose your turn.")
        else:
            action = _player_turn(player, monster)
            if action == "flee":
                print("\n  You flee from combat!")
                _clear_combat_debuffs(player)
                return "flee"

        if not monster_alive(monster):
            break

        # Monster's turn
        result = monster_take_turn(monster, player)
        print(f"\n{result['msg']}")

        # Tick player combat state (buffs, shield, etc.)
        tick_combat_state(player)

        # Tick player defense debuff
        if player.get("defense_debuff_turns", 0) > 0:
            player["defense_debuff_turns"] -= 1
            if player["defense_debuff_turns"] == 0:
                player["defense_debuff"] = 0

        if not player_alive(player):
            break

    if not player_alive(player):
        print(f"\n  You have been defeated by {monster['name']}.")
        _clear_combat_debuffs(player)
        return "lose"

    print(f"\n  {monster['name']} has been defeated!")
    _clear_combat_debuffs(player)
    _give_rewards(player, monster)
    return "win"


def _print_status(player, monster):
    eff_atk = player["attack"] + player.get("attack_buff", 0)
    print("\n" + "-" * 45)
    print(f"  You  ({player['class']}):   HP {player['hp']}/{player['max_hp']}   MP {player['mp']}/{player['max_mp']}   ATK {eff_atk}")
    print(f"  {monster['name']}: HP {monster['hp']}/{monster['max_hp']}")
    if player.get("shield_turns", 0) > 0:
        print(f"  [Frost Shield active: {player['shield_turns']} turn(s)]")
    if player.get("evade_next"):
        print("  [Smoke Bomb active: next hit evaded]")
    if player.get("attack_buff_turns", 0) > 0:
        print(f"  [ATK Buff: +{player.get('attack_buff',0)} for {player['attack_buff_turns']} turn(s)]")
    print("-" * 45)


def _player_turn(player, monster):
    print("\n  Actions: [1] Attack  [2] Skill  [3] Item  [4] Flee")
    choice = input("  > ").strip()

    if choice == "1":
        _basic_attack(player, monster)

    elif choice == "2":
        _use_skill(player, monster)

    elif choice == "3":
        _use_item(player)

    elif choice == "4":
        if random.random() < 0.5:
            return "flee"
        else:
            print("  You failed to flee!")
    else:
        print("  Invalid input. You hesitate.")

    return None


def _effective_player_attack(player):
    return player["attack"] + player.get("attack_buff", 0)


def _basic_attack(player, monster):
    raw = _effective_player_attack(player)
    mon_def = monster["defense"] + monster.get("defense_buff", 0)
    damage = max(1, raw - mon_def)
    monster["hp"] -= damage
    print(f"\n  You attack {monster['name']} for {damage} damage!")


def _use_skill(player, monster):
    show_skills(player)
    print("  Choose skill number (0 to cancel):")
    choice = input("  > ").strip()

    if choice == "0":
        print("  Cancelled.")
        return

    if not choice.isdigit():
        print("  Invalid.")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(player["skills"]):
        print("  Invalid skill number.")
        return

    skill = player["skills"][idx]
    cost  = skill["mp_cost"]

    if player["mp"] < cost:
        print(f"  Not enough MP. {skill['name']} costs {cost} MP. You have {player['mp']} MP.")
        print("  Use a Mana Vial or Mana Elixir to restore MP.")
        return

    # Deduct mana
    player["mp"] -= cost

    stype = skill["type"]
    name  = skill["name"]
    mon_def = monster["defense"] + monster.get("defense_buff", 0)
    raw_atk = _effective_player_attack(player)

    if stype == "damage":
        damage = max(1, int(raw_atk * skill["multiplier"]) - mon_def)
        monster["hp"] -= damage
        print(f"\n  You use {name}! Deals {damage} physical damage!")

    elif stype == "magic":
        damage = int(raw_atk * skill["multiplier"])
        monster["hp"] -= damage
        print(f"\n  You use {name}! Magic deals {damage} (ignores defense)!")

    elif stype == "magic_double":
        hit1 = int(raw_atk * skill["multiplier"])
        hit2 = int(raw_atk * skill["multiplier"])
        monster["hp"] -= (hit1 + hit2)
        print(f"\n  You use {name}! Hits twice: {hit1} + {hit2} = {hit1 + hit2} magic damage!")

    elif stype == "stun":
        damage = max(1, int(raw_atk * skill["multiplier"]) - mon_def)
        monster["hp"] -= damage
        monster["stunned"] = True
        print(f"\n  You use {name}! Deals {damage} damage and stuns {monster['name']}!")

    elif stype == "evade":
        player["evade_next"] = True
        print(f"\n  You use {name}! You will evade the next attack!")

    elif stype == "poison":
        damage = max(1, int(raw_atk * skill["multiplier"]) - mon_def)
        monster["hp"] -= damage
        monster["poison_dmg"]   = skill["poison_dmg"]
        monster["poison_turns"] = skill["poison_turns"]
        print(f"\n  You use {name}! Deals {damage} damage and poisons {monster['name']} ({skill['poison_dmg']} dmg/turn for {skill['poison_turns']} turns)!")

    elif stype == "shield":
        dur = skill.get("duration", 2)
        player["shield_turns"] = dur
        print(f"\n  You use {name}! Incoming damage halved for {dur} turn(s)!")

    elif stype == "buff_attack":
        bonus = skill.get("bonus", 5)
        dur   = skill.get("duration", 3)
        player["attack_buff"] = bonus
        player["attack_buff_turns"] = dur
        print(f"\n  You use {name}! ATK +{bonus} for {dur} turn(s)!")

    else:
        print(f"\n  You use {name}. Nothing happens (unknown type).")


def _use_item(player):
    consumables = [(i, item) for i, item in enumerate(player["inventory"]) if item["type"] == "consumable"]
    if not consumables:
        print("  No consumables in inventory.")
        return

    print("  Consumables:")
    for pos, (inv_idx, item) in enumerate(consumables):
        print(f"    [{pos + 1}] {item['name']} - {item['description']}")

    choice = input("  Use which? (0 to cancel): ").strip()
    if choice == "0":
        return

    if not choice.isdigit():
        print("  Invalid.")
        return

    pos = int(choice) - 1
    if pos < 0 or pos >= len(consumables):
        print("  Invalid number.")
        return

    inv_idx = consumables[pos][0]
    use_consumable_in_combat(player, inv_idx)


def _give_rewards(player, monster):
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


def _clear_combat_debuffs(player):
    """Clear temporary debuffs after combat ends."""
    player["defense_debuff"] = 0
    player["defense_debuff_turns"] = 0
    player.setdefault("stunned_turns", 0)
    player["stunned_turns"] = 0
