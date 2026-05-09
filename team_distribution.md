# Text RPG Game - 7-Member Team Task Distribution

Based on the structure of the game codebase (`main.py`, `models.py`, `data.py`, `commands.py`, `combat.py`) and the `plan.md`, here is a balanced workload distribution designed for a 7-person team. Each member takes ownership of specific modules and game logic.

## Member 1: Core Engine & Game State Manager
**Primary Focus:** `game/main.py`
**Responsibilities:**
- Implement the primary game loop (prompting user, processing input, rendering output).
- Handle the Win/Lose condition checking (e.g., triggering game over when player dies, or game complete when bosses are defeated).
- Integrate modules from other team members into the main executable flow.
- Ensure the game starts cleanly and prompts for character creation correctly.
- *Related Plan Steps: 1, 10, 11*

## Member 2: Data Architecture & Object Models
**Primary Focus:** `game/models.py`
**Responsibilities:**
- Design the fundamental Python classes representing game entities (`Player`, `Monster`, `Room`, `Item`, `Weapon`, `Armor`, `Skill`).
- Define base attributes and methods for these entities (e.g., `hp`, `attack`, `defense`, `inventory`, getters/setters).
- Ensure models are easily extendable and can interact with each other (e.g., a Room holds a list of Monsters).
- *Related Plan Steps: 2*

## Member 3: Character & Progression Designer
**Primary Focus:** `game/data.py` (Player/Class config)
**Responsibilities:**
- Define the starting stats and parameters for various player classes (Warrior, Rogue, Mage).
- Implement the interactive Player Creation sequence (name input, class choice).
- Assign starting skills and initial equipment.
- Balance the base hit points, attack, and defense across the different character choices.
- *Related Plan Steps: 3, 5*

## Member 4: World Builder & Encounter Designer
**Primary Focus:** `game/data.py` (World, Rooms, Monsters)
**Responsibilities:**
- Map out the dungeon architecture (minimum 3+ rooms) and set valid exits/connections.
- Create rich, descriptive text for environments.
- Define monster stats, descriptions, and place them inside specific rooms.
- Flag and position the main boss(es) in the map.
- *Related Plan Steps: 4*

## Member 5: Command Parser & Navigation Engineer
**Primary Focus:** `game/commands.py`
**Responsibilities:**
- Implement the natural language input parser (routing commands like `move`, `look`, `help`, `quit`).
- Build the navigation logic that physically moves the player between connected rooms.
- Handle "look" commands to dynamically print room descriptions, visible items, and present monsters.
- Output clear and helpful error messages for invalid commands.
- *Related Plan Steps: 9*

## Member 6: Inventory & Economy Developer
**Primary Focus:** `game/commands.py` & Item logic
**Responsibilities:**
- Implement the inventory system (taking items from rooms, dropping items).
- Handle the logic for equipping and unequipping weapons/armor, recalculating player stats accordingly.
- Create the loot drop system: determining what items monsters drop upon defeat and placing them in the room or inventory.
- *Related Plan Steps: 6, 8*

## Member 7: Combat System Architect
**Primary Focus:** `game/combat.py`
**Responsibilities:**
- Construct the turn-based combat loop (player attacks, monster retaliates).
- Calculate damage formulas accounting for base stats, weapon bonuses, and defense mitigation.
- Implement the logic for using class-specific skills during combat (e.g., heavy strikes, heals).
- Return combat results back to the main loop (e.g., monster death, player death).
- *Related Plan Steps: 7*

---

### Collaboration Notes
- **Member 1 (Engine)** and **Member 5 (Parser)** must work closely to ensure user input correctly translates into game state changes.
- **Member 2 (Architecture)** provides the blueprints that **Members 3, 4, 6, and 7** will instantiate and manipulate.
- **Member 4 (World)** and **Member 6 (Economy)** will need to coordinate on how loot tables are attached to monsters and rooms.
