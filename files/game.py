# game.py
# The main game loop. Handles player commands, room navigation,
# combat triggers, and win/lose conditions.

import sys
from room import (
    build_rooms, describe_room, get_room_monsters,
    mark_room_cleared, collect_room_loot, can_move
)
from monster import get_monster
from combat import start_combat
from player import is_alive as player_alive
from items import describe_item
from utils import show_stats, show_inventory, show_skills, equip_item, use_consumable, discard_item, is_alive

def run_game(player):
    """
    Main game loop. Runs until the player wins, dies, or quits.
    """
    rooms = build_rooms()
    current_room_id = "entrance"

    print("\n  You step into the dungeon.")
    print("  Type 'help' at any time to see available commands.\n")

    while True:
        room = rooms[current_room_id]

        # Describe the current room
        describe_room(room)

        # Check if we need to fight before anything else
        if not room["cleared"] and room["monsters"]:
            _trigger_combat(player, room, rooms)
            if not player_alive(player):
                _game_over()
                return

        # Check win condition after every combat
        if _check_win(rooms):
            _game_win(player)
            return

        # Prompt for input
        command = input("\n  > ").strip().lower()
        _handle_command(command, player, room, rooms, current_room_id)

        # Move if the command was a direction
        if command in room["connections"]:
            destination = can_move(room, command)
            if destination:
                current_room_id = destination
            else:
                print("  You can't go that way.")


def _trigger_combat(player, room, rooms):
    """
    Fight all monsters in the room one by one.
    If the player dies mid-room, stop immediately.
    """
    monster_ids = list(room["monsters"])  # copy to iterate

    for monster_id in monster_ids:
        if not player_alive(player):
            return

        monster = get_monster(monster_id)
        if not monster:
            continue

        result = start_combat(player, monster)

        if result == "lose":
            return  # player is dead, exit

        if result == "flee":
            # On flee, the player stays in the room but we skip remaining monsters
            print("  You escaped the fight, but the room is not cleared.")
            return

        # result == "win": remove this monster from the room
        room["monsters"].remove(monster_id)

    # If all monsters defeated, clear the room
    if not room["monsters"]:
        mark_room_cleared(room)
        print("\n  All enemies in this room have been defeated.")


def _handle_command(command, player, room, rooms, current_room_id):
    """
    Process a player command.
    Movement commands are handled by the loop by updating current_room_id.
    """
    # Movement
    if command in ("north", "south", "east", "west", "n", "s", "e", "w"):
        # Normalize shorthand
        direction_map = {"n": "north", "s": "south", "e": "east", "w": "west"}
        direction = direction_map.get(command, command)

        destination = can_move(room, direction)
        if not destination:
            print("  There is no exit in that direction.")
        # Actual movement is done in run_game by updating current_room_id
        return

    elif command == "help":
        _show_help()

    elif command == "look":
        describe_room(room)

    elif command == "stats":
        show_stats(player)

    elif command == "inventory" or command == "inv":
        show_inventory(player)

    elif command == "skills":
        show_skills(player)

    elif command == "loot":
        if room["cleared"] or not room["monsters"]:
            collect_room_loot(room, player)
        else:
            print("  You can't loot while enemies are present.")

    elif command.startswith("equip "):
        # equip <number>
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            idx = int(parts[1]) - 1
            equip_item(player, idx)
        else:
            print("  Usage: equip <item number>")

    elif command.startswith("use "):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            idx = int(parts[1]) - 1
            use_consumable(player, idx)
        else:
            print("  Usage: use <item number>")

    elif command.startswith("discard "):
        parts = command.split()
        if len(parts) == 2 and parts[1].isdigit():
            idx = int(parts[1]) - 1
            discard_item(player, idx)
        else:
            print("  Usage: discard <item number>")

    elif command == "map":
        _show_map(rooms)

    elif command == "quit" or command == "exit":
        print("\n  You abandon your quest. Goodbye.")
        sys.exit(0)

    else:
        print("  Unknown command. Type 'help' for a list of commands.")


def _show_help():
    """Print all available commands."""
    print("\n--- Commands ---")
    print("  north / south / east / west  (or n/s/e/w)  Move in a direction")
    print("  look                                        Describe current room")
    print("  stats                                       Show your stats")
    print("  inventory / inv                             Show your inventory")
    print("  skills                                      Show your skills")
    print("  loot                                        Pick up floor items")
    print("  equip <number>                              Equip a weapon or armor")
    print("  use <number>                                Use a consumable")
    print("  discard <number>                            Remove item from inventory")
    print("  map                                         Show dungeon map")
    print("  quit                                        Exit the game")


def _show_map(rooms):
    """Print a simple text map showing which rooms are cleared."""
    print("\n--- Dungeon Map ---")
    for room_id, room in rooms.items():
        status = "Cleared" if room["cleared"] else "Active"
        print(f"  {room['name']} [{status}]")


def _check_win(rooms):
    """
    Win condition: all boss rooms must be cleared.
    """
    for room in rooms.values():
        if room["is_boss_room"] and not room["cleared"]:
            return False
    return True


def _game_over():
    """Print game over screen and exit."""
    print("\n" + "=" * 50)
    print("  GAME OVER")
    print("  You have fallen in the dungeon.")
    print("  Your story ends here.")
    print("=" * 50)
    sys.exit(0)


def _game_win(player):
    """Print win screen and exit."""
    print("\n" + "=" * 50)
    print("  VICTORY")
    print(f"  {player['name']} the {player['class']} has cleared the dungeon!")
    print("  The Shadow Lord is defeated.")
    print("  Light returns to the land.")
    print(f"  Gold collected: {player['gold']}")
    print("  Game Completed: You have defeated all the bosses!")
    print("=" * 50)
    sys.exit(0)
