from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter
from typing import *

from functions.send_message_helper import send_message_helper
from loader import bot, input_date_callback_factory

# input_date_callback_factory = CallbackData('type', 'content', prefix='date')


class InputDateCallbackFilter(AdvancedCustomFilter):
    """
    Фильтрация callback_data - выделяем данные, которые относятся к клавиатуре ввода даты

    """
    key = 'filter_input_date'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter) -> bool:
        """
        Функция фильтрации

        """
        return config.check(query=call)


bot.add_custom_filter(InputDateCallbackFilter())

def days_buttons_row(start_day: int) -> List[telebot.types.InlineKeyboardButton]:
    """
    Генератор кнопок для "дней" по строкам

    :param start_day: первый день в строек
    :return: строка кнопок

    """
    if start_day < 29:
        out: List[telebot.types.InlineKeyboardButton] = [
            InlineKeyboardButton(text=str(i), callback_data=input_date_callback_factory.new(type='D', content=str(i)))
            for i in range(start_day, start_day + 7)
        ]
    else:
        out: List[telebot.types.InlineKeyboardButton] = [
            InlineKeyboardButton(text=str(i), callback_data=input_date_callback_factory.new(type='D', content=str(i)))
            for i in range(29, 29 + 3)
        ]
        aux: List[telebot.types.InlineKeyboardButton] = [
            InlineKeyboardButton(text='-', callback_data=input_date_callback_factory.new(type='idle', content='idle'))
            for _ in range(4)
        ]
        out.extend(aux)

    return out

def months_buttons_row(start_month: int) -> List[telebot.types.InlineKeyboardButton]:
    """
    Генератор кнопок для "месяцев" по строкам

    :param start_month: первый месяц в строке
    :return: строка кнопок

    """
    months: Tuple = ('янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек')
    start_index: int = start_month - 1

    return [
        InlineKeyboardButton(text=months[i], callback_data=input_date_callback_factory.new(type='M', content=(i + 1)))
        for i in range(start_index, start_index + 6)
    ]

def years_buttons_row(start_year: int, size: int) -> List[telebot.types.InlineKeyboardButton]:
    """
    Генератор кнопок для "годов" по строкам

    :param start_year: первый год в строке
    :param size: количество кнопок
    :return: строка кнопок

    """
    return [
        InlineKeyboardButton(text=str(i), callback_data=input_date_callback_factory.new(type='Y', content=i))
        for i in range(start_year, start_year + size)
    ]


def keyboard_input_date():
    buttons = [
        days_buttons_row(1),
        days_buttons_row(8),
        days_buttons_row(15),
        days_buttons_row(22),
        days_buttons_row(29),
        months_buttons_row(1),
        months_buttons_row(7),
        years_buttons_row(2022, 2),
        [
            InlineKeyboardButton(text='Готово', callback_data=input_date_callback_factory.new(type='enter', content='enter'))
        ]
    ]

    return InlineKeyboardMarkup(buttons)



@bot.callback_query_handler(
    func=None,
    filter_input_date=input_date_callback_factory.filter(type='D')
)
def day_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку

    :param call: telebot.types.CallbackQuery

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data = input_date_callback_factory.parse(callback_data=call.data)

    day = int(callback_data['content'])

    old = call.message.text
    new = '{}{:02d}{}'.format(old[:-10], day, old[-8:])
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=call.message.message_id,
        text=new,
        parse_mode='HTML',
        reply_markup=keyboard_input_date()
    )


@bot.callback_query_handler(
    func=None,
    filter_input_date=input_date_callback_factory.filter(type='M')
)
def month_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку выбора страны

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data = input_date_callback_factory.parse(callback_data=call.data)

    month = int(callback_data['content'])

    old = call.message.text
    new = '{}{:02d}{}'.format(old[:-7], month, old[-5:])
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=call.message.message_id,
        text=new,
        parse_mode='HTML',
        reply_markup=keyboard_input_date()
    )

@bot.callback_query_handler(
    func=None,
    filter_input_date=input_date_callback_factory.filter(type='Y')
)
def year_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку выбора страны

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data = input_date_callback_factory.parse(callback_data=call.data)

    year = int(callback_data['content'])

    old = call.message.text
    new = old[:-4] + str(year)
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=call.message.message_id,
        text=new,
        parse_mode='HTML',
        reply_markup=keyboard_input_date()
    )
