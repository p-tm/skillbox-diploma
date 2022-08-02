#import datetime

from dataclasses import dataclass

from classes.hotel import Hotel
from classes.hotels import Hotels
from datetime import datetime, timedelta
from telebot import telebot
from typing import *


@dataclass
class UserStateData:
    """
    Хранение данных (состояния) конкретного пользователя в конкретном чате

    """
    def __init__(self):
        """
        Конструктор

        """
        self._substate: int = None                  # текущее состояние внутри основного
        self._selected_country_id: int = None       # id выбранной страны (берётся из удалённого запроса)
        self._selected_city_id: int = None          # id выбранного города (берётся из удалённого запроса)
        self._hotels_amount: int = None             # количество отелей
        self._photo_required: bool = None           # требуется ли фотография
        self._photos_amount: int = None             # количество фото
        self._checkin_date: datetime = None
        self._checkout_date: datetime = None
        self._nights: int = None
        self._keyboard_maker: Dict = {}             # информация о текущей используемой частичной клавиатуре
        self._messages_to_delete: telebot.types.Message = None     # если надо удалять более одного сообщения, то второе записывается сюда
        self._header_message: telebot.types.Message = None
        self._last_message: telebot.types.Message = None
        self._max_checkout_date: datetime = None    # максимальная дата выезда
        self._hotels: Hotels = Hotels()


        self.reinit_keyboard()

    def set_keyboard_data(self, *, case: str, current: int, last: int) -> None:
        """
        Запись информации об используемой в настоящий момент частичной клавиатуре

        :param case: текущее состояние
        :param current: текущий номер частичной клавиатуры
        :param last: всего частичных клавиатур

        """
        self._keyboard_maker['case'] = case
        self._keyboard_maker['current'] = current
        self._keyboard_maker['last'] = last

    def retrieve_keyboard_data(self) -> Tuple[str, int, int]:
        """
        Возвращает информацию об используемой в настоящий момент частичной клавиатуре

        :return: описание частичной клавиатуры

        """
        return self._keyboard_maker['case'], self._keyboard_maker['current'], self._keyboard_maker['last']

    def next_keyboard(self) -> int:
        """
        Возвращает номер следующей частичной клавиатуры
        Если это была последняя, возвращает "0"

        :return: номер следующей клавиатуры

        """
        current = self._keyboard_maker['current']
        last = self._keyboard_maker['last']
        next = current + 1
        if next <= last:
            self._keyboard_maker['current'] = next
            return next
        return 0

    def reinit_keyboard(self) -> None:
        """
        Инициализация (сброс) данных о частичной клавиатуре

        """
        self._keyboard_maker['case'] = 'none'
        self._keyboard_maker['current'] = 0
        self._keyboard_maker['last'] = 0

    def calculate_nights(self) -> bool:
        """
        Посчитать кол-во ночей

        :return bool: True = кол-во ночей не превышает 28

        """
        diff: datetime.timedelta = self._checkout_date - self._checkin_date
        self._nights = diff.days
        return self._nights <= 28

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def substate(self):
        return self._substate

    @substate.setter
    def substate(self, st):
        self._substate = st

    @property
    def selected_country_id(self):
        return self._selected_country_id

    @selected_country_id.setter
    def selected_country_id(self, id):
        self._selected_country_id = id

    @property
    def selected_city_id(self):
        return self._selected_city_id

    @selected_city_id.setter
    def selected_city_id(self, id):
        self._selected_city_id = id

    @property
    def hotels_amount(self):
        return self._hotels_amount

    @hotels_amount.setter
    def hotels_amount(self, amount: int):
        self._hotels_amount = amount

    @property
    def photo_required(self):
        return self._photo_required

    @photo_required.setter
    def photo_required(self, b: bool):
        self._photo_required = b

    @property
    def photos_amount(self):
        return self._photos_amount

    @photos_amount.setter
    def photos_amount(self, amount: int):
        self._photos_amount = amount

    @property
    def checkin_date(self):
        return self._checkin_date

    @checkin_date.setter
    def checkin_date(self, d):
        today = datetime.now()
        if d > today:
            self._checkin_date = d
        else:
            raise ValueError('Дата заезда должна быть не ранее "завтрашнего" дня')

        self._max_checkout_date = d + timedelta(days=+28)

    @property
    def checkout_date(self):
        return self._checkout_date

    @checkout_date.setter
    def checkout_date(self, d):
        if d > self._checkin_date:
            self._checkout_date = d
        else:
            raise ValueError('Дата выезда должна быть хотя бы на 1 день позже даты заезда')

    @property
    def nights(self):
        return self._nights

    @property
    def message_to_delete(self):
        return  self._messages_to_delete

    @message_to_delete.setter
    def message_to_delete(self, msg):
        self._messages_to_delete = msg

    @property
    def header_message(self):
        return self._header_message

    @header_message.setter
    def header_message(self, msg):
        self._header_message = msg

    @property
    def last_message(self):
        return self._last_message

    @last_message.setter
    def last_message(self, msg):
        self._last_message = msg

    @property
    def max_checkout_date(self):
        return self._max_checkout_date

    @property
    def hotels(self):
        return self._hotels

    @property
    def keyboard_maker(self):
        return self._keyboard_maker





