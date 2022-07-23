import requests
import json

from typing import *
#from PcTelBot import PcTelBot
from User import User


class ApiCalls:
    """
    Класс:
    -----


    Аттрибуты:
    ---------


    Методы:
    ------


    """
    def get_countries_per_world(self):
        """
        Функция (метод объекта):
        -----------------------

        :return:

        """
        url = "https://country-list5.p.rapidapi.com/countrylist/"

        headers = {
            "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
            "X-RapidAPI-Host": "country-list5.p.rapidapi.com"
        }

        countries_all = requests.request("GET", url, headers=headers)
        countries_dict = None

        if countries_all.status_code == 200:
            countries_dict = json.loads(countries_all.text)['country']

        return countries_dict, countries_all.status_code


    def get_cities_per_country(self, ciso: str):
        """
        Функция (метод объекта):
        -----------------------

        :return:

        """
        url = "https://city-list.p.rapidapi.com/api/getCity/" + ciso

        headers = {
            "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
            "X-RapidAPI-Host": "city-list.p.rapidapi.com"
        }

        cities_all = requests.request("GET", url, headers=headers)
        cities_dict = None

        if cities_all.status_code == 200:
            cities_dict = json.loads(cities_all.text)['0']

        return cities_dict, cities_all.status_code

    def get_city_destination_id(self, city_name: str):
        """
        Функция (метод объекта):
        -----------------------

        :return:

        """
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"

        querystring = {"query": city_name}

        headers = {
            "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        location_all = requests.request("GET", url, headers=headers, params=querystring)
        location_dict = None

        if location_all.status_code == 200:
            location_dict = json.loads(location_all.text)

        return location_dict, location_all.status_code

    def get_hotels_per_city(self, bot: 'PcTelBot',  user: User):
        """
        Функция (метод объекта):
        -----------------------
            Запрашивает перечень отелей в выбранном городе через API-call

        Примечания:
        ----------
            API-call может сам вернуть нужно кол-во отелей (??)

        :param bot: PcTelBot
            -
        :param user: User
            -
        :return: Dict
            - словарь, содержание определяется ответом API-call

        """

        # тут уже требуется указать даты

        url: 'URL' = "https://hotels4.p.rapidapi.com/properties/list"

        destination_id: int = bot.countries[user.selected_country].cities[user.selected_city].dids[0]
        # checkin_date = user.checkin_date
        # checkout_date = user.checkout_date
        checkin_date = '2022-09-01'
        checkout_date = '2022-09-05'
        amount = user.hotels_amount

        querystring: Dict = {
            "destinationId": destination_id,
            "pageNumber": "1",
            "pageSize": amount,
            "checkIn": checkin_date,
            "checkOut": checkout_date,
            "adults1": "1",
            "sortOrder": "PRICE"
        }

        headers: Dict = {
            "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        hotels_all = requests.request("GET", url, headers=headers, params=querystring)
        hotels_dict = None

        if hotels_all.status_code == 200:
            hotels_dict = json.loads(hotels_all.text)

        return hotels_dict, hotels_all.status_code

    def get_hotel_pictures(self, hotel_id: int):
        """
        Функция:
        --------
            Запрашивает фото отеля через API-call

        Примечания:
        ----------
            API-call не может получить указанное кол-во картинок, может только все

        :param hotel_id:
        :return:

        """

        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

        querystring = {"id": hotel_id}

        headers = {
            "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        pictures_all = requests.request("GET", url, headers=headers, params=querystring)
        pictures_dict = None

        if pictures_all.status_code == 200:
            pictures_dict: Dict = json.loads(pictures_all.text)

        return pictures_dict, pictures_all.status_code





