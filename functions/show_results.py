import pickle

from telebot import telebot
from typing import *

from classes.hotel import Hotel
from classes.user_state_data import UserStateData
from commands.menu import menu
from config import LowpriceSubstates, SUBSTATE_NONE
from functions.print_results_data import print_results_data
from functions.send_message_helper import send_message_helper
from loader import bot


def show_results(message: telebot.types.Message) -> None:
    """
    Выводит результаты поиска отелей

    :param message: предыдущее сообщение в чате Telegram

    """
    suitable_hotels_message: str = 'Список подходящих отелей:'

    user: int = message.chat.id
    chat: int = message.chat.id

    send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=suitable_hotels_message
    )

    data: Dict[str, UserStateData]
    with bot.retrieve_data(chat_id=chat, user_id=user) as data:
        usd = data['usd']

    print_results_data(message, usd)

    """ логгирование """
    bobj: 'binary_object' = pickle.dumps(usd)
    usd.history.add_rec('RSLT', bobj.__str__())

    """ на этом процесс закончен, выдаём главное меню для новго выбора """

    horiz_delimiter = '----------------------------------------------------------------------'

    send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=horiz_delimiter
    )

    # # переходим в новое состояние
    # with bot.retrieve_data(user, chat) as data:
    #     data['usd'].substate = SUBSTATE_NONE

    menu(message=message)