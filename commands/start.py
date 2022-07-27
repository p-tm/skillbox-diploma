from telebot import telebot
from typing import *

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.menu import menu
from functions.send_message_helper import send_message_helper
from loader import bot, storage


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    """
    Обработчик команды "/start"

    :param message: telebot.types.Message - сообщение от пользователя
    :return: None

    """
    #user = message.from_user.id
    user: int = message.chat.id
    chat: int = message.chat.id

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

    if bot.get_state(user, chat) is None:

        hello_message: str = 'Здравствуйте!\n\n' \
                             'Это бот по поиску и подбору отелей\n\n' \
                             'Если я правильно понимаю, Вы - <b>{}</b>\n'.format(
            message.from_user.full_name
        )

        if message.from_user.username is not None:
            hello_message += '(aka @{})\n'.format(message.from_user.username)

        # try:
        #     bot.send_message(
        #         chat_id=chat2,
        #         text=hello_message,
        #         parse_mode='HTML'
        #     )
        # except exceptions.ReadTimeout:
        #     a = 1
        #     raise
        # except BaseException as e:
        #     b = 1

        send_message_helper(bot.send_message, retries=3)(chat_id=chat, text=hello_message, parse_mode='HTML')

        bot.set_state(user_id=user, state=UserState.user_started_bot, chat_id=chat)
        bot.add_data(user_id=user, chat_id=chat, usd=UserStateData()) # key = 'usd'

        # вызов главного меню (в виде inline кнопок)
        menu(message)

    else:
        already_started_message: str = 'Вы уже стартовали. Для прерывания выполнения текущего запроса используйте ' \
                                       'команду "/stop" '
        send_message_helper(bot.send_message, retries=3)(chat_id=chat, text=already_started_message)
        # try:
        #     bot.send_message(
        #         chat,
        #         'Вы уже стартовали. Для прерывания выполнения текущего запроса используйте команду "/stop"'
        #     )
        # except exceptions.ReadTimeout:
        #     raise


