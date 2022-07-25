import math

from typing import *

from classes.user_state_data import UserStateData
from classes.countries import Countries

from telebot import telebot, types as tt
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

from loader import bot, storage, countries


select_country_buttons_callback_factory = CallbackData('cmd_id', prefix='country')

class SelectCountryCallbackFilter(AdvancedCustomFilter):
    key = 'filter_select_country'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter) -> bool:
        x = config.check(query=call)
        return x

bot.add_custom_filter(SelectCountryCallbackFilter())

def keyboard_select_country(countries: Countries) -> List[telebot.types.InlineKeyboardMarkup]:
    """
    Функция:
    -------
    Создаёт виртуальную клавиатуру с кнопками для выбора страны

    :param countries: Countries
        - перечень стран
    :return: List[telebot.types.InlineKeyboardMarkup]
        - объект: клавиатура (набор клавиатур)

    """
    _countries = list(countries.values())
    number_of_keyboards = math.ceil(countries.size / 100)

    kb_parts = []

    buttons = [
        [
            tt.InlineKeyboardButton(
                text=_countries[j * 3 + i].nicename,
                #callback_data='/cmd country ' + str(_countries[j * 3 + i].id)
                callback_data=select_country_buttons_callback_factory.new(cmd_id=str(_countries[j * 3 + i].id))
            )
            for i in range(3)
            if j * 3 + i < countries.size
        ]
        for j in range(0, int(100 / 3))
    ]

    kb_parts.append(buttons)

    buttons = [
        [
            tt.InlineKeyboardButton(
                text=_countries[j * 3 + i].nicename,
                callback_data='/cmd country ' + str(_countries[j * 3 + i].id)
            )
            for i in range(3)
            if j * 3 + i < countries.size
        ]
        for j in range(int(100 / 3), int(200 / 3))
    ]

    kb_parts.append(buttons)

    buttons = [
        [
            tt.InlineKeyboardButton(
                text=_countries[j * 3 + i].nicename,
                callback_data='/cmd country ' + str(_countries[j * 3 + i].id)
            )
            for i in range(3)
            if j * 3 + i < countries.size
        ]
        for j in range(int(200 / 3), int(countries.size / 3) + 1)
    ]

    kb_parts.append(buttons)

    keyboards = [tt.InlineKeyboardMarkup(item) for item in kb_parts]

    return keyboards

def select_country(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """
    Функция:
    -------
    Выбор страны

    :param message: telebot.types.Message
        - сообщение
    :param bot: telebot.TeleBot
        -
    :return: None

    """
    user: int = message.chat.id
    chat: int = message.chat.id
    keyboards = keyboard_select_country(countries)

    bot.send_message(
        chat_id=chat,
        text='Выберите страну:',
        reply_markup=keyboards[0]
    )
    bot.send_message(
        chat_id=chat,
        text='---',
        reply_markup=keyboards[1]
    )
    bot.send_message(
        chat_id=chat,
        text='---',
        reply_markup=keyboards[2]
    )


@bot.callback_query_handler(
    func=None,
    filter_select_country=select_country_buttons_callback_factory.filter()
)
def country_selector_button(call):

    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data: Dict[str, str] = select_country_buttons_callback_factory.parse(callback_data=call.data)

    with bot.retrieve_data(user, chat) as data:
        data['usd'].selected_country_id = callback_data['cmd_id']




