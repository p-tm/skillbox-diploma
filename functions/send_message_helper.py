import sys
import time
from requests import exceptions
from requests.exceptions import ConnectionError, ReadTimeout
from telebot import telebot
from typing import *

from exceptions.message_timeout import MessageTimeout
from functions.console_message import console_message

def send_message_helper(func: Callable, *, retries: Optional[int] = 1) -> Callable:
    """
    Декоратор - применяется к функции telebot.TeleBot.sendMessage()
    Обрабатывает ошибки функции send_message()

    :param func: Callable - декорируемая функция
    :param retries: Optional[int] - число попыток
    :return: Callable
    :raise:

    """
    def helper(*args, **kwargs) -> telebot.types.Message:
        _tries_counter = 1
        while True:
            try:
                result: telebot.types.Message = func(*args, **kwargs)
                return result
            except (ConnectionError, ReadTimeout):
                if _tries_counter == retries:
                    console_message('Не удалось от править сообщение.')
                    #raise MessageTimeout('Не удалось от править сообщение.')
                    return
                console_message('Не удаётся отправить сообщение. Следующая попытка...')
                time.sleep(3)
                _tries_counter += 1
            except Exception as e:
                console_message(str(e))
                #raise MessageTimeout('Не удалось от править сообщение.')
                return

    return helper



