"""
Описание функции

"""
import os

from typing import Any, Dict

from api.api_calls import ApiCalls
from classes.countries import Countries
from classes.country import Country
from exceptions.data_unavalible import DataUnavailible
from functions.cashfile import cashfile
from functions.get_raw_data import get_raw_data


def countries_per_world(countries: Countries) -> None:
    """
    Формирует список стран

    Список стран одинаков для всех пользователей
    Список стран считывается один раз при запуске бота, но т.к. в данной конкретной работе
    допустимое количество обращений к удалённой базе ограничено, при считывании мы
    формируем файл, и при следующем считывании проверяем наличие этого файла.
    Если файл существует - читаем не из удалённой базы, а из файла

    :param countries: массив записей о странах (внешний mutable)
    :raises: DataUnavailible

    """
    f_name: str = 'countries_raw.txt'

    countries_raw: Dict[str, Any] = get_raw_data(
        force=False,
        fname=f_name,
        func=ApiCalls().get_countries_per_world
    )

    def add_country(item):
        countries[item['id']] = Country(item['id'], item['iso'], item['countryname'], item['nicename'])

    [add_country(item) for item in countries_raw]
