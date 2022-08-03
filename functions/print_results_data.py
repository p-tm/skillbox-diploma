from telebot import telebot
from typing import *

from classes.user_state_data import UserStateData
from functions.send_message_helper import send_message_helper
from loader import bot


def print_results_data(message: telebot.types.Message, usd: UserStateData) -> None:

    user: int = message.chat.id
    chat: int = message.chat.id

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

