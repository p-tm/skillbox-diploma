from telebot import telebot

from functions.send_message_helper import send_message_helper
from loader import bot


@bot.message_handler()
def unexpected_command(message: telebot.types.Message) -> None:
    """
    Обработчик неизвестной или недопустимой команды
    (этот обработчик вызывается, если до этого ни один другой не был вызван)

    :param message:

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text='Неизвестная или недопустимая команда.\nЕсли Вы хотите остановить выполнение текущей команды, введите "/stop"'
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
