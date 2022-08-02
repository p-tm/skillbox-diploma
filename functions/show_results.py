from telebot import telebot
from typing import *

from classes.hotel import Hotel
from classes.user_state_data import UserStateData
from commands.menu import menu
from config import LOWPRICE_SUBSTATES
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

    keylist: List[int] = list(usd.hotels.keys())

    key: int
    for key in keylist:

        send_message_helper(bot.send_message, retries=3)(
            chat_id=chat,
            text=usd.hotels[key].print_to_telegram(),
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        ph: str
        for ph in usd.hotels[key].images:
            send_message_helper(bot.send_photo, retries=3)(
                chat_id=chat,
                photo=ph
            )

    """ на этом процесс закончен, выдаём главное меню для новго выбора """

    horiz_delimiter = '----------------------------------------------------------------------'

    send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=horiz_delimiter
    )

    # переходим в новое состояние
    with bot.retrieve_data(user, chat) as data:
        data['usd'].substate = LOWPRICE_SUBSTATES.NONE.value

    menu(message=message)