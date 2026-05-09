import random
from typing import List

from models import Monster, Player, Potion, Skill


def choose_skill(skills: List[Skill]) -> Skill:
    print("Choose a skill:")
    for index, skill in enumerate(skills, start=1):
        print(f"  {index}. {skill.name} (cost {skill.mana_cost}) - {skill.description}")
    while True:
        choice = input("Skill number: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(skills):
                return skills[index]
        print("Invalid choice. Try again.")


def apply_skill(attacker_name: str, skill: Skill, player: Player, monster: Monster, target: str) -> None:
    if skill.effect_type == "damage":
        if target == "monster":
            damage = max(1, skill.effect_value)
            monster.take_damage(damage)
            print(f"{attacker_name} uses {skill.name} for {damage} damage!")
        else:
            damage = max(1, skill.effect_value - player.total_defense())
            player.take_damage(damage)
            print(f"{attacker_name} uses {skill.name} for {damage} damage!")
    else:
        if target == "monster":
            monster.hp += skill.effect_value
            print(f"{attacker_name} uses {skill.name} and heals {skill.effect_value} HP!")
        else:
            healed = player.heal(skill.effect_value)
            print(f"{attacker_name} uses {skill.name} and heals {healed} HP!")


def player_attack(player: Player, monster: Monster) -> None:
    damage = max(1, player.total_attack() - 1)
    monster.take_damage(damage)
    print(f"You strike the {monster.name} for {damage} damage.")


def monster_attack(player: Player, monster: Monster) -> None:
    damage = max(1, monster.total_attack() - player.total_defense())
    player.take_damage(damage)
    print(f"{monster.name} hits you for {damage} damage.")


def use_potion_in_combat(player: Player) -> bool:
    potion = next((item for item in player.inventory if isinstance(item, Potion)), None)
    if not potion:
        print("You have no potions.")
        return False
    healed = player.heal(potion.heal_amount)
    player.remove_item(potion)
    print(f"You use a potion and heal {healed} HP.")
    return True


def combat_loop(player: Player, monster: Monster) -> bool:
    print(f"\nCombat begins with {monster.name}!")
    while player.is_alive() and monster.is_alive():
        print(
            f"HP {player.hp}/{player.max_hp} | Mana {player.mana}/{player.max_mana} "
            f"| {monster.name} HP {monster.hp}"
        )
        action = input("Action (attack/skill/potion/run): ").strip().lower()

        if action == "attack":
            player_attack(player, monster)
        elif action == "skill":
            if not player.skills:
                print("You have no skills.")
            else:
                skill = choose_skill(player.skills)
                if player.spend_mana(skill.mana_cost):
                    apply_skill(player.name, skill, player, monster, "monster")
                else:
                    print("Not enough mana.")
                    continue
        elif action == "potion":
            if not use_potion_in_combat(player):
                continue
        elif action == "run":
            print("You retreat from combat!")
            return False
        else:
            print("Unknown action.")
            continue

        player.restore_mana(1)

        if monster.is_alive():
            if monster.skills and random.random() < 0.4:
                skill = random.choice(monster.skills)
                apply_skill(monster.name, skill, player, monster, "player")
            else:
                monster_attack(player, monster)

    return player.is_alive()
