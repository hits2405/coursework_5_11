from dataclasses import dataclass
from typing import List, Union
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: Union[float, int]
    stamina_per_turn: Union[float, int]


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: Union[float, int]
    max_damage: Union[float, int]
    stamina_per_hit: Union[float, int]

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    # TODO содержит 2 списка - с оружием и с броней
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Union[Weapon, None]:
        # TODO возвращает объект оружия по имени
        for weapon in list(self.equipment.weapons):
            if weapon.name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name) -> Union[Armor, None]:
        # TODO возвращает объект брони по имени
        for armor in list(self.equipment.armors):
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> list:
        # TODO возвращаем список с оружием
        return [weapon.name for weapon in list(self.equipment.weapons)]

    def get_armors_names(self) -> list:
        # TODO возвращаем список с броней
        return [armor.name for armor in list(self.equipment.armors)]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:

        equipment_file = open('data/equipment.json', encoding='utf-8')
        data = json.load(equipment_file)
        equipment_file.close()
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
