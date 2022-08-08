"""
Описание функции

"""
from telebot import telebot

from classes.user_state_data import UserStateData
from commands.menu import menu
from functions.send_message_helper import send_message_helper

from loader import bot

def start_new(message: telebot.types.Message, usd: UserStateData) -> None:
    """
    Функция вызывается когда запрос завершён
    выдаём главное меню для нового выбора

    :param message:
    :param usd:

    """
    horiz_delimiter = '------------------------------------------------------------------------------------------------'

    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=horiz_delimiter
    )

    menu(message=message)