"""
Описание класса

"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from telebot import telebot
from typing import Dict, Optional, Tuple, Union

from classes.hotels import Hotels


@dataclass
class UserStateData:
    """
    Хранение данных (состояния) конкретного пользователя в конкретном чате
    Инкапсулирует все данные, индивидуальные для пользователя (перечень выбранных отелей и т.п.)

    """
    _substate: Optional[int]                        # текущее состояние (суб-состояние, внутри основного)
    _selected_country_id: Optional[int]             # id выбранной страны (берётся из удалённого запроса)
    _selected_city_id: Optional[int]                # id выбранного города (берётся из удалённого запроса)
    _hotels_amount: Optional[int]                   # количество отелей
    _photo_required: Optional[bool]                 # требуется ли фотография
    _photos_amount: Optional[int]                   # количество фото
    _checkin_date: Optional[datetime]               # дата заезда
    _checkout_date: Optional[datetime]              # дата выезда
    _nights: Optional[int]                          # количество ночей
    _keyboard_maker: Dict[str, Union[str, int]]     # информация о текущей используемой частичной клавиатуре
    _messages_to_delete: Optional[telebot.types.Message]   # сообщение, которые впоследствие надо удалить
    _header_message: Optional[telebot.types.Message]       # логический заголовок
    _last_message: Optional[telebot.types.Message]  # последнее сообщение
    _max_checkout_date: Optional[datetime]          # максимальная дата выезда
    _hotels: Hotels                                 # перечень выбранных отелей
    history: 'HistoryLog'                           # логгер

    def __init__(self) -> None:
        """
        Конструктор

        """
        from classes.history_log import HistoryLog

        self._substate = None
        self._selected_country_id = None
        self._selected_city_id = None
        self._hotels_amount = None
        self._photo_required = None
        self._photos_amount = None
        self._checkin_date = None
        self._checkout_date = None
        self._nights = None
        self._keyboard_maker = {}
        self._messages_to_delete = None
        self._header_message = None
        self._last_message = None
        self._max_checkout_date = None
        self._hotels: Hotels = Hotels()
        self.history = HistoryLog()

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
        diff: timedelta = self._checkout_date - self._checkin_date
        self._nights = diff.days
        return self._nights <= 28

    def summary(self, *, history: Optional[bool] = False) -> str:
        """
        Формирует текст сообщения для show_summary()

        :return: текст сообщения

        """

        from loader import countries

        country_key = self._selected_country_id
        city_key = self._selected_city_id

        if not history:
            tmp = 'Итак, Ваши критерии поиска:\n\n'
        else:
            tmp = 'Итоговые критерии поиска:\n\n'

        summary_message: str = (
            tmp +
            '<i>Страна:</i> {}\n'
            '<i>Город:</i> {}\n'
            '<i>Дата заезда:</i> {}\n'
            '<i>Дата выезда:</i> {}\n'
            '<i>Количество ночей:</i> {}\n'
            '<i>Количество отелей:</i> {}\n'
            '<i>Показывать фото:</i> {}'
        ).format(
            countries[country_key].nicename,
            countries[country_key].cities[city_key].name,
            self._checkin_date.strftime('%d.%m.%Y'),
            self._checkout_date.strftime('%d.%m.%Y'),
            self._nights,
            self._hotels_amount,
            'Да' if self._photo_required else 'Нет'
        )

        if self._photo_required:
            summary_message += '\n<i>Количество фото:</i> {}'.format(self._photos_amount)

        return summary_message

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
