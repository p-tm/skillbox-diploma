"""
Неизвестная или недопустимая команда

"""
from telebot import telebot
from typing import Any, Dict

from classes.user_state_data import UserStateData
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from loader import bot


@bot.message_handler()
def unexpected_command(message: telebot.types.Message) -> None:
    """
    Обработчик неизвестной или недопустимой команды
    (этот обработчик вызывается, если до этого ни один другой не был вызван)

    :param message:

    """
    usd: UserStateData = get_usd(message=message)

    unknown_command_message: str = (
        'Неизвестная или недопустимая команда.\n'
        'Если Вы хотите остановить выполнение текущей команды,'
        'введите "/stop"'
    )

    check_state: str = bot.get_state(user_id=usd.user, chat_id=usd.chat)
    if check_state is None:
        return

    """  логгирование """
    usd.history.add_rec('UCMD', '\"{}\" (неизвестная или недопустимая команда)'.format(message.text))

    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=unknown_command_message
    )

    # вытаскиваем предыдущее сообщение (до неизвестной команды)
    # и дублируем его
    msg = usd.last_message

    send_message_helper(bot.send_message, retries=3)(
        chat_id=msg.chat.id,
        text=msg.text,
        reply_markup=msg.reply_markup
    )
