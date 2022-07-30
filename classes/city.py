from dataclasses import dataclass
from typing import *


@dataclass
class City:
    """
    Описание сущности "город"

    """
    def __init__(self, id: int, ciso: str, name: str, population: int) -> None:
        """
        Конструктор

        :return: None

        """
        self._id: int = id
        self._country_iso: str = ciso
        self._name: str = name
        self._population: int = population
        self._dids: List[int] = []  # это список destination_id которые выдаёт hotels.com.api

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def dids(self):
        return self._dids
