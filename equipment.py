from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        """
        возвращает объект оружия по имени
        """
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        """
        возвращает объект брони по имени
        """
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> List[str]:
        """
        возвращает список с названиями оружия
        """
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> List[str]:
        """
        возвращает список с названиями брони
        """
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """
        метод загружает json в переменную EquipmentData
        """
        with open("./data/equipment.json", encoding="utf-8") as equipment_file:
            data = json.load(equipment_file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)

            return equipment_schema().load(data)