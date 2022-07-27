import os

from typing import *

from api.api_calls import ApiCalls
from classes.countries import Countries
from classes.country import Country
from exceptions.data_unavalible import DataUnavailible
from functions.cashfile import cashfile


def countries_per_world(countries: Countries) -> None:
    """
    Формирует список стран

    Список стран одинаков для всех пользователей
    Список стран считывается один раз при запуске бота, но т.к. в данной конкретной работе
    допустимое количество обращений к удалённой базе ограничено, при считывании мы
    формируем файл, и при следующем считывании проверяем наличие этого файла.
    Если файл существует - читаем не из удалённой базы, а из файла


    :return: None
    :raises: DataUnavailible

    """
    f_name: str = 'countries_raw.txt'
    f_name = cashfile(f_name)

    if not os.path.exists(f_name):

        try:
            countries_raw: List[Dict] = ApiCalls().get_countries_per_world()
        except DataUnavailible:
            raise

        with open(f_name, 'w') as f_con:
            f_con.write(str(countries_raw))
    else:
        with open(f_name, 'r') as f_con:
            countries_raw = eval(f_con.read())

    # TODO переделать - если файл существует, то и структуру обновлять не надо
    # TODO получается, что когда бот запускается это один раз должно произойти
    # TODO и в остальных местах тоже

    def add_country(item):
        countries[item['id']] = Country(item['id'], item['iso'], item['countryname'], item['nicename'])

    # for item in countries_raw:
    #     self.countries[item['id']] = Country(item['id'], item['iso'], item['countryname'], item['nicename'])

    [add_country(item) for item in countries_raw]
