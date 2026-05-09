# Dungeon of Shadows - Full Documentation

## Overview

This is a text-based dungeon crawler written in Python.
The player types commands in a terminal to navigate rooms,
fight monsters, collect loot, and defeat the final boss.

The project is split into 6 modules plus an entry point.
Each module has one clear job. Nothing overlaps.

---

## File Structure

    dungeon/
    ├── main.py      Entry point. Starts the game.
    ├── items.py     Item definitions (weapons, armors, consumables).
    ├── player.py    Player creation, stats, inventory, skills.
    ├── monster.py   Monster definitions, AI, loot, combat math.
    ├── room.py      Dungeon map, room data, connections.
    ├── combat.py    Full combat loop between player and monster.
    └── game.py      Game loop, command parsing, win/lose logic.

The load order matters:
items.py has no dependencies.
player.py imports items.py.
monster.py has no dependencies.
room.py imports items.py.
combat.py imports player.py, monster.py, items.py.
game.py imports room.py, monster.py, combat.py, player.py, items.py.
main.py imports player.py and game.py.

---

## items.py

### Why this file exists first

Items are the simplest data in the game. Nothing else needs to
be loaded before items. Weapons, armors, and consumables are
all defined here as plain Python dictionaries.

### Structure of an item

Every item is a dictionary with these keys:

    id           Unique string key. Used to reference items across modules.
    name         Display name shown to the player.
    type         "weapon", "armor", or "consumable".
    description  Short lore or flavor text.

Weapons also have:

    attack_bonus   Integer added to the player's attack stat.

Armors also have:

    defense_bonus  Integer added to the player's defense stat.

Consumables also have:

    heal_amount    Integer HP restored when used.

### Why dictionaries, not classes?

Classes add boilerplate. For this scale of game, a dictionary
is readable, easy to copy, and easy to pass around. There is no
behavior on items themselves. They just hold data.

### get_item(item_id)

Returns a fresh copy of an item by its ID string.
The copy is important. If we returned the original, equipping
the same item twice would cause both the inventory and the
equipped slot to point to the same dict. Changes to one
would affect the other.

### describe_item(item)

Prints item details to the terminal. Used in inventory display
and loot drops. Checks item type to decide which stat to show.

### Item catalog

Weapons (6 total):
- rusty_sword (+3 ATK): Starting-tier weapon.
- iron_axe (+6 ATK): Mid-tier melee weapon.
- shadow_dagger (+5 ATK): Rogue-flavored weapon.
- oak_staff (+4 ATK): Mage's weapon.
- bone_sword (+8 ATK): High-tier drop from elite monsters.
- doom_blade (+15 ATK): Boss drop. Best weapon in the game.

Armors (5 total):
- leather_vest (+3 DEF): Common starting armor.
- iron_shield (+6 DEF): Mid-tier defense.
- shadow_cloak (+4 DEF): Rogue-flavored armor.
- mage_robe (+2 DEF): Low defense, fits Mage's style.
- dark_armor (+10 DEF): Rare elite drop. Best armor in the game.

Consumables (2 total):
- health_potion: Restores 30 HP.
- elixir: Restores 60 HP.

---

## player.py

### Why this comes second

The player needs items to exist first, because equipping changes
the player's attack and defense values based on item stats.
Player also references item functions directly (describe_item).

### CLASSES dictionary

Three classes are defined:

    "1": Warrior   HP: 120  ATK: 15  DEF: 10
    "2": Rogue     HP: 90   ATK: 18  DEF: 6
    "3": Mage      HP: 80   ATK: 20  DEF: 4

Each class has a skill list. Skills are stored as dictionaries
with these keys:

    name              Display name.
    description       Explains what the skill does.
    cooldown          How many turns before the skill can be used again.
    current_cooldown  Tracks remaining wait time. Starts at 0 (ready).
    type              "damage", "magic", "stun", "evade", or "shield".
    multiplier        Scales the player's attack stat for damage output.

Design reasoning for the three classes:

Warrior has the most HP and solid defense. Low ceiling on damage
but very forgiving. Good for new players.

Rogue has high attack and a massive damage multiplier (Backstab
at 2.5x). Low HP forces aggressive play. Smoke Bomb adds a
safety valve against one hit.

Mage has the highest attack and a 3x damage skill that ignores
defense. Glass cannon. Frost Shield compensates partially.

### create_player()

Walks through character creation step by step:

1. Ask for a name. Default to "Adventurer" if empty.
2. Display class options with stats.
3. Accept input 1, 2, or 3. Reject anything else.
4. Deep copy the class data into a fresh player dictionary.

Why deep copy? The CLASSES dict is a module-level constant.
If we just assigned it, the player's skill cooldowns would
mutate the class template. Every new game would start with
whatever cooldowns the last game left behind.

### Player dictionary keys

    name             Player's name.
    class            Class name string.
    hp               Current HP.
    max_hp           Maximum HP.
    attack           Current attack (base + weapon bonus).
    defense          Current defense (base + armor bonus).
    base_attack      Original attack stat without equipment.
    base_defense     Original defense stat without equipment.
    skills           List of skill dicts with cooldowns.
    inventory        List of item dicts.
    weapon           Currently equipped weapon dict (or None).
    armor            Currently equipped armor dict (or None).
    gold             Gold collected.
    shield_turns     Tracks Frost Shield duration.
    evade_next       True if Smoke Bomb is active.
    stunned          Unused for player but kept for symmetry with monsters.

### equip_item(player, index)

Takes an index into the inventory list.
If a weapon is already equipped, it goes back into inventory.
Then the selected item replaces the equipped slot.
Attack or defense is recalculated from base stat + item bonus.

Why store base stats separately? Without them, we cannot know
what the player's attack was before equipping. Swapping weapons
would stack bonuses incorrectly.

### use_consumable(player, index)

Heals the player by the item's heal_amount.
Clamps HP to max_hp. Removes the item from inventory.

### tick_cooldowns(player)

Called at the end of every combat turn.
Decrements current_cooldown by 1 for each skill.
Minimum is 0. Skills never go negative.

### is_alive(player)

Returns True if hp > 0. Used by combat.py and game.py
to check if the game should continue.

---

## monster.py

### Purpose

Defines all monsters and their combat AI.
Monsters are also plain dictionaries. get_monster() always
returns a deep copy so each fight is independent.

### MONSTER_TEMPLATES keys

    id             Unique string key.
    name           Display name.
    type           "Common", "Undead", "Caster", "Elite", or "BOSS".
    lore           One or two sentences of flavor text.
    hp / max_hp    Hit points.
    attack         Base damage stat.
    defense        Reduces incoming physical damage.
    gold_drop      Tuple (min, max) for random gold reward.
    loot_table     List of item IDs that can drop.
    loot_chance    Float 0.0 to 1.0. Boss is always 1.0.
    skills         List of skill dicts.
    is_boss        True only for the Shadow Lord.

### The four monster types

Goblin (Common):
HP: 30. Weak but fast. Cheap Shot hits at 1.5x.
Found in pairs at the entrance. Designed as a tutorial fight.

Skeleton Warrior (Undead):
HP: 45. Mid-range threat. Bone Slash hits at 1.8x.
Higher defense than the goblin.

Dark Mage (Caster):
HP: 55. Low defense but dangerous. Shadow Bolt ignores defense.
Drain Life heals the mage while hurting the player.
Forces the player to kill it fast or get out-sustained.

Stone Golem (Elite):
HP: 90. Highest HP of regular monsters. Quake Slam at 2.2x
is the hardest non-boss hit. Stone Skin temporarily increases
effective defense. A tough fight even for a geared player.

Shadow Lord (BOSS):
HP: 200. Three skills. Shadow Wave ignores defense.
Void Crush is the hardest hit in the game at 3x attack.
Dark Regeneration heals 20 HP on a 6-turn cooldown.
Always drops loot.

### monster_take_turn(monster, player)

This is the monster AI function.

Step 1: Tick down all skill cooldowns.
Step 2: Find skills with current_cooldown == 0.
Step 3: If skills are ready and random.random() < 0.6, use one.
        Otherwise do a basic attack.

60% chance to use a skill when available is intentional.
100% would feel scripted. 60% keeps fights unpredictable.

Why random selection among ready skills? The Shadow Lord has
three skills. A fixed priority would make him feel mechanical.
Random choice means the player can never fully predict the fight.

### Stun handling

If the player uses Shield Bash (Warrior skill), the monster
gets monster["stunned"] = True. monster_take_turn checks this
flag at the top and skips the turn if true, then sets it back
to False. This gives Shield Bash real tactical value.

### _basic_attack(monster, player)

Checks evade_next first. If the player is evading (Smoke Bomb),
the attack misses completely.

Then checks shield_turns. If the player has Frost Shield active,
incoming raw damage is halved before defense reduction.

Final damage: max(1, raw - player["defense"]). The max(1, ...)
ensures the player always takes at least 1 damage. Without this,
a heavily armored player could take 0 damage forever.

### _use_monster_skill(monster, player, skill)

Handles each skill type:

damage: raw = attack * multiplier, reduced by defense.
magic: same but skips defense entirely.
drain: deals damage and heals the monster for half.
shield: sets monster["shield_turns"] to increase effective defense.
heal: restores flat HP up to max_hp.

### roll_loot(monster)

Rolls random.random() against loot_chance. If it passes, picks
one random item ID from loot_table. Returns a list for
consistency (could extend to multi-drop later without changing
the interface).

### roll_gold(monster)

Returns random.randint(low, high) from the monster's gold_drop
tuple.

---

## room.py

### Purpose

Defines the dungeon layout. All rooms and their connections
form a small directed graph. Rooms are connected by direction
strings ("north", "south", etc.).

### Room graph

    entrance <-> guard_hall <-> crypt <-> boss_chamber
                     |
                dark_library

Entrance: Tutorial room. Two goblins. Has a weapon and potion.
Guard Hall: Hub room. Three connections. Skeleton and goblin.
Dark Library: Side room. Dark mage. Best magic loot.
Crypt: Pre-boss room. Stone golem and skeleton. Has elixir.
Boss Chamber: One-way deeper. Shadow Lord. No floor loot.

Why this layout? The player is forced to clear the Guard Hall
before reaching the Crypt or Library. The Library is optional
and rewards exploration with better loot. The Crypt is a
difficulty spike before the boss. Linear progression with
one meaningful detour.

### build_rooms()

Creates a fresh dungeon at the start of each game.
Deep copies each template and adds runtime state:

    cleared       False until all monsters are dead.
    loot_taken    False until the player collects floor items.
    loot_items    Actual item dicts expanded from the loot ID list.

Why expand loot IDs at build time? Rooms store monster IDs
as strings (re-fetched each fight via get_monster). But floor
loot needs to be ready as item dicts immediately so the player
can pick them up without a lookup step every time.

### describe_room(room)

Prints room name, description, exits, enemy count, and
floor loot names. Hides loot details until the player uses
the "loot" command.

### collect_room_loot(room, player)

Moves all floor items to player inventory.
Sets loot_taken to True so the room does not offer loot again.
Blocked if monsters are still present. You have to fight first.

### can_move(room, direction)

Returns the destination room ID or None.
The game loop uses this to validate movement before changing
the current room.

---

## combat.py

### Purpose

Manages the full combat loop between the player and one monster.
Returns "win", "lose", or "flee" to the caller.

### start_combat(player, monster)

The outer loop. Runs while both sides are alive.

Each iteration:
1. Print status (both HPs).
2. Player takes their turn.
3. If player chose to flee and succeeded, return "flee".
4. If monster is dead after player's turn, break.
5. Monster takes its turn.
6. Tick player cooldowns.
7. Tick player shield.
8. If player is dead, break.

After the loop:
- If player HP <= 0, return "lose".
- Otherwise, distribute rewards and return "win".

### _player_turn(player, monster)

Presents four options:
1. Attack (always available).
2. Use Skill (opens skill selection sub-menu).
3. Use Item (opens consumable sub-menu).
4. Flee (50% chance to escape).

Invalid input makes the player skip their turn. This is
intentional. Mistyping a command in combat costs you a turn,
which adds a small pressure to act deliberately.

### _player_attack(player, monster)

raw = player["attack"]
Checks monster shield_turns. If active, monster defense is
multiplied by 1.5 and the shield counter decrements.
damage = max(1, raw - monster_defense).

### _player_use_skill(player, monster)

Fetches the chosen skill by index.
Checks cooldown. If it is > 0, denies the action.
Sets current_cooldown to skill["cooldown"] on use.

Then branches by skill type:

damage: raw = attack * multiplier, minus defense.
magic: raw = attack * multiplier, no defense reduction.
stun:  deals damage, sets monster["stunned"] = True,
       prints that the monster is stunned.
evade: sets player["evade_next"] = True.
       The next incoming hit (in monster.py) will miss.
shield: sets player["shield_turns"] = duration.
        Incoming damage is halved while this is active.

### _player_use_item_in_combat

Filters inventory to only consumables.
Presents them numbered.
Player picks one by number.
Calls use_consumable logic inline (does not call player.py's
use_consumable to avoid double-removing the item).

### _distribute_rewards(player, monster)

Calls roll_gold and adds to player gold.
Calls roll_loot and appends any drops to player inventory.
Prints results.

---

## game.py

### Purpose

The outermost loop that ties everything together.
Parses player input, moves between rooms, triggers combat,
and checks win/lose conditions.

### run_game(player)

Builds the dungeon with build_rooms().
Sets starting room to "entrance".

Main loop:
1. Get current room.
2. Describe it.
3. If room has monsters and is not cleared, trigger combat.
4. If player dies in combat, call _game_over().
5. Check win condition after each combat.
6. Get player input.
7. Handle command.
8. If command is a direction, update current_room_id.

### _trigger_combat(player, room, rooms)

Iterates over the room's monster ID list.
For each ID, calls get_monster() to get a fresh copy.
Calls start_combat(player, monster).

If the player wins, removes that monster ID from room["monsters"].
If the player dies or flees, stops immediately.
If all monsters are dead, calls mark_room_cleared(room).

Why fight monsters one at a time instead of all at once?
Sequential fights let the player use items and skills between
encounters. It makes a room with two goblins feel different
from a room with one. The player has to manage resources
across multiple fights.

### _handle_command(command, player, room, rooms, current_room_id)

Parses text commands. Supported commands:

    north/south/east/west (or n/s/e/w)   Move.
    look                                  Redescribe room.
    stats                                 Show player stats.
    inventory / inv                       Show inventory.
    skills                                Show skills and cooldowns.
    loot                                  Collect floor items.
    equip <number>                        Equip item from inventory.
    use <number>                          Use consumable from inventory.
    discard <number>                      Remove item from inventory.
    map                                   Show all rooms and clear status.
    quit / exit                           End the game.

Movement commands are validated but the actual room ID change
happens back in run_game. _handle_command does not have write
access to current_room_id because Python passes primitives by
value. The loop handles the move.

### _check_win(rooms)

Iterates over all rooms. If any boss room (is_boss_room == True)
is not cleared, returns False. If all boss rooms are cleared,
returns True.

Currently there is one boss room (boss_chamber). Adding more
bosses only requires adding more rooms with is_boss_room = True
and populating them with monsters.

### _game_over() and _game_win(player)

Both print a formatted screen and call sys.exit(0).
sys.exit is used instead of returning up the call stack because
the game is a simple single-session program. There is no menu
to return to.

---

## main.py

### Why it is this short

main.py is the entry point and nothing else.
create_player() and run_game() each have full responsibility
for their own phase. main.py just sequences them.

---

## Combat Math Summary

### Player deals damage

Physical (basic attack or damage skill):
    damage = max(1, player.attack * multiplier - monster.defense)

Magic (Fireball, Shadow Wave):
    damage = player.attack * multiplier   (no defense subtracted)

### Monster deals damage to player

Physical:
    raw = monster.attack
    if player.shield_turns > 0: raw = raw * 0.5
    damage = max(1, raw - player.defense)

Magic:
    raw = monster.attack * multiplier
    if player.shield_turns > 0: raw = raw * 0.5
    player.hp -= raw   (defense not subtracted)

Drain:
    damage = max(1, attack * multiplier - player.defense)
    heal = damage // 2
    monster.hp = min(monster.hp + heal, monster.max_hp)

### Why max(1, ...) everywhere

Without the floor, a player with high defense could take 0
damage indefinitely. That removes tension. Every hit should
sting at least a little.

---

## Win and Lose Conditions

Lose: player.hp <= 0 at any point during combat.
      game.py calls _game_over() which prints a message
      and calls sys.exit(0).

Win:  All rooms where is_boss_room == True are marked cleared.
      _check_win() returns True.
      game.py calls _game_win(player) and exits.

The check happens after every combat result in run_game.
It cannot be triggered mid-fight, only between encounters.

---

## Design Decisions Summary

1. Dictionaries over classes.
   Keeps the code flat and readable. No __init__, no inheritance.
   Each module owns its data format and documents its keys.

2. Deep copy everywhere.
   Templates are constants. Runtime copies hold mutable state.
   This prevents one game session from polluting the next
   and prevents shared references between equipped items
   and inventory slots.

3. Module separation by responsibility.
   items.py knows nothing about combat.
   monster.py knows nothing about rooms.
   combat.py knows about players and monsters but not rooms.
   game.py is the only place that connects everything.
   This makes debugging straightforward. A loot bug is in
   items.py or monster.py. A navigation bug is in game.py.

4. Random AI at 60% skill usage.
   100% feels scripted. 0% is just a stat check.
   60% creates enough variance that fights feel live
   without being completely unpredictable.

5. max(1, ...) damage floor.
   Prevents stalemates. Defense should matter but never
   reach full immunity.

6. Single-session design.
   No save files. No persistence. The game runs, you finish
   or die, and it exits. This is the simplest architecture
   for a dungeon crawler at this scale.
