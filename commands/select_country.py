"""
Реализация шага по выбору страны

"""
import math

from telebot import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter
from typing import Any, Dict, List, Optional, Tuple

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from classes.countries import Countries
from commands.select_city import select_city
from config import (
    BestdealSubstates, DELETE_OLD_KEYBOARDS, HighpriceSubstates, LowpriceSubstates, MAX_KEYS_PER_KEYBOARD,
    POPULAR_COUNTRIES
)
from exceptions.data_unavalible import DataUnavailible
from functions.cities_per_country import cities_per_country
from functions.console_message import console_message
from functions.send_message_helper import send_message_helper
from functions.get_usd import get_usd
from functions.start_new import start_new
from loader import bot, storage, countries, select_country_buttons_callback_factory


# select_country_buttons_callback_factory = CallbackData('cmd_id', prefix='country')

class SelectCountryCallbackFilter(AdvancedCustomFilter):
    """
    Фильтрация callback_data - выделяем данные, которые относятся к клавиатуре выбора страны

    """
    key = 'filter_select_country'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter) -> bool:
        """
        Функция фильтрации - пропускает сообщения от кнопок выбора страны

        :return: True = пропустить сообщение

        """

        usd: UserStateData = get_usd(message=call.message)
        if usd is None:
            return False

        is_select_country: bool = False
        if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
            is_select_country = usd.substate == LowpriceSubstates.SELECT_COUNTRY.value
        elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
            is_select_country = usd.substate == HighpriceSubstates.SELECT_COUNTRY.value
        elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
            is_select_country = usd.substate == BestdealSubstates.SELECT_COUNTRY.value

        return is_select_country and config.check(query=call)


bot.add_custom_filter(SelectCountryCallbackFilter())


def keyboard_select_country(
        countries: Countries,
        current: Optional[int] = 1
) -> Tuple[telebot.types.InlineKeyboardMarkup, int, int]:
    """
    Создаёт виртуальную клавиатуру с кнопками для выбора страны

    :param countries: перечень стран
    :param current: номер куска клавиатуры
    :return: Tuple[объект inline-клавиатура для сообщения, номер текущей, всего]

    """
    _countries = list(countries.values())   # перечень стран в виде List - для удобства
    """ немного отсортируем, так, чтобы в начале оказались наиболее популярные """
    def exchange(src: List[Any], i_old: int, i_new: int):
        """ берёт i_old элемент списка и ставит его на место i_new """
        item: Any = src.pop(i_old)
        src.insert(i_new, item)

    # for i, popular_iso in enumerate(POPULAR_COUNTRIES):
    #     for j, country in enumerate(_countries):
    #         if country.iso == popular_iso:
    #             exchange(_countries, j, i)
    #             break
    [
        exchange(_countries, j, i)
        for i, popular_iso in enumerate(POPULAR_COUNTRIES)
        for j, country in enumerate(_countries)
        if country.iso == popular_iso
    ]

    keys_per_kb: int = MAX_KEYS_PER_KEYBOARD
    number_of_keyboards: int = math.ceil(countries.size / keys_per_kb)  # сколько частичных клавиатур получится
    first_row: int = int((current - 1) * keys_per_kb/3) # номер первой строки в частичной клавиатуре
    last_row: int = first_row + int(keys_per_kb/3)      # номер последней строки в частичной клавиатуре

    buttons = [
        [
            InlineKeyboardButton(
                text=_countries[j * 3 + i].nicename,
                callback_data=select_country_buttons_callback_factory.new(cmd_id=str(_countries[j * 3 + i].country_id))
            )
            for i in range(3)
            if j * 3 + i < countries.size
        ]
        for j in range(first_row, last_row) # 10 строчек по 3 кнопки
    ]
    if not current == number_of_keyboards:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='ещё...',
                    callback_data=select_country_buttons_callback_factory.new(cmd_id='keyboard_next_part')
                )
            ]
        )

    keyboard: telebot.types.InlineKeyboardMarkup = InlineKeyboardMarkup(buttons)

    return keyboard, current, number_of_keyboards


def select_country(message: telebot.types.Message, kbrd: Optional[int] = 1) -> None:
    """
    Выбор страны

    :param message: предыдущее сообщение в чате Telegram
    :param kbrd: порядковый номер частичной клавиатуры

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    keyboard, current, last = keyboard_select_country(countries, kbrd)

    usd.set_keyboard_data(case='countries', current=current, last=last)

    # рисуем первые 30 кнопок
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text='Выберите страну:',
        reply_markup=keyboard
    )

    usd.message_to_delete = msg
    usd.last_message = msg


@bot.callback_query_handler(
    func=None,
    state=[
        UserState.user_lowprice_in_progress,
        UserState.user_highprice_in_progress,
        UserState.user_bestdeal_in_progress
    ],
    filter_select_country=select_country_buttons_callback_factory.filter(cmd_id=['keyboard_next_part'])
)
def next_part_of_keyboard(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку "ещё..." (т.е. показать следующую часть клавиатуры)

    :param call:

    """
    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return

    if DELETE_OLD_KEYBOARDS:
        send_message_helper(bot.delete_message, retries=3)(
            chat_id=usd.chat,
            message_id=call.message.id
        )

    kbrd: int = usd.next_keyboard()

    select_country(call.message, kbrd)


@bot.callback_query_handler(
    func=None,
    state=[
        UserState.user_lowprice_in_progress,
        UserState.user_highprice_in_progress,
        UserState.user_bestdeal_in_progress
    ],
    filter_select_country=select_country_buttons_callback_factory.filter()
)
def country_selector_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку выбора страны

    :param call: telebot.types.CallbackQuery

    """
    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return

    callback_data: Dict[str, str] = select_country_buttons_callback_factory.parse(callback_data=call.data)

    selected_country_id = int(callback_data['cmd_id'])

    # if DELETE_OLD_KEYBOARDS:
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=call.message.id
    #     )

    usd.selected_country_id = selected_country_id
    usd.reinit_keyboard()

    """ переходим к выбору города """

    # новое состояние
    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        usd.substate = LowpriceSubstates.SELECT_CITY.value
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        usd.substate = HighpriceSubstates.SELECT_CITY.value
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SELECT_CITY.value

    # запрашиваем список городов в стране (удалённый запрос)
    try:
        cities_per_country(selected_country_id)
    except DataUnavailible as e:
        console_message('Не могу получить список городов.' + str(e))
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text="🚫 Не могу получить список городов."
         )
        start_new(message=call.message, usd=usd)
        return

    select_city(cid=selected_country_id, message=call.message)






