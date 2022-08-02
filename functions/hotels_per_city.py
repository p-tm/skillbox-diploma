import os

from telebot import telebot
from typing import *

from api.api_calls import ApiCalls
from classes.city import City
from classes.country import Country
from classes.hotel import Hotel
from classes.user_state_data import UserStateData
from exceptions.data_unavalible import DataUnavailible
from functions.cashfile import cashfile
from loader import bot, countries



def hotels_per_city(message: telebot.types.Message) -> None:
    """
    Формирует список отелей по заданным параметрам


    :param message: предыдущее сообщение в чате Telegram

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        usd: UserStateData = data['usd']

    country: Country = countries[usd.selected_country_id]
    city: City = country.cities[usd.selected_city_id]

    f_name: str = 'city_did_raw_' + country.iso + '_' + city.name + '.txt'
    f_name: str = cashfile(f_name)

    if not os.path.exists(f_name):

        try:
            locations_raw: Dict = ApiCalls().get_city_destination_id(city.name)
        except DataUnavailible:
            raise

        f_did: Iterable[str]
        with open(f_name, 'w', errors='replace') as f_did:
            f_did.write(str(locations_raw))
    else:
        f_did: Iterable[str]
        with open(f_name, 'r', errors='replace') as f_did:
            locations_raw: Dict = eval(f_did.read())

    locations_list: List[Dict[str, str]] = locations_raw['suggestions'][0]['entities'] # "0" is for CITY_GROUP

    # def add_destination_id(item: Dict[str, int]) -> None:
    #     """
    #     Добавляем destination_id в список
    #
    #     :param item: запись в словаре
    #     """
    #     city.add_did(item['destinationId'])

    #[add_destination_id(item) for item in locations_list]
    item: Dict[str, int]
    [city.add_did(item['destinationId']) for item in locations_list]

    # теперь собственно для каждого отеля надо запросить детали
    # чтобы запросить детали уже нужны вроде даты

    # тут надо каждый раз честно запрашивать, потому что
    # перечень возвращаемых отелей разный для разных юзеров
    # и даже для разных запросов одного юзера

    f_name = 'hotels_raw_' + country.iso + '_' + city.name + '.txt'
    f_name = cashfile(f_name)

    if not os.path.exists(f_name):

        try:
            hotels_raw: Dict = ApiCalls().get_hotels_per_city(usd)
        except DataUnavailible:
            raise

        with open(f_name, 'w', errors='replace') as f_hot:
            f_hot.write(str(hotels_raw))
    else:
        with open(f_name, 'r', errors='replace') as f_hot:
            hotels_raw = eval(f_hot.read())

    hotels_list = hotels_raw['data']['body']['searchResults']['results']

    data: Dict[int, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        usd = data['usd']

    usd.hotels.clear()

    def add_hotel(item):
        hotel = Hotel(
            usd=usd,
            h_id=item['id'],
            h_name=item['name'],
            ppn=item['ratePlan']['price']['current'],
            dtcc=item['landmarks'][0]['distance'],
            addr=item['address']['streetAddress']
        )

        hotel.country = country.nicename
        hotel.city = city.name

        usd.hotels[item['id']] = hotel

    [add_hotel(item) for item in hotels_list]

    # проверим, нужно ли запрашивать фото
    if usd.photo_required:

        item: Hotel
        for item in usd.hotels.values():
            # Фото можно на запрашивать а взять из файла, если есть,
            # потому что все юзеры, если запрашивают фото отеля,
            # то получают одно и то же

            f_name: str = 'photos_raw_' + country.iso + '_' + city.name + '_' + str(item.hotel_id) + '.txt'
            f_name: str = cashfile(f_name)

            if not os.path.exists(f_name):

                try:
                    photos_raw: Dict = ApiCalls().get_hotel_pictures(item.hotel_id)
                except DataUnavailible:
                    raise

                f_pht: Iterable[str]
                with open(f_name, 'w', errors='replace') as f_pht:
                    f_pht.write(str(photos_raw))
            else:
                f_pht: Iterable[str]
                with open(f_name, 'r', errors='replace') as f_pht:
                    photos_raw: Dict = eval(f_pht.read())

            photos_list: List[str] = photos_raw['hotelImages']

            item.clear_images()

            def add_image(rec):
                image_url_template = rec['baseUrl']
                image_url = image_url_template.replace('{size}', 'z')
                item.add_image(image_url)

            [add_image(rec) for i, rec in enumerate(photos_list) if i < usd.photos_amount]
