"""
Описание функции

"""
from telebot import telebot
from typing import Dict

from classes.user_state_data import UserStateData
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from loader import bot


def reenter_date(message: telebot.types.Message, caption: str) -> None:
    """
    Приглашение на повторный ввод даты (если таковой требуется)
    (например после ввода некорректной даты)

    :param message: предыдущее сообщение в чате Telegram
    :param caption: текст аварийного сообщения

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    # для начала удаляем клавиатуру
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=usd.chat,
        message_id=message.id,
        text=message.text
    )

    # выводим сообщение об ошибке
    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=caption
    )

    msg = usd.last_message

    # повторяем предыдущее сообщение (вместе с клавиатурой)
    send_message_helper(bot.send_message, retries=3)(
        chat_id=msg.chat.id,
        text=msg.text,
        reply_markup=msg.reply_markup
    )
