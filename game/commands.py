import random
from typing import Dict, Optional, Tuple

from combat import combat_loop
from models import Armor, Item, Player, Potion, Room, Weapon


def find_item_by_name(items: list, name: str) -> Optional[Item]:
    for item in items:
        if item.name.lower() == name:
            return item
    return None


def handle_move(current_room: Room, rooms: Dict[str, Room], direction: str) -> Room:
    if direction not in current_room.exits:
        print("You cannot go that way.")
        return current_room
    return rooms[current_room.exits[direction]]


def handle_take(player: Player, room: Room, target_name: str) -> None:
    item = find_item_by_name(room.items, target_name)
    if not item:
        print("That item is not here.")
        return
    player.add_item(item)
    room.items.remove(item)
    print(f"You picked up {item.name}.")


def handle_drop(player: Player, room: Room, target_name: str) -> None:
    item = find_item_by_name(player.inventory, target_name)
    if not item:
        print("You do not have that item.")
        return
    player.remove_item(item)
    room.items.append(item)
    print(f"You dropped {item.name}.")


def handle_equip(player: Player, target_name: str) -> None:
    item = find_item_by_name(player.inventory, target_name)
    if not item:
        print("You do not have that item.")
        return
    if isinstance(item, Weapon):
        player.weapon = item
        print(f"You equipped {item.name}.")
    elif isinstance(item, Armor):
        player.armor = item
        print(f"You equipped {item.name}.")
    else:
        print("You cannot equip that item.")


def handle_use(player: Player, target_name: str) -> None:
    if target_name == "potion":
        item = next((inv for inv in player.inventory if isinstance(inv, Potion)), None)
    else:
        item = find_item_by_name(player.inventory, target_name)

    if not item:
        print("You do not have that item.")
        return

    if isinstance(item, Potion):
        healed = player.heal(item.heal_amount)
        player.remove_item(item)
        print(f"You use a potion and heal {healed} HP.")
    else:
        print("You cannot use that item right now.")


def handle_buy_potion(player: Player, room: Room, potion: Potion) -> None:
    if not room.has_shop:
        print("There is no shop here.")
        return
    if player.gold < potion.cost:
        print("You do not have enough gold.")
        return
    player.gold -= potion.cost
    player.add_item(potion)
    print(f"You bought a {potion.name} for {potion.cost} gold.")


def handle_fight(player: Player, room: Room) -> Tuple[bool, Optional[str]]:
    if not room.monsters:
        print("There are no monsters to fight.")
        return True, None

    monster = room.monsters[0]
    survived = combat_loop(player, monster)
    if not survived:
        return False, None

    if monster.is_alive():
        return True, monster.name

    room.monsters.remove(monster)
    player.gold += monster.gold_drop
    print(f"You gained {monster.gold_drop} gold.")

    if monster.loot_table:
        loot = random.choice(monster.loot_table)
        room.items.append(loot)
        print(f"{monster.name} dropped {loot.name}.")
    else:
        print(f"{monster.name} dropped nothing.")

    if monster.is_boss:
        print("You have defeated the boss!")

    return True, monster.name
