"""
Описание функции

"""
import os

from telebot import telebot
from typing import Any, Dict, List, Optional

from api.api_calls import ApiCalls
from classes.city import City
from classes.country import Country
from classes.hotel import Hotel
from classes.user_state import UserState
from classes.user_state_data import UserStateData
from functions.get_raw_data import get_raw_data
from functions.get_usd import get_usd
from config import GET_HOTELS_FROM_SERVER
from loader import bot, countries



def hotels_per_city(message: telebot.types.Message) -> None:
    """
    Формирует список отелей по заданным параметрам


    :param message: предыдущее сообщение в чате Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    country: Country = countries[usd.selected_country_id]
    city: City = country.cities[usd.selected_city_id]

    f_name: str = 'city_did_raw_' + country.iso + '_' + city.name + '.txt'

    locations_raw: Dict[str, Any] = get_raw_data(
        force=False,
        fname=f_name,
        func=ApiCalls().get_city_destination_id,
        city_name=city.name
    )

    locations_list: List[Dict[str, str]] = locations_raw['suggestions'][0]['entities'] # "0" is for CITY_GROUP

    item: Dict[str, int]
    [city.add_did(item['destinationId']) for item in locations_list]

    # теперь собственно для каждого отеля надо запросить детали
    # тут надо каждый раз честно запрашивать, потому что
    # перечень возвращаемых отелей разный для разных юзеров
    # и даже для разных запросов одного юзера

    f_name = 'hotels_raw_' + country.iso + '_' + city.name + '.txt'

    hotels_raw: Dict[str, Any] = get_raw_data(
        force=GET_HOTELS_FROM_SERVER,
        fname=f_name,
        func=ApiCalls().get_hotels_per_city,
        usd=usd,
        page=1
    )

    hotels_list = hotels_raw['data']['body']['searchResults']['results']

    usd.hotels.clear()

    def dist_to_city_center(item: Dict) -> Optional[str]:
        for i in item['landmarks']:
            if i['label'] == 'City center':
                return i['distance']
        return None

    # если bestdeal то нужно вручную отобрать отели, которые находятся
    # в заданном диапазоне расстояний
    # в остальных случаях сразу получаем требуемое кол-во отелей
    hotels_list_filtered: List = []
    if usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        # бёрём только те отели, у которых есть поле 'City center'
        # и если оно есть то укладывается в заданный диапазон
        counter = 0
        for item in hotels_list:
            dtcc: str = dist_to_city_center(item)
            if dtcc is not None:
                if usd.min_distance <= Hotel.str_to_km(dtcc) <= usd.max_distance:
                    hotels_list_filtered.append(item)
                    counter += 1
            if counter == usd.hotels_amount:
                break

    else:
        hotels_list_filtered = hotels_list


    def add_hotel(item: Dict):
        hotel = Hotel(
            usd=usd,
            h_id=item['id'],
            h_name=item['name'],
            ppn=item['ratePlan']['price']['current'],
            #dtcc=item['landmarks'][0]['distance'],
            dtcc=dist_to_city_center(item),
            addr=item['address'].get('streetAddress', 'не указан')
        )

        hotel.country = country.nicename
        hotel.city = city.name

        usd.hotels[item['id']] = hotel

    [add_hotel(item) for item in hotels_list_filtered]

    # проверим, нужно ли запрашивать фото
    if usd.photo_required:

        item: Hotel
        for item in usd.hotels.values():
            # Фото можно на запрашивать а взять из файла, если есть,
            # потому что все юзеры, если запрашивают фото отеля,
            # то получают одно и то же

            f_name: str = 'photos_raw_' + country.iso + '_' + city.name + '_' + str(item.hotel_id) + '.txt'

            photos_raw: Dict[str, Any] = get_raw_data(
                force=False,
                fname=f_name,
                func=ApiCalls().get_hotel_pictures,
                hotel_id=item.hotel_id
            )

            photos_list: List[str] = photos_raw['hotelImages']

            item.clear_images()

            def add_image(rec):
                image_url_template = rec['baseUrl']
                image_url = image_url_template.replace('{size}', 'z')
                item.add_image(image_url)

            [add_image(rec) for i, rec in enumerate(photos_list) if i < usd.photos_amount]
