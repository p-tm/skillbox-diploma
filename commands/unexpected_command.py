from telebot import telebot
from typing import *

from functions.send_message_helper import send_message_helper
from loader import bot


@bot.message_handler()
def unexpected_command(message: telebot.types.Message) -> None:
    """
    Обработчик неизвестной или недопустимой команды
    (этот обработчик вызывается, если до этого ни один другой не был вызван)

    :param message:

    """
    unknown_command_message: str = ('Неизвестная или недопустимая команда.\n'
                                    'Если Вы хотите остановить выполнение текущей команды, введите "/stop"')
    user: int = message.chat.id
    chat: int = message.chat.id

    """  логгирование """
    data: Dict[str, Any]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        data['usd'].history.add_rec('UCMD', '\"' + message.text + '\"')

    send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=unknown_command_message
    )

    # вытаскиваем предыдущее сообщение (до неизвестной команды)
    # и дублируем его
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        msg = data['usd'].last_message

    send_message_helper(bot.send_message, retries=3)(
        chat_id=msg.chat.id,
        text=msg.text,
        reply_markup=msg.reply_markup
    )
