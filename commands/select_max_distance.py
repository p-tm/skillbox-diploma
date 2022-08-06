"""
Реализация шага по вводу максимального расстояния

"""
from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from config import (
    BestdealSubstates, DELETE_OLD_KEYBOARDS, HighpriceSubstates, LowpriceSubstates, MAX_DISTANCE
)
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from functions.show_summary import show_summary
from functions.value_valid import value_valid
from loader import bot

def select_max_distance(message: telebot.types.Message) -> None:
    """
    Ввод маскимального расстояния

    :param message: предыдущее сообщение для передачи user и chat

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    max_price_message = 'Введите маскимальное расстояние в км: (минимум {}, максимум {})'.format(
        usd.min_distance,
        MAX_DISTANCE
    )

    # приглашение
    msg: telebot.types.Message = send_message_helper(bot.send_message)(
        chat_id=usd.chat,
        text=max_price_message
    )

    usd.last_message = msg


def filter_func(message: telebot.types.Message) -> bool:
    """
    Фильтр для сообщения в котором вводится маскимальное расстояние

    :param message: сообщение к которому прицеплена клавиатура
    :return: True = сообщение прошло через фильтр

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return False

    if usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        return usd.substate == BestdealSubstates.SELECT_MAX_DISTANCE.value

    return False


@bot.message_handler(content_types=['text'], func=filter_func)
def max_distance_text(message: telebot.types.Message) -> None:
    """
    Обработчик - считывает маскимальное расстояние

    :param message: предыдущее сообщение в чате Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    nan_message: str = 'Необходимо ввести число от {:.1f} до {:.1f}. Введите ещё раз'.format(
        usd.min_distance,
        MAX_DISTANCE
    )
    not_in_range_message: str = nan_message

    # проверяем корректность ввода
    try:
        max_distance: float = float(message.text)
    except ValueError:
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=nan_message
        )
        select_max_distance(message)
        return

    if not value_valid(max_distance, usd.min_distance, MAX_DISTANCE):
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=not_in_range_message
        )
        select_max_distance(message)
        return

    # запоминаем значение
    usd.max_distance = max_distance

    # переходим в новое состояние
    if usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SHOW_SUMMARY.value

    show_summary(message=message)