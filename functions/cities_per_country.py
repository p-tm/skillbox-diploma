import os

from typing import *

from api.api_calls import ApiCalls
from classes.city import City
from exceptions.data_unavalible import DataUnavailible

from functions.cashfile import cashfile
from functions.get_raw_data import get_raw_data
from loader import countries

def cities_per_country(cid: int) -> None:
    """
    Формирует спискок городов для выбранной страны

    В идеале, нужно сформировать список всех стран и городов по странам один раз при запуске бота.
    Но, т.к. в данной конкретной работе....

    :param cid: int - id страны

    """
    country = countries[cid]
    f_name = 'cities_raw_' + country.iso + '.txt'

    cities_raw: Dict[str, Any] = get_raw_data(
        force=False,
        fname=f_name,
        func=ApiCalls().get_cities_per_country,
        ciso=country.iso
    )

    def add_city(item):
        country.cities[item['id']] = City(item['id'], item['country'], item['name'], item['population'])

    [add_city(item) for item in cities_raw if item['population'] >= 10000]