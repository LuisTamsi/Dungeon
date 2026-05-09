# Text-Based Dungeon Adventure Game Design

This document serves two purposes:

1. A standalone design guide for the game.
2. A walkthrough that mirrors the exact order the code will be written later.

It provides deep reasoning for every section and the flow from the first definition to the last.

## 1) Goals and Non-Goals

### Goals

- Build a text-based dungeon adventure game that runs in the terminal.
- Provide at least 3 interconnected rooms with names, descriptions, and navigation.
- Provide at least 4 monster types, including at least 1 boss.
- Provide at least 2 item types (weapons and armors) with stats.
- Support player name input, class selection, stats, inventory, skills, and item use.
- Implement win/lose combat; player death ends the game.
- Provide a clear dungeon completion condition (e.g., defeat all bosses).

### Non-Goals

- No GUI, graphics, or real-time input.
- No multiplayer, networking, or persistence.
- No complex pathfinding or procedural generation.

Reasoning: Tight scope avoids feature creep and keeps the game testable and explainable in a single file or small module set.

## 2) High-Level Architecture

### Modules (planned)

- main module: game loop, input parsing, state transitions.
- entities module: Player, Monster, and item data models.
- combat module: combat loop, damage resolution, win/lose checks.
- world module: rooms, connections, and dungeon completion logic.

Reasoning: Modularization keeps each concern isolated. It makes debugging easier, allows focused tests, and aligns with the request for clear code structure.

## 3) Walkthrough in Exact Code Order

This section is written to match the future code order. Each step explains the reasoning behind the design choices.

### 3.1) Imports and Constants

Planned content:

- Standard library imports for typing and randomization.
- Constants for base stats, class choices, and item categories.

Reasoning: Randomization is necessary for combat variance and loot drops. Type hints help readability and debugging in a CLI game where object relationships can become complex.

### 3.2) Data Models: Items

Planned definitions:

- Base Item with name, description, and type.
- Weapon and Armor subtypes with attack and defense modifiers.

Reasoning: Items are split by type because weapons and armor affect different stats. This makes stat application explicit and prevents ambiguous item effects.

### 3.3) Data Models: Skills

Planned definitions:

- Skill name, description, and effect (e.g., extra damage, heal).
- Lightweight representation so both player and monsters can use skills.

Reasoning: Skills add tactical depth without requiring complex systems. A shared structure reduces duplication between player and monster abilities.

### 3.4) Data Models: Player

Planned definitions:

- Player class with name, class type, hp, attack, defense, inventory, and skills.
- Methods: take_damage, heal, equip_item, use_item, add_item, remove_item.

Reasoning: The player is the central state holder. Methods encapsulate how stats change and prevent scattered mutations across the code.

### 3.5) Data Models: Monster

Planned definitions:

- Monster class with name, description, hp, attack, skills, loot table, and boss flag.
- Method: take_damage and drop_loot.

Reasoning: Monsters mirror player stats to keep combat logic symmetrical. Loot is stored in the monster so that the combat module can request it on defeat.

### 3.6) World Model: Room

Planned definitions:

- Room name, description, exits (connections), and contents (monsters/items).
- Method: describe and get_exit.

Reasoning: A room is a container for narrative and gameplay elements. Using explicit exits makes navigation deterministic and easy to validate.

### 3.7) World Setup: Dungeon Map

Planned definitions:

- At least 3 rooms: e.g., Tavern, Hallway, Boss Chamber.
- Connections: bidirectional where appropriate.
- Initial monsters and items placed in rooms.

Reasoning: Fixed rooms keep the game predictable and easier to reason about in a learning context. Bidirectional connections prevent player dead ends unless intentionally designed.

### 3.8) Class Selection and Player Creation

Planned flow:

- Prompt user for character name.
- Offer class choices (Warrior, Rogue, Mage) with distinct stats.
- Assign class skills and base inventory.

Reasoning: Class choice provides replay value and demonstrates how stats affect combat outcomes. Assigning starting gear ensures every class is viable from the first combat.

### 3.9) Command Parsing Layer

Planned commands:

- move/go <direction>
- look
- inventory
- take <item>
- use <item>
- drop <item>
- fight
- help
- quit

Reasoning: A simple verb-noun grammar keeps the input model easy to understand. It is also easy to parse in a terminal without external libraries.

### 3.10) Combat System

Planned flow:

- Initiate when player uses fight or enters a room with aggressive monsters.
- Turn-based loop: player action then monster action.
- Damage = attacker attack + weapon bonus - defender defense.
- Skills can modify damage or heal.
- End conditions: monster hp <= 0 or player hp <= 0.

Reasoning: Turn-based combat is predictable and easy to debug. A clear damage formula ensures the impact of items is measurable. Skills add variety without complicating flow.

### 3.11) Loot and Inventory Management

Planned flow:

- Defeated monster drops loot, which can be added to inventory.
- Player can equip weapon/armor to gain stat bonuses.
- Player can discard items to manage inventory.

Reasoning: Loot is a core RPG loop. Inventory management creates decisions and uses the item model in multiple contexts.

### 3.12) Game Progression and Win Condition

Planned logic:

- Track defeated bosses.
- If all bosses are defeated, display completion message and exit.
- If player hp <= 0, display game over message and exit.

Reasoning: A clear completion condition is required. Bosses are natural milestones and align with the requirement of at least one boss monster.

### 3.13) Main Game Loop

Planned flow:

- Initialize world and player.
- Enter loop: show room description, wait for command, process action.
- After each command, check win/lose conditions.

Reasoning: The loop ties together world, player, combat, and inventory. Checking win/lose after actions avoids unnecessary complexity.

## 4) Example Entities and World (Design Reference)

### Player Classes

- Warrior: high hp, moderate attack, skill: Power Strike.
- Rogue: moderate hp, high attack, skill: Backstab.
- Mage: low hp, high attack, skill: Firebolt.

Reasoning: These archetypes are familiar and illustrate trade-offs in a simple stat system.

### Monsters (Minimum 4 types)

- Goblin: weak, common.
- Skeleton: moderate, resilient.
- Slime: low attack, high hp.
- Dragon (Boss): high hp and attack.

Reasoning: Variety in stats makes combat less repetitive. A boss with stronger stats creates a clear endgame objective.

### Items (Minimum 2 types)

- Weapon: Longsword (+attack).
- Armor: Leather Armor (+defense).

Reasoning: Two item types fulfill requirements and demonstrate stat modification and equipment logic.

## 5) Why This Structure Works

- The data models (Player, Monster, Room, Items) define the game state clearly.
- The combat module is isolated and reusable for any encounter.
- The command parser keeps the game loop simple and reduces branching complexity.
- The win/lose conditions are explicit and easy to test.

## 6) Next Step

When you say the word, I will begin writing the actual code in the order described above.
