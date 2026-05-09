from typing import Dict

from commands import (
    handle_buy_potion,
    handle_drop,
    handle_equip,
    handle_fight,
    handle_move,
    handle_take,
    handle_use,
)
from data import (
    build_class_presets,
    build_items,
    build_monster_templates,
    build_rooms,
    build_skills,
    create_player,
    spawn_room_monsters,
)
from models import Player, Room


def prompt_choice(prompt: str, options: list) -> str:
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print("Invalid choice. Try again.")


def describe_room(room: Room) -> None:
    print(f"\n== {room.name} ==")
    print(room.description)
    print(f"Room tier: {room.tier}")

    if room.monsters:
        names = ", ".join(monster.name for monster in room.monsters)
        print(f"Monsters here: {names}")
    else:
        print("Monsters here: none")

    if room.items:
        names = ", ".join(item.name for item in room.items)
        print(f"Items here: {names}")
    else:
        print("Items here: none")

    exits = ", ".join(room.exits.keys())
    print(f"Exits: {exits}")


def show_inventory(player: Player) -> None:
    print("\nInventory:")
    if not player.inventory:
        print("  (empty)")
    else:
        for item in player.inventory:
            print(f"  - {item.name} ({item.item_type})")

    print(f"Gold: {player.gold}")
    print(f"HP: {player.hp}/{player.max_hp}")
    print(f"Mana: {player.mana}/{player.max_mana}")
    print(
        f"Equipped: {player.weapon.name if player.weapon else 'None'}, "
        f"{player.armor.name if player.armor else 'None'}"
    )


def create_player_flow(class_presets: Dict[str, Dict]) -> Player:
    name = input("Enter your character name: ").strip() or "Adventurer"
    print("Choose a class: warrior, rogue, mage")
    class_choice = prompt_choice("Class: ", list(class_presets.keys()))
    player = create_player(name, class_choice, class_presets)

    print(
        f"\nWelcome, {player.name} the {player.class_name}! "
        f"HP: {player.hp}, Mana: {player.mana}, ATK: {player.attack}, DEF: {player.defense}"
    )
    print(
        f"Starting gear: {player.weapon.name if player.weapon else 'None'}, "
        f"{player.armor.name if player.armor else 'None'}"
    )
    return player


def check_win_condition(rooms: Dict[str, Room]) -> bool:
    for room in rooms.values():
        if room.tier == "boss":
            if not room.spawned:
                return False
            if room.monsters:
                return False
    return True


def main() -> None:
    print("Text-Based Dungeon Adventure")
    items = build_items()
    skills = build_skills()
    class_presets = build_class_presets(items, skills)
    monster_templates = build_monster_templates(items, skills)
    rooms = build_rooms(items)

    player = create_player_flow(class_presets)
    current_room = rooms["entrance"]

    print("\nType 'help' to see commands. Explore the dungeon and defeat the boss!")

    while True:
        spawn_room_monsters(current_room, monster_templates, skills)
        describe_room(current_room)
        command = input("\n> ").strip().lower()

        if not command:
            continue

        parts = command.split(maxsplit=1)
        verb = parts[0]
        target = parts[1] if len(parts) > 1 else ""

        if verb in {"move", "go"}:
            if not target:
                print("Move where?")
            else:
                current_room = handle_move(current_room, rooms, target)
        elif verb in current_room.exits:
            current_room = handle_move(current_room, rooms, verb)
        elif verb == "look":
            describe_room(current_room)
        elif verb == "inventory":
            show_inventory(player)
        elif verb == "take":
            if not target:
                print("Take what?")
            else:
                handle_take(player, current_room, target)
        elif verb == "drop":
            if not target:
                print("Drop what?")
            else:
                handle_drop(player, current_room, target)
        elif verb == "equip":
            if not target:
                print("Equip what?")
            else:
                handle_equip(player, target)
        elif verb == "use":
            if not target:
                print("Use what?")
            else:
                handle_use(player, target)
        elif verb == "buy":
            if target != "potion":
                print("You can only buy 'potion' here.")
            else:
                potion = items["potion"]
                handle_buy_potion(player, current_room, potion)
        elif verb == "fight":
            survived, _ = handle_fight(player, current_room)
            if not survived:
                print("\nGame Over. You have fallen in the dungeon.")
                break
        elif verb == "help":
            print(
                "Commands: move/go <dir>, look, inventory, take <item>, "
                "drop <item>, equip <item>, use <item>, buy potion, fight, help, quit"
            )
            print("You can also type a direction directly (north/east/south/west).")
        elif verb == "quit":
            print("You leave the dungeon behind.")
            break
        else:
            print("Unknown command. Type 'help' for a list of commands.")

        if not player.is_alive():
            print("\nGame Over. You have fallen in the dungeon.")
            break

        if check_win_condition(rooms):
            print("\nGame Completed: You have defeated all the bosses!")
            break


if __name__ == "__main__":
    main()
