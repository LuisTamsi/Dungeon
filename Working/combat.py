# =============================================================================
# combat.py — Turn-Based Combat Engine
#
# Combat flow (per confirmed design):
#   1. Show monster info
#   2. PLAYER TURN: Attack | Use Skill | Use Item (item use skips attack)
#   3. Check if monster dead → victory
#   4. MONSTER TURN: Random skill → damage player
#   5. Check if player dead → game over
#   Repeat until one side falls.
# =============================================================================

import player as player_module
import monster as monster_module
import items as item_module
import utils


# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------

def start_combat(current_player: dict, enemy: dict) -> bool:
    """
    Run a full combat encounter between the player and one monster.
    Returns True if the player wins, calls player_module.die() on defeat.

    Parameters named 'current_player' to avoid shadowing the player module.
    """
    utils.header(f"COMBAT — {enemy['name']}")
    monster_module.display_monster(enemy)

    while True:
        utils.blank()
        utils.separator()
        _show_combat_status(current_player, enemy)
        utils.separator()

        # ── PLAYER TURN ──────────────────────────────────────────────────
        action = _player_turn_menu(current_player)

        used_item = False

        if action == "1":  # Basic Attack
            _player_basic_attack(current_player, enemy)

        elif action == "2":  # Use Skill
            result = _player_use_skill(current_player, enemy)
            if not result:
                continue  # Skill failed (not enough MP), re-prompt

        elif action == "3":  # Use Item — SKIPS ATTACK TURN
            result = _player_use_item_in_combat(current_player)
            if not result:
                continue  # No consumable used, re-prompt
            used_item = True
            utils.warn("Using an item takes your action — the enemy still attacks!")

        # Check: did the monster die from the player's action?
        if not monster_module.is_alive(enemy):
            _handle_victory(current_player, enemy)
            return True

        # ── MONSTER TURN ──────────────────────────────────────────────────
        monster_module.execute_turn(enemy, current_player)

        # Check: did the player die?
        if not player_module.is_alive(current_player):
            player_module.die(current_player)
            # die() calls sys.exit() so execution never reaches here,
            # but returning False makes the logic explicit for tests.
            return False


# -----------------------------------------------------------------------------
# Player Actions
# -----------------------------------------------------------------------------

def _player_turn_menu(current_player: dict) -> str:
    """Show combat options and return the player's choice."""
    print("\n  What will you do?")
    print("  [1] Attack")
    print("  [2] Use Skill")
    print("  [3] Use Item")
    return utils.get_valid_input("  > ", ["1", "2", "3"])


def _player_basic_attack(current_player: dict, enemy: dict):
    """
    Deal basic attack damage.
    Formula: max(1, player.attack - enemy.defense)
    max(1,...) ensures at least 1 damage — prevents infinite stalemates.
    """
    damage = max(1, current_player["attack"] - enemy["defense"])
    enemy["hp"] = max(0, enemy["hp"] - damage)
    utils.blank()
    print(f"  ⚔  You attack {enemy['name']}!")
    utils.info(f"You deal {damage} damage! ({enemy['name']} HP: {enemy['hp']}/{enemy['max_hp']})")


def _player_use_skill(current_player: dict, enemy: dict) -> bool:
    """
    Show the player's skills, let them pick one, then execute it.
    Returns False if the player can't afford or picks an invalid skill
    (so the combat loop re-prompts without advancing the turn).
    """
    utils.subheader("YOUR SKILLS")
    skills = current_player["skills"]

    for i, skill in enumerate(skills, 1):
        cost = skill.get("mana_cost", 0)
        if skill["type"] == "attack":
            effect = f"{skill.get('damage', 0)} dmg"
        else:
            effect = f"+{skill.get('defense_bonus', 0)} DEF (1 turn)"
        affordable = "✓" if current_player["mp"] >= cost else "✗"
        print(f"  [{i}] {skill['name']} — {effect}  (Cost: {cost} MP) {affordable}")

    print(f"  [0] Back")
    print(f"\n  MP: {current_player['mp']}/{current_player['max_mp']}")

    valid = [str(i) for i in range(len(skills) + 1)]
    choice = utils.get_valid_input("  > ", valid)

    if choice == "0":
        return False

    skill = skills[int(choice) - 1]
    cost  = skill.get("mana_cost", 0)

    if current_player["mp"] < cost:
        utils.warn(f"Not enough MP! Need {cost} MP, you have {current_player['mp']}.")
        return False

    # Deduct mana
    current_player["mp"] -= cost

    stype = skill["type"]
    utils.blank()
    print(f"  ✨ You use {skill['name']}!")

    if stype == "attack":
        raw   = skill.get("damage", 0)
        dmg   = max(1, raw - enemy["defense"])
        enemy["hp"] = max(0, enemy["hp"] - dmg)
        utils.info(f"You deal {dmg} damage! ({enemy['name']} HP: {enemy['hp']}/{enemy['max_hp']})")

    elif stype == "defense":
        bonus = skill.get("defense_bonus", 0)
        current_player["defense"] += bonus
        # Mark for removal after this round
        current_player["_skill_def_bonus"] = current_player.get("_skill_def_bonus", 0) + bonus
        utils.info(f"Your defense increased by {bonus} this turn! (DEF: {current_player['defense']})")

    return True


def _player_use_item_in_combat(current_player: dict) -> bool:
    """
    Show consumables in the player's inventory and use one.
    SKIPS the player's attack — the monster still gets its turn after this.
    Returns False if no consumable was used (so the loop re-prompts).

    Why skip the attack: Using an item in combat is a deliberate trade-off —
    heal now but take a hit. It prevents infinite HP recovery while also attacking.
    """
    # Filter only consumables
    consumables = [
        name for name in current_player["inventory"]
        if name in __import__("data").ITEMS
        and __import__("data").ITEMS[name]["item_type"] == "consumable"
    ]

    if not consumables:
        utils.warn("You have no usable items!")
        return False

    utils.subheader("USE ITEM")
    for i, name in enumerate(consumables, 1):
        item = __import__("data").ITEMS[name]
        print(f"  [{i}] {item_module.describe_item(item)}")
    print("  [0] Back")

    valid = [str(i) for i in range(len(consumables) + 1)]
    choice = utils.get_valid_input("  > ", valid)

    if choice == "0":
        return False

    item_name = consumables[int(choice) - 1]
    item_module.use_item(current_player, item_name)
    return True


# -----------------------------------------------------------------------------
# Post-Combat
# -----------------------------------------------------------------------------

def _handle_victory(current_player: dict, enemy: dict):
    """
    Handle the aftermath of defeating a monster:
    - Roll gold drop
    - Roll item loot
    - Add rewards to player
    - Reset any temporary skill defense bonus
    """
    # Reset any temp defense bonus from player skills
    if current_player.get("_skill_def_bonus", 0) > 0:
        current_player["defense"] -= current_player["_skill_def_bonus"]
        current_player["_skill_def_bonus"] = 0

    utils.blank()
    utils.header(f"VICTORY — {enemy['name']} DEFEATED")

    gold = monster_module.roll_gold(enemy)
    current_player["gold"] += gold
    utils.success(f"You defeated {enemy['name']}!")
    utils.info(f"  Looted {gold} gold. (Total: {current_player['gold']} g)")

    drops = monster_module.roll_loot(enemy)
    if drops:
        for item_name in drops:
            current_player["inventory"].append(item_name)
            utils.success(f"  Item dropped: {item_name}!")
    else:
        utils.info("  No items dropped.")


def _show_combat_status(current_player: dict, enemy: dict):
    """Show a compact side-by-side status of player and enemy HP/MP."""
    print(f"  {current_player['name']} ({current_player['class']})"
          f"    HP: {current_player['hp']}/{current_player['max_hp']}"
          f"    MP: {current_player['mp']}/{current_player['max_mp']}")
    print(f"  {enemy['name']}"
          f"    HP: {enemy['hp']}/{enemy['max_hp']}"
          f"    MP: {enemy['mp']}/{enemy['max_mp']}")
