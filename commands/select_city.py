import math

from telebot import telebot
from telebot.types import Message
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter
from typing import *

from classes.cities import Cities
from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_hotels_amount import select_hotels_amount
from config import DELETE_OLD_KEYBOARDS, LOWPRICE_SUBSTATES, MAX_KEYS_PER_KEYBOARD

from functions.send_message_helper import send_message_helper

from loader import bot, countries, storage, select_city_buttons_callback_factory


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
        user = call.message.chat.id
        chat = call.message.chat.id
        with bot.retrieve_data(user, chat) as data:
            is_select_country = data['usd'].substate == LOWPRICE_SUBSTATES.SELECT_CITY.value
        return is_select_country and config.check(query=call)


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
    user: int = message.chat.id
    chat: int = message.chat.id
    keyboard, current, last = keyboard_select_city(cid, kbrd)

    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        data['usd'].set_keyboard_data(case='cities', current=current, last=last)

    # рисуем первые 30 кнопок
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text='Выберите город:',
        reply_markup=keyboard
    )

    with bot.retrieve_data(user, chat) as data:
        data['usd'].message_to_delete = msg
        data['usd'].last_message = msg


@bot.callback_query_handler(
    func=None,
    state=[UserState.user_lowprice_in_progress],
    filter_select_city=select_city_buttons_callback_factory.filter(cmd_id='keyboard_next_part')
)
def next_part_of_keyboard(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку "ещё..." (т.е. показать следующую часть клавиатуры)

    :param call: telebot.types.CallbackQuery

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    if DELETE_OLD_KEYBOARDS:
        send_message_helper(bot.delete_message, retries=3)(
            chat_id=chat,
            message_id=call.message.id
        )

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        cid: int = data['usd'].selected_country_id
        kbrd: int = data['usd'].next_keyboard()

    select_city(cid=cid, message=call.message, kbrd=kbrd)


@bot.callback_query_handler(
    func=None,
    state=[UserState.user_lowprice_in_progress],
    filter_select_city=select_city_buttons_callback_factory.filter()
)
def city_selector_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку выбора страны

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data: Dict[str, str] = select_city_buttons_callback_factory.parse(callback_data=call.data)

    selected_city_id = int(callback_data['cmd_id'])

    # if DELETE_OLD_KEYBOARDS:
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=call.message.id
    #     )

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        data['usd'].selected_city_id = selected_city_id
        data['usd'].reinit_keyboard()

    # новое состояние
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        data['usd'].substate = LOWPRICE_SUBSTATES.SELECT_HOTELS_AMOUNT.value

    select_hotels_amount(message=call.message)



