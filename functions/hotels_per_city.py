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
from functions.get_raw_data import get_raw_data
from config import GET_HOTELS_FROM_SERVER
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
        usd=usd
    )

    hotels_list = hotels_raw['data']['body']['searchResults']['results']

    data: Dict[int, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        usd = data['usd']

    usd.hotels.clear()

    def add_hotel(item: Dict):
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
