import sys
import random

def run_simple_game():
    # 1. Fundamental Player (with MP and skills based on filez)
    player = {
        "name": input("Enter your hero's name: ").strip() or "Hero",
        "hp": 100,
        "max_hp": 100,
        "mp": 50,
        "max_mp": 50,
        "attack": 20,
        "gold": 0,
        "skills": [
            {"name": "Heavy Strike", "mp_cost": 10, "damage": 40},
            {"name": "Heal", "mp_cost": 15, "heal": 30}
        ]
    }

    # 2. Fundamental World
    rooms = {
        "entrance": {
            "name": "Dungeon Entrance",
            "desc": "A dark, eerie entrance to the dungeon.",
            "monster": None,
            "exits": {"north": "hallway"}
        },
        "hallway": {
            "name": "Cobblestone Hallway",
            "desc": "A long hallway littered with bones.",
            "monster": {"name": "Skeleton", "hp": 40, "attack": 12, "gold": 15, "is_boss": False},
            "exits": {"south": "entrance", "north": "boss_room"}
        },
        "boss_room": {
            "name": "The Shadow Chamber",
            "desc": "A massive circular room radiating dark magic.",
            "monster": {"name": "Shadow Lord", "hp": 120, "attack": 25, "gold": 100, "is_boss": True},
            "exits": {"south": "hallway"}
        }
    }

    current_room_id = "entrance"

    print(f"\nWelcome to the Simple Filez RPG, {player['name']}!")

    # 3. Main Loop
    while True:
        room = rooms[current_room_id]
        print(f"\n=== {room['name']} ===")
        print(room['desc'])
        print("Exits:", ", ".join(room['exits'].keys()))

        # Trigger combat if there's a monster
        if room['monster'] and room['monster']['hp'] > 0:
            monster = room['monster']
            print(f"\nWatch out! {monster['name']} approaches! (HP: {monster['hp']})")
            
            while player["hp"] > 0 and monster["hp"] > 0:
                print(f"\n[You: {player['hp']}/{player['max_hp']} HP | {player['mp']}/{player['max_mp']} MP]  [{monster['name']}: {monster['hp']} HP]")
                print("1. Attack  2. Use Skill")
                action = input("> ").strip()

                if action == "1":
                    damage = player["attack"]
                    monster["hp"] -= damage
                    print(f"You strike {monster['name']} for {damage} damage!")
                elif action == "2":
                    print("Skills:")
                    for i, s in enumerate(player["skills"]):
                        print(f"  {i+1}. {s['name']} ({s['mp_cost']} MP)")
                    s_choice = input("Select skill (or 0 to cancel): ").strip()
                    
                    if s_choice.isdigit() and 1 <= int(s_choice) <= len(player["skills"]):
                        skill = player["skills"][int(s_choice)-1]
                        if player["mp"] >= skill["mp_cost"]:
                            player["mp"] -= skill["mp_cost"]
                            if "damage" in skill:
                                monster["hp"] -= skill["damage"]
                                print(f"You used {skill['name']}! Deals {skill['damage']} damage.")
                            elif "heal" in skill:
                                player["hp"] = min(player["max_hp"], player["hp"] + skill["heal"])
                                print(f"You used {skill['name']}! Restored {skill['heal']} HP.")
                        else:
                            print("Not enough MP!")
                            continue
                    else:
                        continue
                else:
                    print("Invalid action.")
                    continue

                # Monster attacks back if alive
                if monster["hp"] > 0:
                    player["hp"] -= monster["attack"]
                    print(f"{monster['name']} attacks you for {monster['attack']} damage!")

            if player["hp"] <= 0:
                print("\nYou have died... Game Over.")
                return

            print(f"\nYou defeated {monster['name']}!")
            player["gold"] += monster["gold"]
            print(f"Looted {monster['gold']} gold. Total Gold: {player['gold']}")

            if monster["is_boss"]:
                print("\n*** CONGRATULATIONS! ***")
                print("You defeated the Shadow Lord and won the game!")
                return

        # Navigation & Commands
        command = input(f"\nWhat do you want to do? (move <dir> / quit): ").lower().split()
        if not command:
            continue
            
        action = command[0]

        if action == "quit":
            print("Thanks for playing!")
            break
        elif action in ("move", "go"):
            if len(command) > 1:
                direction = command[1]
                if direction in room["exits"]:
                    current_room_id = room["exits"][direction]
                    print(f"You head {direction}.")
                else:
                    print("You can't go that way.")
            else:
                print("Move where?")
        else:
            print("Unknown command. Try: move <dir> or quit.")

if __name__ == "__main__":
    run_simple_game()
