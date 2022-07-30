from dataclasses import dataclass

from classes.cities import Cities

@dataclass
class Country:
    """
    Описание сущности "Страна"

    """
    # !!! сохраняем id для страны и для города
    # потому что потом по id будем связывать их с кнопками на экране

    def __init__(self, id: int, iso: str, countryname: str, nicename: str):
        """
        Конструктор

        :param id: id страны
        :param iso:
        :param countryname:
        :param nicename:
        :return: None

        """
        self._id = id
        self._iso = iso
        self._countryname = countryname
        self._nicename = nicename
        self._cities = Cities()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def id(self):
        return self._id

    @property
    def iso(self):
        return self._iso

    @property
    def nicename(self):
        return self._nicename

    @property
    def cities(self):
        return self._cities
