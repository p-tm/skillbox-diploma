import time

from json import loads
from json.decoder import JSONDecodeError

from requests import request, exceptions
from requests.models import Response

from typing import *

from config import COUNTRIES_API_HEADERS, CITIES_API_HEADERS

from exceptions.fatal_error import FatalError
from exceptions.data_unavalible import DataUnavailible

from functions.console_message import console_message


class ApiCalls:
    """
    Инкапсулирует работу с удалёнными серверами через API

    """
    _countries_api_headers = COUNTRIES_API_HEADERS
    _cities_api_headers = CITIES_API_HEADERS

    def request_helper(self, func: Callable, *, retries: Optional[int] = 1) -> Callable:
        """
        Декоратор - применяется к функции request
        Обрабатывает ошибки функции request

        :param func: декорируемая функция
        :param retries: число попыток
        :return: Callable
        :raise: DataUnavailible - не удалось получить данные

        """
        def helper(*args, **kwargs) -> Response:
            _tries_counter = 1
            while True:
                try:
                    resp: Response = func(*args, **kwargs)
                    break
                except exceptions.ConnectionError:
                    if _tries_counter == retries:
                        raise DataUnavailible('Нет связи с сервером данных')
                    console_message('Список стран - нет связи с сервером данных. Следующая попытка...')
                    time.sleep(3)
                    _tries_counter += 1
                except Exception as e:
                    console_message(str(e))
                    raise DataUnavailible
            ''' считаем, что если код ответа 200, то данные точно целые и нормально потом декодируются '''
            ''' всё равно непонятно, что можно сделать, если данные пришли "битые" '''
            if resp.status_code != 200:
                raise DataUnavailible('Код ответа от сервера: {}'.format(resp.status_code))
            return resp

        return helper


    def json_decode_helper(self, func: Callable) -> Callable:

        def helper(*args, **kwargs) -> Any:
            try:
                ''' тут уже знаем, что код ответа был 200, и данные точно целые и нормально декодируются '''
                ''' всё равно непонятно, что можно сделать, если данные пришли "битые" '''
                ''' просто выведем сообщение о том, что проблема при декодировании данных '''
                return func(*args, **kwargs)
            except (JSONDecodeError, TypeError, Exception) as e:
                console_message('Ошибка при декодировании данных. ' + str(e))

        return helper

    def get_countries_per_world(self) -> Dict:
        """
        Запрашивает полный список стран в мире

        :return: Dict - полученные данные в виде словаря (в "сыром" виде)

        """
        url = "https://country-list5.p.rapidapi.com/countrylist/"

        countries_all: Response = self.request_helper(request, retries=3)("GET", url, headers=self._countries_api_headers)
        countries_dict: Dict = self.json_decode_helper(loads)(countries_all.text)['country']

        return countries_dict


    def get_cities_per_country(self, ciso: str) -> Dict:
        """
        Получает список городов в указанной стране

        :param ciso: ISO-обозначение страны

        :return:

        """
        url = "https://city-list.p.rapidapi.com/api/getCity/" + ciso

        # headers = {
        #     "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
        #     "X-RapidAPI-Host": "city-list.p.rapidapi.com"
        # }

        cities_all: Response = self.request_helper(request, retries=3)("GET", url, headers=self._cities_api_headers)
        cities_dict: Dict = self.json_decode_helper(loads)(cities_all.text)['0']

        return cities_dict

        # cities_dict = None
        #
        # if cities_all.status_code == 200:
        #     cities_dict = json.loads(cities_all.text)['0']
        #
        # return cities_dict, cities_all.status_code

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

    def get_hotels_per_city(self, bot: 'telebot.TeleBot',  user: Dict):
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





