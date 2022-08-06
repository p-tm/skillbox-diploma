"""
API-запросы к удалённым среверам

"""
import time

from json import loads
from json.decoder import JSONDecodeError
from requests import request, exceptions
from requests.models import Response
from typing import Any, Callable, Dict, Optional

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from config import (
    COUNTRIES_API_HEADERS, CITIES_API_HEADERS, HOTELS_API_HEADERS, LowpriceSubstates, HighpriceSubstates
)
from exceptions.fatal_error import FatalError
from exceptions.data_unavalible import DataUnavailible
from functions.console_message import console_message


class ApiCalls:
    """
    Инкапсулирует работу с удалёнными серверами через API

    """
    _countries_api_headers: Dict[str, str] = COUNTRIES_API_HEADERS
    _cities_api_headers: Dict[str, str] = CITIES_API_HEADERS
    _hotels_api_headers: Dict[str, str] = HOTELS_API_HEADERS

    def request_helper(self, func: Callable, *, retries: Optional[int] = 1) -> Callable:
        """
        Декоратор - применяется к функции request
        Обрабатывает ошибки функции request

        :param func: декорируемая функция
        :param retries: число попыток
        :return: декорированная функция
        :raise DataUnavailible: - не удалось получить данные

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
        """
        Декоратор - применяется к функции json.loads
        Обрабатывает ошибки функции json.loads

        :param func: декорируемая функция
        :return: декорированная функция

        """
        def helper(*args, **kwargs) -> Any:
            try:
                ''' тут уже знаем, что код ответа был 200, и данные точно целые и нормально декодируются '''
                ''' всё равно непонятно, что можно сделать, если данные пришли "битые" '''
                ''' просто выведем сообщение о том, что проблема при декодировании данных '''
                return func(*args, **kwargs)
            except (JSONDecodeError, TypeError, Exception) as e:
                console_message('Ошибка при декодировании данных. ' + str(e))

        return helper

    def get_countries_per_world(self) -> Dict[str, Any]:
        """
        Запрашивает полный список стран в мире

        :return: полученные данные в виде словаря (в "сыром" виде)

        """
        url = "https://country-list5.p.rapidapi.com/countrylist/"

        countries_all: Response = self.request_helper(request, retries=3)(
            "GET",
            url,
            headers=self._countries_api_headers
        )
        countries_dict: Dict[str, Any] = self.json_decode_helper(loads)(countries_all.text)['country']

        return countries_dict


    def get_cities_per_country(self, ciso: str) -> Dict[str, Any]:
        """
        Получает список городов в указанной стране

        :param ciso: ISO-обозначение страны

        :return:

        """
        url = "https://city-list.p.rapidapi.com/api/getCity/" + ciso

        cities_all: Response = self.request_helper(request, retries=3)("GET", url, headers=self._cities_api_headers)
        cities_dict: Dict[str, Any] = self.json_decode_helper(loads)(cities_all.text)['0']

        return cities_dict

    def get_city_destination_id(self, city_name: str) -> Dict[str, Any]:
        """
        Возвращает 'destination_id' по указанному городу (по строковому имени)

        :return: словарь, содержание определяется ответом API-call

        """
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"

        querystring = {"query": city_name}

        location_all: Response = self.request_helper(request, retries=3)(
            "GET",
            url,
            headers=self._hotels_api_headers,
            params=querystring
        )
        location_dict: Dict[str, Any] = self.json_decode_helper(loads)(location_all.text)

        return location_dict

    def get_hotels_per_city(self, usd: UserStateData, page: int = 1) -> Dict[str, Any]:
        """
        Получает перечень отелей в выбранном городе через API-call
        API-call может сам возвращает заданное кол-во отелей

        :param usd:
        :param page:
        :return: словарь, содержание определяется ответом API-call

        """

        from loader import countries

        # тут уже требуется указать даты

        url: 'URL' = "https://hotels4.p.rapidapi.com/properties/list"

        destination_id: int = countries[usd.selected_country_id].cities[usd.selected_city_id].dids[0]
        checkin_date = usd.checkin_date.strftime('%Y-%m-%d')
        checkout_date = usd.checkout_date.strftime('%Y-%m-%d')
        amount = usd.hotels_amount

        if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
            querystring: Dict = {
                "destinationId": destination_id,
                "pageNumber": "1",
                "pageSize": amount,
                "checkIn": checkin_date,
                "checkOut": checkout_date,
                "adults1": "1",
                "sortOrder": 'PRICE'
            }
        elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
            querystring: Dict = {
                "destinationId": destination_id,
                "pageNumber": "1",
                "pageSize": amount,
                "checkIn": checkin_date,
                "checkOut": checkout_date,
                "adults1": "1",
                "sortOrder": 'PRICE_HIGHEST_FIRST'
            }
        elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
            querystring: Dict = {
                "destinationId": destination_id,
                "pageNumber": page,
                "pageSize": "25",
                "checkIn": checkin_date,
                "checkOut": checkout_date,
                "adults1": "1",
                "sortOrder": 'DISTANCE_FROM_LANDMARK',
                "priceMin": usd.min_price,
                "priceMax": usd.max_price,
                "landmarkIds": "City center"
            }

        hotels_all: Response = self.request_helper(request, retries=3)(
            "GET",
            url,
            headers=self._hotels_api_headers,
            params=querystring
        )
        hotels_dict: Dict[str, Any] = self.json_decode_helper(loads)(hotels_all.text)

        return hotels_dict

    def get_hotel_pictures(self, hotel_id: int) -> Dict[str, Any]:
        """
        Получает фото отеля через API-call
        API-call не может получить указанное кол-во картинок, может только все

        :param hotel_id: id отеля, полученное из предыдущего запроса API-call
        :return:

        """
        url: 'URL' = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

        querystring = {"id": hotel_id}

        pictures_all: Response = self.request_helper(request, retries=3)(
            "GET",
            url,
            headers=self._hotels_api_headers,
            params=querystring
        )
        pictures_dict: Dict[str, Any] = self.json_decode_helper(loads)(pictures_all.text)

        return pictures_dict
