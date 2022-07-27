import sys
import time
import datetime

from typing import  *
from requests import exceptions

from telebot import telebot
from telebot import types as tt

from functions.console_message import console_message

from exceptions.fatal_error import FatalError


def init_ui(bot: telebot.TeleBot, *, retries: Optional[int] = 1) -> None:
    """
    Инициализация элементов интерфейса пользователя

    :param bot - инстанс бота
    :param retries: Optional[int] - число попыток
    :return: None

    """
    _tries_counter = 1
    while True:
        try:
            bot.set_my_commands([
                tt.BotCommand('/start', 'Перезапуск бота'),
                tt.BotCommand('/help', 'Помощь'),
                tt.BotCommand('/menu', 'Вызов меню команд'),
                tt.BotCommand('/stop', 'Прервать текущий запрос'),
                tt.BotCommand('/lowprice', 'Подобрать самые дешёвые отели'),
                tt.BotCommand('/highprice', 'Подобрать самые дорогие отели')
            ])
            return
        except exceptions.ConnectionError as e:
            if _tries_counter == retries:
                raise FatalError('Нет связи с сервером Telegram')
            console_message('Нет связи с сервером Telegram. Следующая попытка...')
            time.sleep(3)
            _tries_counter += 1
        except Exception as e:
            console_message(str(e))
            break




