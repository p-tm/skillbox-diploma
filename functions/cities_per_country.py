import os

from typing import *

from api.api_calls import ApiCalls
from classes.city import City
from exceptions.data_unavalible import DataUnavailible

from functions.cashfile import cashfile
from loader import countries

def cities_per_country(cid: int):
    """
    Формирует спискок городов для выбранной страны

    В идеале, нужно сформировать список всех стран и городов по странам один раз при запуске бота.
    Но, т.к. в данной конкретной работе....

    :param cid: int - id страны
    :return:

    """
    country = countries[cid]
    f_name = 'cities_raw_' + country.iso + '.txt'
    f_name = cashfile(f_name)

    if not os.path.exists(f_name):

        try:
            cities_raw: List[Dict] = ApiCalls().get_cities_per_country(country.iso)
        except DataUnavailible:
            raise

        with open(f_name, 'w', errors='replace') as f_cit:
            f_cit.write(str(cities_raw))
    else:
        with open(f_name, 'r', errors='replace') as f_cit:
            cities_raw = eval(f_cit.read())

    def add_city(item):
        country.cities[item['id']] = City(item['id'], item['country'], item['name'], item['population'])

    [add_city(item) for item in cities_raw if item['population'] >= 10000]