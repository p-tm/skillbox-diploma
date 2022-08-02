from telebot import telebot
from typing import *

from classes.user_state_data import UserStateData
from functions.send_message_helper import send_message_helper
from loader import bot


def reenter_date(message: telebot.types.Message, caption: str) -> None:
    """
    Приглашение на повторный ввод даты (если таковой требуется)
    (например после ввода некорректной даты)

    :param message: предыдущее сообщение в чате Telegram
    :param caption: текст аварийного сообщения

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    # для начала удаляем клавиатуру
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=message.id,
        text=message.text
    )

    # выводим сообщение об ошибке
    send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=caption
    )

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        msg = data['usd'].last_message

    # повторяем предыдущее сообщение (вместе с клавиатурой)
    send_message_helper(bot.send_message, retries=3)(
        chat_id=msg.chat.id,
        text=msg.text,
        reply_markup=msg.reply_markup
    )
