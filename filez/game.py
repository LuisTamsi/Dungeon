# game.py
# Main game loop. Handles navigation, commands, combat triggers,
# shop access, and win/lose conditions.

import sys
from room import build_rooms, describe_room, collect_room_loot, mark_room_cleared, can_move
from monster import get_monster
from combat import start_combat
from player import (
    show_stats, show_inventory, show_skills,
    equip_item, use_consumable, discard_item,
    open_shop, is_alive as player_alive,
)
from items import describe_item

# Direction aliases
DIRECTIONS = {
    "north": "north", "south": "south", "east": "east", "west": "west",
    "n": "north", "s": "south", "e": "east", "w": "west",
}


def run_game(player):
    rooms = build_rooms()
    current_room_id = "entrance"
    in_combat = False

    print("\n  You step into the dungeon. Good luck.")
    print("  Type 'help' to see all commands.\n")

    while True:
        room = rooms[current_room_id]
        describe_room(room)

        # Auto-trigger combat if enemies are present
        if not room["cleared"] and room["monster_ids"]:
            _trigger_combat(player, room)
            if not player_alive(player):
                _game_over()
                return

        if _check_win(rooms):
            _game_win(player)
            return

        command = input("\n  > ").strip().lower()

        # Parse "go <direction>"
        if command.startswith("go "):
            direction_word = command[3:].strip()
            direction = DIRECTIONS.get(direction_word)
            if not direction:
                print("  Unknown direction. Use: go north / go south / go east / go west")
                continue

            destination = can_move(room, direction)
            if destination:
                current_room_id = destination
            else:
                print(f"  There is no exit to the {direction}.")
            continue

        _handle_command(command, player, room, in_combat=False)

        if _check_win(rooms):
            _game_win(player)
            return


def _trigger_combat(player, room):
    """Fight all monsters in the room sequentially."""
    monster_ids = list(room["monster_ids"])

    for monster_id in monster_ids:
        if not player_alive(player):
            return

        monster = get_monster(monster_id)
        if not monster:
            continue

        result = start_combat(player, monster)

        if result == "lose":
            return

        if result == "flee":
            print("  You escaped. The room is not cleared.")
            return

        # win: remove this monster from the room list
        if monster_id in room["monster_ids"]:
            room["monster_ids"].remove(monster_id)

    if not room["monster_ids"]:
        mark_room_cleared(room)
        print("\n  All enemies defeated. The room is cleared.")


def _handle_command(command, player, room, in_combat=False):
    """Parse and execute a non-movement command."""

    if command == "help":
        _show_help()

    elif command == "look":
        describe_room(room)

    elif command == "stats":
        show_stats(player)

    elif command in ("inventory", "inv"):
        show_inventory(player)

    elif command == "skills":
        show_skills(player)

    elif command == "loot":
        collect_room_loot(room, player)

    elif command == "map":
        print("  Map is handled in the main loop.")

    elif command.startswith("equip "):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            equip_item(player, int(parts[1]) - 1)
        else:
            print("  Usage: equip <item number>")

    elif command.startswith("use "):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            use_consumable(player, int(parts[1]) - 1)
        else:
            print("  Usage: use <item number>")

    elif command.startswith("discard "):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            discard_item(player, int(parts[1]) - 1)
        else:
            print("  Usage: discard <item number>")

    elif command == "shop":
        if in_combat:
            print("  You cannot shop during combat.")
        else:
            open_shop(player)

    elif command in ("quit", "exit"):
        print("\n  You abandon the dungeon. Goodbye.")
        sys.exit(0)

    else:
        print("  Unknown command. Type 'help' for the list.")


def run_game(player):
    """Main loop (overrides the stub above)."""
    rooms = build_rooms()
    current_room_id = "entrance"

    print("\n  You step into the dungeon. Good luck.")
    print("  Type 'help' to see all commands.\n")

    while True:
        room = rooms[current_room_id]
        describe_room(room)

        # Auto-trigger combat if enemies are present
        if not room["cleared"] and room["monster_ids"]:
            _trigger_combat(player, room)
            if not player_alive(player):
                _game_over()
                return

        if _check_win(rooms):
            _game_win(player)
            return

        command = input("\n  > ").strip().lower()

        # "go <direction>"
        if command.startswith("go "):
            direction_word = command[3:].strip()
            direction = DIRECTIONS.get(direction_word)
            if not direction:
                print("  Unknown direction. Use: go north / go south / go east / go west")
                continue
            destination = can_move(room, direction)
            if destination:
                current_room_id = destination
            else:
                print(f"  No exit to the {direction}.")
            continue

        # Map command needs access to rooms
        if command == "map":
            _show_map(rooms)
            continue

        # All other commands
        if command == "help":
            _show_help()
        elif command == "look":
            describe_room(room)
        elif command == "stats":
            show_stats(player)
        elif command in ("inventory", "inv"):
            show_inventory(player)
        elif command == "skills":
            show_skills(player)
        elif command == "loot":
            collect_room_loot(room, player)
        elif command.startswith("equip "):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                equip_item(player, int(parts[1]) - 1)
            else:
                print("  Usage: equip <item number>")
        elif command.startswith("use "):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                use_consumable(player, int(parts[1]) - 1)
            else:
                print("  Usage: use <item number>")
        elif command.startswith("discard "):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                discard_item(player, int(parts[1]) - 1)
            else:
                print("  Usage: discard <item number>")
        elif command == "shop":
            open_shop(player)
        elif command in ("quit", "exit"):
            print("\n  You abandon the dungeon. Goodbye.")
            sys.exit(0)
        else:
            print("  Unknown command. Type 'help' for the list.")

        if _check_win(rooms):
            _game_win(player)
            return


def _show_help():
    print("\n--- Commands ---")
    print("  go north/south/east/west   Move to an adjacent room")
    print("  look                       Describe the current room")
    print("  stats                      Show your stats")
    print("  inventory / inv            Show your inventory")
    print("  skills                     Show your skills and MP costs")
    print("  loot                       Pick up floor/chest items")
    print("  equip <number>             Equip a weapon or armor")
    print("  use <number>               Use a consumable (HP/MP restore)")
    print("  discard <number>           Remove an item from inventory")
    print("  shop                       Open the traveling merchant")
    print("  map                        Show the dungeon map")
    print("  quit                       Exit the game")


def _show_map(rooms):
    print("\n--- Dungeon Map ---")
    for room_id, room in rooms.items():
        tag   = room["room_type"].upper()
        state = "Cleared" if room["cleared"] else "Active"
        exits = ", ".join(room["connections"].keys())
        print(f"  [{tag}] {room['name']}  [{state}]  Exits: {exits}")


def _check_win(rooms):
    return all(room["cleared"] for room in rooms.values() if room["is_boss_room"])


def _game_over():
    print("\n" + "=" * 55)
    print("  G A M E   O V E R")
    print("  You have fallen in the dungeon.")
    print("  The Shadow Lord remains unchallenged.")
    print("=" * 55)
    sys.exit(0)


def _game_win(player):
    print("\n" + "=" * 55)
    print("  V I C T O R Y")
    print(f"  {player['name']} the {player['class']} has cleared the dungeon!")
    print("  The Shadow Lord is defeated. Light returns.")
    print(f"  Gold collected: {player['gold']}")
    print("  Game Completed: You have defeated all the bosses!")
    print("=" * 55)
    sys.exit(0)
