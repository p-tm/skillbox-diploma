"""
Реализация шага по выбору города

"""
import math

from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter
from typing import Dict, Optional, Tuple

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_hotels_amount import select_hotels_amount
from config import BestdealSubstates, DELETE_OLD_KEYBOARDS, HighpriceSubstates, LowpriceSubstates, MAX_KEYS_PER_KEYBOARD
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper

from loader import bot, countries, select_city_buttons_callback_factory


# select_city_buttons_callback_factory = CallbackData('cmd_id', prefix='city')


class SelectCityCallbackFilter(AdvancedCustomFilter):
    """
    Фильтрация callback_data - выделяем данные, которые относятся к клавиатуре выбора города

    """
    key = 'filter_select_city'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter) -> bool:
        """
        Функция фильтрации

        """
        usd: UserStateData = get_usd(message=call.message)
        if usd is None:
            return False

        is_select_city: bool = False
        if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
            is_select_city = usd.substate == LowpriceSubstates.SELECT_CITY.value
        elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
            is_select_city = usd.substate == HighpriceSubstates.SELECT_CITY.value
        elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
            is_select_city = usd.substate == BestdealSubstates.SELECT_CITY.value

        return is_select_city and config.check(query=call)


bot.add_custom_filter(SelectCityCallbackFilter())


def keyboard_select_city(cid: int, current: Optional[int] = 1) -> Tuple[telebot.types.InlineKeyboardMarkup, int, int]:
    """
    Создаёт виртуальную клавиатуру с кнопками для выбора города

    :param cid: идентификатор страны
    :param current: номер куска клавиатуры
    :return: объект: inline-клавиатура для сообщения

    """
    _cities = list(countries[cid].cities.values())
    keys_per_kb: int = MAX_KEYS_PER_KEYBOARD
    number_of_keyboards = math.ceil(countries[cid].cities.size / keys_per_kb)
    first_row = int((current - 1) * keys_per_kb/3)
    last_row = first_row + int(keys_per_kb/3)

    buttons = [
        [
            InlineKeyboardButton(
                text=_cities[j * 3 + i].name,
                callback_data=select_city_buttons_callback_factory.new(cmd_id=str(_cities[j * 3 + i].city_id))
            )
            for i in range(3)
            if j * 3 + i < countries[cid].cities.size
        ]
        for j in range(first_row, last_row) # 10 строчек по 3 кнопки
    ]
    if not current == number_of_keyboards:
        buttons.append(
            [
                InlineKeyboardButton(text='ещё...', callback_data=select_city_buttons_callback_factory.new(cmd_id='keyboard_next_part'))
            ]
        )

    keyboard = InlineKeyboardMarkup(buttons)

    return keyboard, current, number_of_keyboards


def select_city(cid: int, message: telebot.types.Message, kbrd: Optional[int] = 1) -> None:
    """
    Выбор города

    :param cid: country id (получено от удалённого сервера)
    :param message: предыдущее сообщение в чате Telegram
    :param kbrd: порядковый номер частичной клавиатуры

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    keyboard, current, last = keyboard_select_city(cid, kbrd)

    usd.set_keyboard_data(case='cities', current=current, last=last)

    # рисуем первые 30 кнопок
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text='Выберите город:',
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
    filter_select_city=select_city_buttons_callback_factory.filter(cmd_id='keyboard_next_part')
)
def next_part_of_keyboard(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку "ещё..." (т.е. показать следующую часть клавиатуры)

    :param call: telebot.types.CallbackQuery

    """
    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return

    if DELETE_OLD_KEYBOARDS:
        send_message_helper(bot.delete_message, retries=3)(
            chat_id=usd.chat,
            message_id=call.message.id
        )

    cid: int = usd.selected_country_id
    kbrd: int = usd.next_keyboard()

    select_city(cid=cid, message=call.message, kbrd=kbrd)


@bot.callback_query_handler(
    func=None,
    state=[
        UserState.user_lowprice_in_progress,
        UserState.user_highprice_in_progress,
        UserState.user_bestdeal_in_progress
    ],
    filter_select_city=select_city_buttons_callback_factory.filter()
)
def city_selector_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку выбора страны

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return

    callback_data: Dict[str, str] = select_city_buttons_callback_factory.parse(callback_data=call.data)

    selected_city_id = int(callback_data['cmd_id'])

    # if DELETE_OLD_KEYBOARDS:
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=call.message.id
    #     )

    usd.selected_city_id = selected_city_id
    usd.reinit_keyboard()

    # новое состояние
    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        usd.substate = LowpriceSubstates.SELECT_HOTELS_AMOUNT.value
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        usd.substate = HighpriceSubstates.SELECT_HOTELS_AMOUNT.value
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SELECT_HOTELS_AMOUNT.value

    select_hotels_amount(message=call.message)


