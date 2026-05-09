# =============================================================================
# main.py — Game Entry Point and Main Loop
#
# Responsibilities:
#   - Initialise game state (player + rooms)
#   - Display the current room on entry
#   - Parse and route all typed commands
#   - Check win condition after each action
#
# Command set:
#   go <direction>       — move to adjacent room
#   look                 — re-display current room
#   fight [name]         — fight a monster (optional specific target)
#   pickup <item>        — pick up an item from the floor
#   open chest           — open the Treasure Vault chest
#   inventory / inv      — show inventory, equipment, gold
#   equip <item>         — equip a weapon or armor
#   unequip <slot>       — unequip weapon or armor slot
#   use <item>           — use a consumable outside combat
#   discard <item>       — permanently discard an item
#   stats                — show player stats
#   skills               — show player skills
#   help                 — list all commands
#   quit                 — exit the game
# =============================================================================

import copy
import sys

import data
import player as player_module
import rooms as rooms_module
import items as item_module
import utils


# -----------------------------------------------------------------------------
# Game Initialisation
# -----------------------------------------------------------------------------

def _init_rooms() -> dict:
    """
    Create a deep copy of the room templates from data.ROOMS.
    This is the live game state — modifications (cleared, monsters, etc.)
    happen here and do NOT touch the original data.ROOMS templates.

    Why deepcopy: if we used data.ROOMS directly, the 'cleared' and
    'monsters' fields would be permanently mutated across game sessions
    (or if main() were ever called twice in a test context).
    """
    return copy.deepcopy(data.ROOMS)


def _check_win(rooms: dict) -> bool:
    """
    Return True if the boss chamber has been cleared.
    This is the single win condition: defeat the Dungeon Lord.
    """
    return rooms["boss_chamber"]["cleared"]


# -----------------------------------------------------------------------------
# Command Help
# -----------------------------------------------------------------------------

HELP_TEXT = """
  ╔══════════════════════════════════════════════════════╗
  ║                  COMMAND REFERENCE                   ║
  ╠══════════════════════════════════════════════════════╣
  ║  go <direction>     Move: north / south / east / west║
  ║  look               Redisplay the current room       ║
  ║  fight [name]       Fight a monster (optional name)  ║
  ║  pickup <item>      Pick up an item from the floor   ║
  ║  open chest         Open the Treasure Vault chest    ║
  ╠══════════════════════════════════════════════════════╣
  ║  inventory / inv    Show inventory, equipment, gold  ║
  ║  equip <item>       Equip a weapon or armor          ║
  ║  unequip <slot>     Unequip 'weapon' or 'armor' slot ║
  ║  use <item>         Use a consumable item            ║
  ║  discard <item>     Permanently discard an item      ║
  ╠══════════════════════════════════════════════════════╣
  ║  stats              Show your current stats          ║
  ║  skills             Show your skills and mana costs  ║
  ║  help               Show this command list           ║
  ║  quit               Quit the game                    ║
  ╚══════════════════════════════════════════════════════╝
"""


# -----------------------------------------------------------------------------
# Main Loop
# -----------------------------------------------------------------------------

def main():
    """
    Main game loop.

    Variable naming: the player dict is called 'current_player' throughout
    main.py to avoid shadowing the 'player' module name (which was the bug
    in the original main.py: `player = player.new_player()` crashed because
    'player' the module was overwritten by 'player' the dict on the same line).
    """
    # --- Setup ---
    current_player = player_module.new_player()
    rooms = _init_rooms()
    current_room_key = "entrance"

    # Enter the first room
    rooms_module.enter_room(current_player, rooms[current_room_key])

    # --- Command Loop ---
    while True:
        utils.blank()
        raw = input("  > ").strip()
        if not raw:
            continue

        parts = raw.lower().split()
        verb  = parts[0]
        args  = parts[1:]  # everything after the verb

        # ── Navigation ───────────────────────────────────────────────────
        if verb == "go" and args:
            direction = args[0]
            dest_key  = rooms_module.navigate(rooms, current_room_key, direction)
            if dest_key:
                current_room_key = dest_key
                rooms_module.enter_room(current_player, rooms[current_room_key])

                if _check_win(rooms):
                    _win_screen(current_player)
                    return

        elif verb == "go" and not args:
            utils.warn("Go where? Try: go north / go south / go east / go west")

        # ── Look ─────────────────────────────────────────────────────────
        elif verb == "look":
            rooms_module.enter_room(current_player, rooms[current_room_key])

        # ── Fight ─────────────────────────────────────────────────────────
        elif verb == "fight":
            target = " ".join(args) if args else ""
            # Reconstruct proper-case name (e.g. "dark elf" → "Dark Elf")
            target = target.title()
            rooms_module.fight(current_player, rooms[current_room_key], target)

            if _check_win(rooms):
                _win_screen(current_player)
                return

        # ── Pick Up ───────────────────────────────────────────────────────
        elif verb == "pickup" and args:
            item_name = " ".join(args).title()
            rooms_module.pickup_item(
                current_player, rooms[current_room_key], item_name
            )

        elif verb == "pickup" and not args:
            utils.warn("Pick up what? Try: pickup health potion")

        # ── Open Chest ────────────────────────────────────────────────────
        elif verb == "open" and args and args[0] == "chest":
            rooms_module.open_chest(current_player, rooms[current_room_key])

        elif verb == "open":
            utils.warn("Open what? Try: open chest")

        # ── Inventory ────────────────────────────────────────────────────
        elif verb in ("inventory", "inv"):
            item_module.show_inventory(current_player)

        # ── Equip ────────────────────────────────────────────────────────
        elif verb == "equip" and args:
            item_name = " ".join(args).title()
            item_module.equip_item(current_player, item_name)

        elif verb == "equip" and not args:
            utils.warn("Equip what? Try: equip iron sword")

        # ── Unequip ───────────────────────────────────────────────────────
        elif verb == "unequip" and args:
            slot = args[0].lower()
            item_module.unequip_item(current_player, slot)

        elif verb == "unequip" and not args:
            utils.warn("Unequip which slot? Try: unequip weapon  or  unequip armor")

        # ── Use Item ─────────────────────────────────────────────────────
        elif verb == "use" and args:
            item_name = " ".join(args).title()
            item_module.use_item(current_player, item_name)

        elif verb == "use" and not args:
            utils.warn("Use what? Try: use health potion")

        # ── Discard ──────────────────────────────────────────────────────
        elif verb == "discard" and args:
            item_name = " ".join(args).title()
            item_module.discard_item(current_player, item_name)

        elif verb == "discard" and not args:
            utils.warn("Discard what? Try: discard mana potion")

        # ── Stats / Skills ───────────────────────────────────────────────
        elif verb == "stats":
            player_module.show_stats(current_player)

        elif verb == "skills":
            player_module.show_skills(current_player)

        # ── Help ─────────────────────────────────────────────────────────
        elif verb == "help":
            print(HELP_TEXT)

        # ── Quit ─────────────────────────────────────────────────────────
        elif verb == "quit":
            if utils.confirm("Are you sure you want to quit?"):
                utils.info("Farewell, adventurer. The dungeon remains unconquered.")
                sys.exit(0)

        else:
            utils.warn(f"Unknown command: '{raw}'. Type 'help' to see all commands.")


# -----------------------------------------------------------------------------
# Win Screen
# -----------------------------------------------------------------------------

def _win_screen(current_player: dict):
    """Display the victory screen and exit."""
    utils.blank()
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║                                                  ║")
    print("  ║         D U N G E O N  C L E A R E D !          ║")
    print("  ║                                                  ║")
    print("  ╚══════════════════════════════════════════════════╝")
    utils.blank()
    print(f"  Congratulations, {current_player['name']} the {current_player['class']}!")
    print("  You have slain the Dungeon Lord and broken the curse.")
    print("  The dungeon crumbles behind you as you walk into the light.")
    utils.blank()
    print(f"  Final Stats:")
    print(f"    HP Remaining : {current_player['hp']}/{current_player['max_hp']}")
    print(f"    MP Remaining : {current_player['mp']}/{current_player['max_mp']}")
    print(f"    Gold Earned  : {current_player['gold']} g")
    print(f"    Items Held   : {len(current_player['inventory'])}")
    utils.blank()
    print("  ════════════════════════════════════════════════════")
    print("            Thank you for playing. Well done.")
    print("  ════════════════════════════════════════════════════")
    utils.blank()
    sys.exit(0)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()