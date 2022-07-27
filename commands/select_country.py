import math

from typing import *

from classes.user_state_data import UserStateData
from classes.countries import Countries

from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter

from config import MAX_KEYS_PER_KEYBOARD
from functions.send_message_helper import send_message_helper
from loader import bot, storage, countries


select_country_buttons_callback_factory = CallbackData('cmd_id', prefix='country')

class SelectCountryCallbackFilter(AdvancedCustomFilter):
    """
    Фильтрация callback_data - выделяем данные, которые относятся к клавиатуре выбора страны

    """
    key = 'filter_select_country'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter) -> bool:
        """
        Функция фильтрации

        """
        x = config.check(query=call)
        return x

class CountryNextKbrdCallbackFilter(SimpleCustomFilter):
    """
    Фильтрация callback_data - выделяем данные которые относятся к кнопке "далее" при выборе страны

    """
    key = 'filter_country_next_kbrd'

    def check(self, call: telebot.types.CallbackQuery) -> bool:
        st = storage
        with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
            x = data['usd'].keyboard_maker['case'] == 'countries'
        return x

bot.add_custom_filter(SelectCountryCallbackFilter())
bot.add_custom_filter(CountryNextKbrdCallbackFilter())

def keyboard_select_country(countries: Countries, current: Optional[int] = 1) -> List[telebot.types.InlineKeyboardMarkup]:
    """
    Создаёт виртуальную клавиатуру с кнопками для выбора страны

    :param countries: Countries - перечень стран
    :param current: Optional[int] - номер куска клавиатуры
    :return: List[telebot.types.InlineKeyboardMarkup] - объект: клавиатура (набор клавиатур)

    """
    _countries = list(countries.values())
    keys_per_kb: int = MAX_KEYS_PER_KEYBOARD
    number_of_keyboards = math.ceil(countries.size / keys_per_kb)
    first_key = int((current - 1) * keys_per_kb/3)
    last_key = first_key + int(keys_per_kb/3)

    buttons = [
        [
            InlineKeyboardButton(
                text=_countries[j * 3 + i].nicename,
                callback_data=select_country_buttons_callback_factory.new(cmd_id=str(_countries[j * 3 + i].id))
            )
            for i in range(3)
            if j * 3 + i < countries.size
        ]
        for j in range(first_key, last_key) # 10 строчек по 3 кнопки
    ]
    if not current == number_of_keyboards:
        buttons.append(
            [
                InlineKeyboardButton(text='ещё...', callback_data='keyboard_next_part')
            ]
        )

    keyboard = InlineKeyboardMarkup(buttons)

    return keyboard, current, number_of_keyboards

def select_country(
        message: telebot.types.Message,
        bot: telebot.TeleBot,
        kbrd: Optional[int] = 1
) -> None:
    """
    Выбор страны

    :param message: telebot.types.Message - сообщение
    :param bot: telebot.TeleBot - объект бота
    :param kbrd: telebot.types.InlineKeyboardMarkup - порядковый номер частичной клаавиатуры
    :return: None

    """
    user: int = message.chat.id
    chat: int = message.chat.id
    keyboard, current, last = keyboard_select_country(countries, kbrd)

    with bot.retrieve_data(user, chat) as data:
        data['usd'].set_keyboard_data(case='countries', current=current, last=last)

    # рисуем первые 30 кнопок
    send_message_helper(bot.send_message)(
        chat_id=chat,
        text='Выберите страну:',
        reply_markup=keyboard
    )


@bot.callback_query_handler(
    func=None,
    filter_select_country=select_country_buttons_callback_factory.filter()
)
def country_selector_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку выбора страны

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data: Dict[str, str] = select_country_buttons_callback_factory.parse(callback_data=call.data)

    with bot.retrieve_data(user, chat) as data:
        data['usd'].selected_country_id = callback_data['cmd_id']


@bot.callback_query_handler(
    func=None,
    filter_country_next_kbrd=True
)
def next_part_of_keyboard(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку "ещё..." (т.е. показать следующую часть клавиатуры)

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    with bot.retrieve_data(user, chat) as data:
        kbrd: int = data['usd'].next_keyboard()

    select_country(call.message, bot, kbrd)


