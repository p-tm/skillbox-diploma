from typing import  *

from telebot import telebot
from telebot import types as tt


def init_ui(bot: telebot.TeleBot) -> None:
    """
    Функция:
    -------
    Инициализация элементов интерфейса пользователя

    :return: None

    """
    bot.set_my_commands([
        tt.BotCommand('/start', 'Перезапуск бота'),
        tt.BotCommand('/help', 'Помощь'),
        tt.BotCommand('/menu', 'Вызов меню команд'),
        tt.BotCommand('/stop', 'Прервать текущий запрос'),
        tt.BotCommand('/lowprice', 'Подобрать самые дешёвые отели'),
        tt.BotCommand('/highprice', 'Подобрать самые дорогие отели')
    ])
