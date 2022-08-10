"""
Описание функции

"""
import os

from typing import Any, Dict, Union

from api.api_calls import ApiCalls
from classes.city import City
from exceptions.data_unavalible import DataUnavailible

from functions.cashfile import cashfile
from functions.console_message import console_message
from functions.get_raw_data import get_raw_data
from loader import countries

def cities_per_country(cid: int) -> None:
    """
    Формирует спискок городов для выбранной страны

    В идеале, нужно сформировать список всех стран и городов по странам один раз при запуске бота.
    Но, т.к. в данной конкретной работе имеем лимитированное количество запросов ....

    :param cid: id страны

    """
    country = countries[cid]
    f_name = 'cities_raw_' + country.iso + '.txt'

    cities_raw: Dict[str, Any] = get_raw_data(
        force=False,
        fname=f_name,
        func=ApiCalls().get_cities_per_country,
        ciso=country.iso
    )

    def add_city(item: Dict) -> None:
        """
        Добавляет объект "город" в словарь

        :param item:

        """
        # id: int = item.get('id', 0)
        # cntr: Union[int, str] = item.get('country', 0)
        # name: Union[int, str] = item.get('name', 0)
        # population: int = item.get('population', -1)
        # if id == 0 or cntr == 0 or name == 0 or population == -1:
        #     raise DataUnavailible('Ошибка в структуре данных при получении перечня городов')

        country.cities[item['id']] = City(item['id'], item['country'], item['name'], item['population'])
        # country.cities[item['id']] = City(id, cntr, name, population)

    try:
        [add_city(item) for item in cities_raw if item['population'] >= 10000]
        # [add_city(item) for item in cities_raw if item.get('population', -1) >= 10000]
    except DataUnavailible as e:
        console_message(str(e))
        raise
