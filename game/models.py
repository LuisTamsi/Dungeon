from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Item:
    name: str
    description: str
    item_type: str


@dataclass
class Weapon(Item):
    attack_bonus: int


@dataclass
class Armor(Item):
    defense_bonus: int


@dataclass
class Potion(Item):
    heal_amount: int
    cost: int


@dataclass
class Skill:
    name: str
    description: str
    effect_type: str  # "damage" or "heal"
    effect_value: int
    mana_cost: int


@dataclass
class Player:
    name: str
    class_name: str
    hp: int
    max_hp: int
    mana: int
    max_mana: int
    attack: int
    defense: int
    gold: int
    inventory: List[Item] = field(default_factory=list)
    skills: List[Skill] = field(default_factory=list)
    weapon: Optional[Weapon] = None
    armor: Optional[Armor] = None

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        self.hp = max(0, self.hp - amount)
        return amount

    def heal(self, amount: int) -> int:
        actual = min(self.max_hp - self.hp, amount)
        self.hp += actual
        return actual

    def restore_mana(self, amount: int) -> int:
        actual = min(self.max_mana - self.mana, amount)
        self.mana += actual
        return actual

    def spend_mana(self, amount: int) -> bool:
        if self.mana < amount:
            return False
        self.mana -= amount
        return True

    def total_attack(self) -> int:
        return self.attack + (self.weapon.attack_bonus if self.weapon else 0)

    def total_defense(self) -> int:
        return self.defense + (self.armor.defense_bonus if self.armor else 0)

    def add_item(self, item: Item) -> None:
        self.inventory.append(item)

    def remove_item(self, item: Item) -> None:
        self.inventory.remove(item)


@dataclass
class Monster:
    name: str
    description: str
    hp: int
    attack: int
    weapon_name: str
    weapon_bonus: int
    skills: List[Skill]
    loot_table: List[Item]
    gold_drop: int
    is_boss: bool = False

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        self.hp = max(0, self.hp - amount)
        return amount

    def total_attack(self) -> int:
        return self.attack + self.weapon_bonus


@dataclass
class Room:
    name: str
    description: str
    exits: dict
    tier: str  # "easy", "intermediate", "boss"
    spawn_count: int
    has_shop: bool = False
    monsters: List[Monster] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    spawned: bool = False
