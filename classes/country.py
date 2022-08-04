"""
Описание класса

"""
from dataclasses import dataclass

from classes.cities import Cities

@dataclass
class Country:
    """
    Описание сущности "Страна"

    """
    # !!! сохраняем id для страны и для города
    # потому что потом по id будем связывать их с кнопками на экране

    _country_id: int    # иденитфикатор страны
    _iso: str           # iso-код
    #_countryname: str   # название
    _nicename: str      # название
    _cities: Cities     # массив городов


    def __init__(self, c_id: int, iso: str, countryname: str, nicename: str):
        """
        Конструктор

        :param id: id страны
        :param iso:
        :param countryname:
        :param nicename:
        :return: None

        """
        self.country_id = c_id
        self.iso = iso
        #self._countryname = countryname
        self.nicename = nicename
        self._cities = Cities()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def country_id(self):
        return self._country_id
    @country_id.setter
    def country_id(self, val):
        self._country_id = val

    @property
    def iso(self):
        return self._iso
    @iso.setter
    def iso(self, val):
        self._iso = val

    @property
    def nicename(self):
        return self._nicename
    @nicename.setter
    def nicename(self, val):
        self._nicename = val

    @property
    def cities(self):
        return self._cities
