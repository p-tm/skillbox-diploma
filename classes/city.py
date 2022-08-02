from dataclasses import dataclass
from dataclasses import field
from typing import *


@dataclass
class City:
    """
    Описание сущности "город"

    """
    _city_id: int
    _country_iso: str
    _name: str
    _population: int
    _dids: List[int] = field(default_factory=list)

    def __init__(self, c_id: int, ciso: str, name: str, population: int) -> None:
        """
        Конструктор

        """
        self.city_id = c_id             # id города (выдаёт hotels.com.api)
        self.country_iso = ciso         # iso-код страны
        self.name = name                # название города
        self.population = population    # население
        self._dids = []                 # это список destination_id которые выдаёт hotels.com.api

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

