from typing import *
from requests import exceptions

from telebot import telebot

from loader import bot, storage

from classes.user_state import UserState
from classes.user_state_data import UserStateData

from commands.menu import menu


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    """
    Функция:
    -------
    Обработчик команды "/start"

    :param message: telebot.types.Message
        - сообщение от пользователя
    :return: None

    """
    user = message.from_user.id
    chat = message.chat.id

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

    if bot.get_state(user, chat) is None:

        hello_message: str = 'Здравствуйте!\n\n' \
                             'Это бот по поиску и подбору отелей\n\n' \
                             'Если я правильно понимаю, Вы - <b>{}</b>\n'.format(
            message.from_user.full_name
        )

        if message.from_user.username is not None:
            hello_message += '(aka @{})\n'.format(message.from_user.username)

        try:
            bot.send_message(
                chat_id=chat,
                text=hello_message,
                parse_mode='HTML'
            )
        except exceptions.ReadTimeout:
            raise

        bot.set_state(user_id=user, state=UserState.user_started_bot, chat_id=chat)
        bot.add_data(user_id=user, chat_id=chat, usd=UserStateData()) # key = 'usd'

        # вызов главного меню (в виде inline кнопок)
        menu(message)

    else:

        try:
            bot.send_message(
                chat,
                'Вы уже стартовали. Для прерывания выполнения текущего запроса используйте команду "/stop"'
            )
        except exceptions.ReadTimeout:
            raise


