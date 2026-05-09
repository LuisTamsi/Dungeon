# Game Build Plan (Sequential)

## 1) Define Requirements and Constraints

- Confirm minimum counts: 3+ rooms, 4+ monsters, 2+ item types, 1+ boss.
- Define must-have player features: name input, class choice, hp, attack, skills.
- Define must-have mechanics: inventory, loot drops, combat, win/lose.
- Define input style: command verb + optional target.
- Set completion condition: all bosses defeated.

## 2) Design Data Models

- Item base: name, description, item_type.
- Weapon: attack_bonus.
- Armor: defense_bonus.
- Skill: name, description, effect_type, effect_value.
- Player: name, class_name, hp, max_hp, attack, defense, inventory, skills.
- Monster: name, description, hp, attack, skills, loot_table, is_boss.
- Room: name, description, exits, monsters, items.

## 3) Set Base Stats and Class Presets

- Choose 3 classes with distinct stats (Warrior, Rogue, Mage).
- Assign base hp, attack, defense per class.
- Assign 1 skill per class with clear effect.
- Assign a starting weapon or armor for each class.
- Record all stats as constants for easy tuning.

## 4) Build the Dungeon Map

- Create at least 3 rooms with unique descriptions.
- Define exits with clear directions (north/south/east/west).
- Ensure connections are valid and consistent.
- Place monsters and items in rooms.
- Flag at least one boss monster in a specific room.

## 5) Implement Player Creation

- Prompt for player name.
- Show class choices and validate input.
- Build player object from selected class preset.
- Add starting items to inventory.
- Display a short summary of player stats.

## 6) Implement Inventory Logic

- Add items to inventory with a clean list format.
- Implement equip for weapons and armor.
- Apply stat bonuses on equip.
- Implement use for consumables if any are added later.
- Implement drop and discard with confirmation message.

## 7) Implement Combat Loop

- Decide who goes first (player always first for simplicity).
- Calculate damage: attack + weapon_bonus - defense.
- Allow skills to modify damage or heal.
- Run turn loop until either hp <= 0.
- On player death: print game over and exit.

## 8) Implement Loot Drops

- After monster defeat, roll loot from loot_table.
- Add dropped items to room or directly to inventory.
- Show what dropped and where it went.
- Remove defeated monster from room.

## 9) Implement Command Parser

- Define supported commands: move/go, look, fight, inventory, take, use, drop, help, quit.
- Parse verb and optional target.
- Route to handler functions for each command.
- Provide helpful errors for unknown commands.

## 10) Implement Main Game Loop

- Display room description and visible contents.
- Wait for player command input.
- Execute command handler and update state.
- After each action, check for win/lose.

## 11) Implement Win/Lose Conditions

- Track defeated bosses.
- If all bosses are defeated: print completion and exit.
- If player hp <= 0: print game over and exit.

## 12) Manual Test Checklist

- Room navigation across all exits.
- Combat flow against each monster type.
- Loot drops and inventory changes.
- Equip weapon and armor and verify stat changes.
- Win condition after boss defeat.
- Lose condition when player hp reaches 0.
