"""
Описание класса

"""
from dataclasses import dataclass
from dataclasses import field
from typing import List


@dataclass
class City:
    """
    Описание сущности "город"

    """
    _city_id: int           # id города (выдаёт hotels.com.api)
    _country_iso: str       # iso-код страны
    _name: str              # название города
    _population: int        # население
    _dids: List[int] = field(default_factory=list)   # это список destination_id которые выдаёт hotels.com.api

    def __init__(self, c_id: int, ciso: str, name: str, population: int) -> None:
        """
        Конструктор

        :param c_id: id города
        :param ciso: iso-код страны
        :param name: название города
        :param population: население

        """
        self.city_id = c_id
        self.country_iso = ciso
        self.name = name
        self.population = population
        self._dids = []

    def add_did(self, did: int) -> None:
        """
        Добавить destination_id в список

        :param did: destination_id - выдаёт hotels.com.api

        """
        self._dids.append(did)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def city_id(self):
        return self._id
    @city_id.setter
    def city_id(self, val):
        self._id = val

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, val):
        self._name = val

    @property
    def population(self):
        return self._population
    @population.setter
    def population(self, val):
        if val >= 1000:
            self._population = val
        else:
            raise ValueError('Население города не может быть менее 1000 чел')

    @property
    def dids(self):
        return self._dids

