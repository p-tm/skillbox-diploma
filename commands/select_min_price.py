"""
Реализация шага по вводу минимальной цены

"""
from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_max_price import select_max_price
from config import DELETE_OLD_KEYBOARDS, MAX_HOTELS_AMOUNT, MAX_PRICE
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from functions.value_valid import value_valid
from loader import bot
from states import BestdealSubstates, LowpriceSubstates, HighpriceSubstates


def select_min_price(message: telebot.types.Message) -> None:
    """
    Ввод минимальной стоимости

    :param message: предыдущее сообщение для передачи user и chat

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    min_price_message = 'Введите минимальную цену за ночь в USD: (максимум {})'.format(MAX_PRICE)

    # приглашение
    msg: telebot.types.Message = send_message_helper(bot.send_message)(
        chat_id=usd.chat,
        text=min_price_message
    )

    usd.last_message = msg


def filter_func(message: telebot.types.Message) -> bool:
    """
    Фильтр для сообщения в котором вводится минимальная стоимость

    :param message: сообщение к которому прицеплена клавиатура
    :return: True = сообщение прошло через фильтр

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return False

    if usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        return usd.substate == BestdealSubstates.SELECT_MIN_PRICE.value

    return False


@bot.message_handler(content_types=['text'], func=filter_func)
def min_price_text(message: telebot.types.Message) -> None:
    """
    Обработчик - считывает минимальную стоимость

    :param message: предыдущее сообщение в чате Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    nan_message: str = 'Необходимо ввести целое число от 0 до {}. Введите ещё раз'.format(MAX_PRICE)
    not_in_range_message: str = nan_message

    # проверяем корректность ввода
    try:
        min_price: int = int(message.text)
    except ValueError:
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=nan_message
        )
        select_min_price(message)
        return

    if not value_valid(min_price, 0, MAX_PRICE):
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=not_in_range_message
        )
        select_min_price(message)
        return

    # запоминаем значение
    usd.min_price = min_price

    # переходим в новое состояние
    if usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SELECT_MAX_PRICE.value

    select_max_price(message=message)