from datetime import datetime

from telebot import telebot
from typing import *

from commands.select_checkout_date import select_checkout_date
from config import DELETE_OLD_KEYBOARDS, LOWPRICE_SUBSTATES
from functions import keyboard_input_date
from functions.send_message_helper import send_message_helper
from functions.keyboard_input_date import keyboard_input_date, input_date_callback_factory
from functions.reenter_date import reenter_date
from loader import bot


def select_checkin_date(message: telebot.types.Message) -> None:
    """
    Выбор даты заезда

    :param message:

    """
    user: int = message.chat.id
    chat: int = message.chat.id
    keyboard = keyboard_input_date()

    # приглашение
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text='Выберите дату заезда: __.__.____',
        reply_markup=keyboard
    )

    with bot.retrieve_data(user, chat) as data:
        data['usd'].message_to_delete = msg
        data['usd'].last_message = msg


def filter_func(call):

    user = call.message.chat.id
    chat = call.message.chat.id

    with bot.retrieve_data(user, chat) as data:
        x = data['usd'].substate == LOWPRICE_SUBSTATES.SELECT_CHECKIN_DATE.value
        return x


# @bot.callback_query_handler(
#     func=filter_func,
#     filter_input_date=input_date_callback_factory.filter(type='D')
# )
# def day_button(call: telebot.types.CallbackQuery) -> None:
#     """
#     Обработчик события нажатия на кнопку
#
#     :param call: telebot.types.CallbackQuery
#     :return: None
#
#     """
#     user: int = call.message.chat.id
#     chat: int = call.message.chat.id
#
#     callback_data = input_date_callback_factory.parse(callback_data=call.data)
#
#     day = int(callback_data['content'])
#
#     old = call.message.text
#     new = '{}{:02d}{}'.format(old[:-10], day, old[-8:])
#     send_message_helper(bot.edit_message_text, retries=3)(
#         chat_id=chat,
#         message_id=call.message.message_id,
#         text=new,
#         parse_mode='HTML',
#         reply_markup=keyboard_input_date()
#     )

#
# @bot.callback_query_handler(
#     func=filter_func,
#     filter_input_date=input_date_callback_factory.filter(type='M')
# )
# def month_button(call: telebot.types.CallbackQuery) -> None:
#     """
#     Обработчик события нажатия на кнопку выбора страны
#
#     :param call: telebot.types.CallbackQuery
#     :return: None
#
#     """
#     user: int = call.message.chat.id
#     chat: int = call.message.chat.id
#
#     callback_data = input_date_callback_factory.parse(callback_data=call.data)
#
#     month = int(callback_data['content'])
#
#     old = call.message.text
#     new = '{}{:02d}{}'.format(old[:-7], month, old[-5:])
#     send_message_helper(bot.edit_message_text, retries=3)(
#         chat_id=chat,
#         message_id=call.message.message_id,
#         text=new,
#         parse_mode='HTML',
#         reply_markup=keyboard_input_date()
#     )
#
#
# @bot.callback_query_handler(
#     func=filter_func,
#     filter_input_date=input_date_callback_factory.filter(type='Y')
# )
# def year_button(call: telebot.types.CallbackQuery) -> None:
#     """
#     Обработчик события нажатия на кнопку выбора страны
#
#     :param call: telebot.types.CallbackQuery
#     :return: None
#
#     """
#     user: int = call.message.chat.id
#     chat: int = call.message.chat.id
#
#     callback_data = input_date_callback_factory.parse(callback_data=call.data)
#
#     year = int(callback_data['content'])
#
#     old = call.message.text
#     new = old[:-4] + str(year)
#     send_message_helper(bot.edit_message_text, retries=3)(
#         chat_id=chat,
#         message_id=call.message.message_id,
#         text=new,
#         parse_mode='HTML',
#         reply_markup=keyboard_input_date()
#     )


@bot.callback_query_handler(
    func=filter_func,
    filter_input_date=input_date_callback_factory.filter(type='enter')
)
def enter_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку "готово"

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    #callback_data: Dict[str, str] = input_date_callback_factory.parse(callback_data=call.data)
    try:
        checkin_date = datetime.strptime(call.message.text[-10:], '%d.%m.%Y')
    except ValueError:
        reenter_date(call.message)
        return


    # удаляем клавиатуру
    # if DELETE_OLD_KEYBOARDS:
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=call.message.id
    #     )

    # запоминаем информацию
    with bot.retrieve_data(user, chat) as data:
        data['usd'].checkin_date = checkin_date

    # удаляем клавиатуру
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=call.message.id,
        text='Выберите дату заезда: {}'.format(checkin_date.strftime('%d.%m.%Y'))
    )

    """ переходим к выбору даты выезда """

    # переходим в новое состояние
    with bot.retrieve_data(user, chat) as data:
        data['usd'].substate = LOWPRICE_SUBSTATES.SELECT_CHECKOUT_DATE.value

    select_checkout_date(message=call.message)



