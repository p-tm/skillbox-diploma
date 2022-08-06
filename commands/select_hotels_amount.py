"""
Реализация шага по выбору количества отелей

"""
from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_photo_required import select_photo_required
from config import BestdealSubstates, DELETE_OLD_KEYBOARDS, HighpriceSubstates, LowpriceSubstates, MAX_HOTELS_AMOUNT
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from functions.value_valid import value_valid
from loader import bot

def select_hotels_amount(message: telebot.types.Message) -> None:
    """
    Выбор количества отелей

    :param message: предыдущее сообщение для передачи user и chat

    """
    hotels_number_message = 'Введите количество отелей: (максимум {})'.format(MAX_HOTELS_AMOUNT)

    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    # приглашение
    msg: telebot.types.Message = send_message_helper(bot.send_message)(
        chat_id=usd.chat,
        text=hotels_number_message
    )

    usd.last_message = msg


def filter_func(message: telebot.types.Message) -> bool:
    """
    Фильтр для сообщения в котором вводится кол-во отелей

    :param message: сообщение к которому прицеплена клавиатура
    :return: True = сообщение прошло через фильтр

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return False

    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        return usd.substate == LowpriceSubstates.SELECT_HOTELS_AMOUNT.value
    if usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        return usd.substate == HighpriceSubstates.SELECT_HOTELS_AMOUNT.value
    if usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        return usd.substate == BestdealSubstates.SELECT_HOTELS_AMOUNT.value

    return False

# @bot.message_handler(is_digit=True, content_types=['text'], func=filter_func)
@bot.message_handler(content_types=['text'], func=filter_func)
def hotels_amount_text(message: telebot.types.Message) -> None:
    """
    Обработчик - считывает количество отелей

    :param message: предыдущее сообщение в чате Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    nan_message: str = 'Необходимо ввести целое число от 1 до {}. Введите ещё раз'.format(MAX_HOTELS_AMOUNT)
    not_in_range_message: str = nan_message

    # запоминаем число отелей
    try:
        hotels_amount: int = int(message.text)
    except ValueError:
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=nan_message
        )
        select_hotels_amount(message)
        return

    if not value_valid(hotels_amount, 1, MAX_HOTELS_AMOUNT):
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=not_in_range_message
        )
        select_hotels_amount(message)
        return

    usd.hotels_amount = hotels_amount

    """ переходим к выбору нужны ли картинки """

    # переходим в новое состояние
    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        usd.substate = LowpriceSubstates.SELECT_PHOTO_REQUIRED.value
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        usd.substate = HighpriceSubstates.SELECT_PHOTO_REQUIRED.value
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SELECT_PHOTO_REQUIRED.value

    select_photo_required(message=message)
