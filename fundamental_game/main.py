import sys


class Monster:
    def __init__(self, name, hp, attack, is_boss=False):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.is_boss = is_boss

class Room:
    def __init__(self, name, description, monster=None):
        self.name = name
        self.description = description
        self.exits = {}
        self.monster = monster

def main():
    print("Welcome to the Fundamental RPG!")
    name = input("Enter your hero's name (or press Enter for 'Hero'): ").strip()
    if not name:
        name = "Hero"
    player = {
        "name": name,
        "hp": 100,
        "attack": 25
    }

    # 1. Setup fundamental world
    room1 = Room("Entrance", "A dark and damp cave entrance.")
    room2 = Room("Hallway", "A long stone hallway.", Monster("Goblin", 30, 10))
    room3 = Room("Throne Room", "A massive room with a dark throne.", Monster("Dragon Boss", 100, 20, is_boss=True))

    room1.exits["north"] = room2
    room2.exits["south"] = room1
    room2.exits["north"] = room3
    room3.exits["south"] = room2

    current_room = room1

    # 2. Main Game Loop
    while True:
        print(f"\n--- {current_room.name} ---")
        print(current_room.description)
        
        if current_room.monster and current_room.monster.hp > 0:
            print(f"Watch out! A {current_room.monster.name} is here! (HP: {current_room.monster.hp})")
        
        print("Exits:", ", ".join(current_room.exits.keys()))
        
        command_input = input(f"\n[{player['hp']} HP] What do you want to do? (move <dir> / look / attack / quit): ").lower()
        command = command_input.split()

        if not command:
            continue

        action = command[0]

        # 3. Fundamental Commands
        if action == "quit":
            print("Thanks for playing!")
            break
            
        elif action == "look":
            print("You look around the room.")
            continue
            
        elif action == "move" or action == "go":
            if len(command) > 1:
                direction = command[1]
                # Can't move if there's an alive monster blocking you
                if current_room.monster and current_room.monster.hp > 0:
                    print(f"The {current_room.monster.name} blocks your path! You must defeat it first.")
                elif direction in current_room.exits:
                    current_room = current_room.exits[direction]
                    print(f"You move {direction}.")
                else:
                    print("You can't go that way.")
            else:
                print("Move where?")
                
        elif action == "attack":
            if current_room.monster and current_room.monster.hp > 0:
                m = current_room.monster
                print(f"\nYou attack the {m.name} for {player['attack']} damage!")
                m.hp -= player['attack']
                
                # Win Condition check
                if m.hp <= 0:
                    print(f"You defeated the {m.name}!")
                    if m.is_boss:
                        print("\n*** CONGRATULATIONS! ***")
                        print("You defeated the boss and won the game!")
                        break
                else:
                    # Monster retaliates
                    print(f"The {m.name} attacks you for {m.attack} damage!")
                    player['hp'] -= m.attack
                    
                    # Lose Condition check
                    if player['hp'] <= 0:
                        print("\nYou have been defeated... Game Over.")
                        break
            else:
                print("There is nothing to attack here.")
                
        else:
            print("Invalid command. Try: move, look, attack, or quit.")

if __name__ == "__main__":
    main()
