"""
Описание функции

"""
import os

from telebot import telebot
from typing import Any, Dict, List, Optional, Union

from api.api_calls import ApiCalls
from classes.city import City
from classes.country import Country
from classes.hotel import Hotel
from classes.user_state import UserState
from classes.user_state_data import UserStateData
from exceptions.data_unavalible import DataUnavailible
from functions.console_message import console_message
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

    city.dids.clear()
    usd.hotels.clear()

    f_name: str = 'city_did_raw_' + country.iso + '_' + city.name + '.txt'

    locations_raw: Dict[str, Any] = get_raw_data(
        force=False,
        fname=f_name,
        func=ApiCalls().get_city_destination_id,
        country_name=country.nicename,
        city_name=city.name
    )

    # suggestions: Union[int, Dict] = locations_raw.get('suggestions', 0)
    # if suggestions == 0:
    #     raise DataUnavailible('Ошибка в структуре данных при получении перечня отелей')
    # group: Dict = suggestions[0]
    # locations_list: Union[int, List] = group.get('entities', 0)
    # if locations_list == 0:
    #     raise DataUnavailible('Ошибка в структуре данных при получении перечня отелей')

    try:
        locations_list: List[Dict[str, str]] = locations_raw['suggestions'][0]['entities'] # "0" is for CITY_GROUP
    except Exception as e:
        console_message(str(e))
        raise DataUnavailible

    if not locations_list:
        console_message('Получен пустой список destination_id.')
        return

    # item: Dict[str, int]
    # for item in locations_list:
    #     did: int = item.get('destinationId', 0)
    #     if did == 0:
    #         raise DataUnavailible('Ошибка в структуре данных при получении перечня отелей')
    #     city.add_did(did)
    try:
        [city.add_did(item['destinationId']) for item in locations_list]
    except Exception as e:
        console_message(str(e))
        raise DataUnavailible

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

    try:
        hotels_list = hotels_raw['data']['body']['searchResults']['results']
    except Exception as e:
        console_message(str(e))
        raise DataUnavailible
    # data: Union[int, Dict] = hotels_raw.get('data', 0)
    # if data == 0:
    #     console_message('Ошибка в структуре данных при получении перечня отелей')
    #     raise DataUnavailible('Ошибка в структуре данных при получении перечня отелей')
    # body: Union[int, Dict] = data.get('body', 0)
    # if body == 0:
    #     console_message('Ошибка в структуре данных при получении перечня отелей')
    #     raise DataUnavailible('Ошибка в структуре данных при получении перечня отелей')
    # search_results: Union[int, Dict] = body.get('searchResults', 0)
    # if search_results == 0:
    #     console_message('Ошибка в структуре данных при получении перечня отелей')
    #     raise DataUnavailible('Ошибка в структуре данных при получении перечня отелей')
    # hotels_list: Union[int, List] = search_results.get('results', 0)
    # if hotels_list == 0:
    #     console_message('Ошибка в структуре данных при получении перечня отелей')
    #     raise DataUnavailible('Ошибка в структуре данных при получении перечня отелей')

    if not hotels_list:
        console_message('Получен пустой список отелей.')
        return

    def dist_to_city_center(item: Dict) -> Optional[str]:
        for i in item['landmarks']:
            if i['label'] == 'City center':
                return i['distance']
        return None

    # если bestdeal то нужно вручную отобрать отели, которые находятся
    # в заданном диапазоне расстояний
    # в остальных случаях сразу получаем требуемое кол-во отелей
    hotels_list_filtered: List[Dict] = []
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

            try:
                photos_list: List[str] = photos_raw['hotelImages']
            except Exception as e:
                console_message(str(e))
                raise DataUnavailible

            # photos_list: Union[int, List] = photos_raw.get('hotelImages', 0)
            #
            # if photos_list == 0:
            #     console_message('Ошибка в структуре данных при получении перечня отелей')
            #     raise DataUnavailible('Ошибка в структуре данных при получении перечня отелей')

            item.clear_images()

            def add_image(rec):
                image_url_template = rec['baseUrl']
                image_url = image_url_template.replace('{size}', 'z')
                item.add_image(image_url)

            [add_image(rec) for i, rec in enumerate(photos_list) if i < usd.photos_amount]
