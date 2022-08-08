"""
Описание класса

"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Hotel:
    """
    Описание сущности "отель"

    """
    _hotel_id: int                  # индентификатор отеля (возвращается из API-call)
    _country_id: int                # идентификатор страны
    _city_id: int                   # идентификатор города
    _country: str                   # название страны (для формирования сообщения)
    _city: str                      # название города (для формирования сообщения)
    _nights: int                    # длительность бронирования (для формирования сообщения)
    _name: str                      # название отеля
    _price_per_night_str: str       # цена за ночь (как возвращает API-call)
    _price_per_night: float         # цена за ночь
    _currency: str                  # валюта
    _distance_to_city_center: str   # расстояние до центра (как возвращает API-call)
    _km_to_city_center: float       # расстояния [км] до центра города
    _street: str                    # улица
    _full_address: str              # полный адрес
    _url: 'URL'                     # URL (ссылка на страницу отеля на сайте hotels.com)
    _cost: float                    # стоимость за указанный период
    _images: List[str] = field(default_factory=list)  # массив фото

    def __init__(
            self,
            usd: 'UserStateData',
            h_id: int,
            h_name: str,
            ppn: Optional[str] = None,
            dtcc: Optional[str] = None,
            addr: Optional[str] = None
    ) -> None:
        """
        Конструктор

        :param usd:
        :param h_id: идентификатор отеля (возвращается из API-call)
        :param h_name: название отеля
        :param ppn: цена за ночь
        :param dtcc: расстояние до центра города

        """
        from loader import countries

        self.country_id = usd.selected_country_id
        self.city_id = usd.selected_city_id
        country = countries[usd.selected_country_id]
        city = country.cities[usd.selected_city_id]
        self.nights = usd.nights
        self.country = country.nicename
        self.city = city.name
        self.hotel_id = h_id
        self.name = h_name
        self._full_address = addr

        # ppn приходит в формате '$1,000' - распарсим
        if ppn is not None:
            # убираем разделитель тысяч если есть
            tmp: str = ppn[1:]
            for symbol in ('.', ','):
                tmp: str = tmp.replace(symbol, '')
            try:
                self.price_per_night = int(tmp)
            except ValueError:
                raise
            self._currency = ppn[0]
            self.price_per_night_str = f'{self._currency}{self.price_per_night}'

        # формируем ссылку на страницу отеля
        self.url = 'https://www.hotels.com/ho{}?q-check-in={}&q-check-out={}&q-rooms=1'.format(
            h_id,
            usd.checkin_date.strftime('%Y-%m-%d'),
            usd.checkout_date.strftime('%Y-%m-%d')
        )

        # парсим расстояние до центра
        if dtcc is None:
            self._distance_to_city_center = 'не указано'
        else:
            self._distance_to_city_center = dtcc
            miles = dtcc.split()[0]
            try:
                self.km_to_city_center = float(miles) * 1.61
            except ValueError:
                raise

        # считаем полную стоимость
        self._cost = self._nights * self._price_per_night

        self._images = []

    def add_image(self, img_url: str) -> None:
        """
        Добавить картинку в массив
        (на самом деле хранит ссылки на картинки сами картинки лежат в интернете)

        :param img_url: сслыка на картинку

        """
        self._images.append(img_url)

    def clear_images(self) -> None:
        """
        Очистить массив с картинками

        """
        self._images.clear()

    def print_to_telegram(self) -> str:
        """
        Формирует сообщение для вывода информации об отеле в сообщение Telegram

        :return: res: текст сообщения

        """
        dtcc: str = ''
        if self._distance_to_city_center == 'не указано':
            dtcc = 'не указано'
        else:
            dtcc = '{:.1f} км'.format(self._km_to_city_center)

        res: str = (
                '<i>Наименование:</i> <b>{}</b>\n'
                '<i>Адрес:</i> {}\n'
                '<i>Расстояние до центра города: {}</i>\n'
                '<i>Цена за ночь:</i> {}\n'
                '<i>Полная стоимость:</i> {}{}\n'
                '{}').format(
            self._name,
            self._full_address,
            dtcc,
            self._price_per_night_str,
            self._currency, self._cost,
            self._url
        )

        return res

    @staticmethod
    def str_to_km(miles: str) -> float:
        """

        :param miles:
        :return:
        """
        miles = miles.split()[0]
        try:
            km_to_city_center = float(miles) * 1.61
        except ValueError:
            raise

        return km_to_city_center

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def hotel_id(self):
        return self._id
    @hotel_id.setter
    def hotel_id(self, val):
        self._id = val

    @property
    def country_id(self):
        return self._country_id
    @country_id.setter
    def country_id(self, val):
        self._country_id = val

    @property
    def city_id(self):
        return self._city_id
    @city_id.setter
    def city_id(self, val):
        self._city_id = val

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, val):
        self._name = val

    @property
    def price_per_night_str(self):
        return self._price_per_night_str
    @price_per_night_str.setter
    def price_per_night_str(self, val):
        self._price_per_night_str = val

    @property
    def price_per_night(self):
        return self._price_per_night
    @price_per_night.setter
    def price_per_night(self, val):
        self._price_per_night = val

    @property
    def currency(self):
        return self._currency

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, val):
        self._url = val

    @property
    def km_to_city_center(self):
        return self._km_to_city_center
    @km_to_city_center.setter
    def km_to_city_center(self, val):
        self._km_to_city_center = val

    @property
    def nights(self):
        return self._nights
    @nights.setter
    def nights(self, val):
        self._nights = val

    @property
    def cost(self):
        return self._cost

    @property
    def images(self):
        return self._images

    @property
    def full_address(self):
        return self._full_address









