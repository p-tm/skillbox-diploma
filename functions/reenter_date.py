from telebot import telebot

from functions.send_message_helper import send_message_helper

from loader import bot

def reenter_date(message: telebot.types.Message) -> None:
    """
    Приглашение на повторный ввод даты (после ввода некорректной даты)

    :param message:

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    # для начала удаляем клавиатуру
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=message.id,
        text=message.text
    )

    send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text='Некорректное значение даты, введите дату ещё раз'
    )

    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        msg = data['usd'].last_message

    bot.send_message(
        chat_id=msg.chat.id,
        text=msg.text,
        reply_markup=msg.reply_markup
    )
