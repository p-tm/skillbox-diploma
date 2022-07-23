from typing import *

class Hotel:
    """
    Класс:
    -----
    Описание сущности "Отель"


    Аттрибуты:
    ---------



    Методы:
    ------

    """
    def __init__(self, id, country_id, city_id, h_name, ppn: str = None, dtcc: str = None):
        """
        Функция (метод объекта):
        -----------------------
        Конструктор

        :param id: int
            - индентификатор отеля (возвращается из API-call)
        :param country_id: int
            - идентификатор страны (возвращается из API-call)
        :param city_id: int
            - идентификатор города (возвращается из API-call)
        :param h_name: str
            - название отеля
        :param ppn: str
            - цена за ночь (price per night)
        :param dtcc: str
            - расстояние до центра города (distance to city center)

        """
        self._id: int = id
        self._country_id: int = country_id
        self._city_id: int = city_id
        self._country: str = ''
        self._city: str = ''
        self._name: str = h_name
        self._price_per_night_str: str = ppn # как возвращает API-call
        self._price_per_night: float = 0.0
        self._currency: str = ''
        self._distance_to_city_center_str: str = dtcc # как возвращает API-call
        self._street: str = ''
        self._full_address: str = ''
        #self._url = 'https://www.hotels.com/ho' + str(id) + '?q-check-in=2022-07-24&q-check-out=2022-07-25&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'
        # TODO put actual dates in
        self._url = 'https://www.hotels.com/ho' + str(id) + '?q-check-in=2022-07-24&q-check-out=2022-07-25&q-rooms=1'
        self._images: List['image URL'] = []

        # ppn приходит в формате '$100' - распарсим
        if ppn is not None:
            try:
                self._price_per_night = int(ppn[1:])
            except ValueError:
                raise
            self._currency = ppn[0]


    def print_to_telegram(self) -> str:
        """
        Формирует сообщение для вывода информации об отеле в сообщение Telegram

        :return: res: str
            - текст сообщения

        """
        res: str = '<i>Наименование:</i> <b>{}</b>\n' \
              '<i>Адрес:</i> {}\n' \
              '<i>Цена за ночь:</i> {}\n' \
                   '{}'.format(
            self._name,
            self._country,
            self._price_per_night_str,
            self._url
        )

        return res

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def id(self):
        return self._id

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country = country

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    @property
    def images(self):
        return self._images

"""
https://www.hotels.com/ho181280/crowne-plaza-nottingham-nottingham-united-kingdom/
https://www.hotels.com/ho149150/crowne-plaza-nottingham-nottingham-united-kingdom/
"""