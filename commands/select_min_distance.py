"""
Реализация шага по вводу минимального расстояния

"""
from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_max_distance import select_max_distance
from config import DELETE_OLD_KEYBOARDS, MAX_DISTANCE
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from functions.value_valid import value_valid
from loader import bot
from states import BestdealSubstates, LowpriceSubstates, HighpriceSubstates

def select_min_distance(message: telebot.types.Message) -> None:
    """
    Ввод минимального расстояния

    :param message: предыдущее сообщение для передачи user и chat

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    min_distance_message = 'Введите минимальное расстояние в км: (максимум {:.1f})'.format(MAX_DISTANCE)

    # приглашение
    msg: telebot.types.Message = send_message_helper(bot.send_message)(
        chat_id=usd.chat,
        text=min_distance_message
    )

    usd.last_message = msg

def filter_func(message: telebot.types.Message) -> bool:
    """
    Фильтр для сообщения в котором вводится минимальное расстояние

    :param message: сообщение к которому прицеплена клавиатура
    :return: True = сообщение прошло через фильтр

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return False

    if usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        return usd.substate == BestdealSubstates.SELECT_MIN_DISTANCE.value

    return False

@bot.message_handler(content_types=['text'], func=filter_func)
def min_distance_text(message: telebot.types.Message) -> None:
    """
    Обработчик - считывает минимальное расстояния

    :param message: предыдущее сообщение в чате Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    nan_message: str = 'Необходимо ввести число от 0.0 до {:.1f}. Введите ещё раз'.format(MAX_DISTANCE)
    not_in_range_message: str = nan_message

    # проверяем корректность ввода
    try:
        min_distance: float = float(message.text)
    except ValueError:
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=nan_message
        )
        select_min_distance(message)
        return

    if not value_valid(min_distance, 0, MAX_DISTANCE):
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=not_in_range_message
        )
        select_min_distance(message)
        return

    # запоминаем значение
    usd.min_distance = min_distance

    # переходим в новое состояние
    if usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SELECT_MAX_DISTANCE.value

    select_max_distance(message=message)


