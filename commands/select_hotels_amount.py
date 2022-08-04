"""
Реализация шага по выбору количества отелей

"""
from telebot import telebot
from typing import *

from classes.user_state_data import UserStateData
from commands.select_photo_required import select_photo_required
from config import DELETE_OLD_KEYBOARDS, HighpriceSubstates, LowpriceSubstates, MAX_HOTELS_AMOUNT
from functions.send_message_helper import send_message_helper
from functions.value_valid import value_valid
from loader import bot, storage

def select_hotels_amount(message: telebot.types.Message) -> None:
    """
    Выбор количества отелей

    :param message: предыдущее сообщение для передачи user и chat

    """
    hotels_number_message = 'Введите количество отелей: (максимум {})'.format(MAX_HOTELS_AMOUNT)

    user: int = message.chat.id
    chat: int = message.chat.id

    # приглашение
    msg: telebot.types.Message = send_message_helper(bot.send_message)(
        chat_id=chat,
        text=hotels_number_message
    )

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        # data['usd'].message_to_delete = msg
        data['usd'].last_message = msg


def filter_func(message: telebot.types.Message) -> bool:
    """
    Фильтр для сообщения в котором вводится кол-во отелей

    :param message: сообщение к которому прицеплена клавиатура
    :return: True = сообщение прошло через фильтр

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    check_state: str = bot.get_state(user_id=user, chat_id=chat)
    if check_state is None:
        return False

    user_state: str = check_state.split(':')[1]

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        if user_state == 'user_lowprice_in_progress':
            return data['usd'].substate == LowpriceSubstates.SELECT_HOTELS_AMOUNT.value
        if user_state == 'user_highprice_in_progress':
            return data['usd'].substate == HighpriceSubstates.SELECT_HOTELS_AMOUNT.value

    return False

# @bot.message_handler(is_digit=True, content_types=['text'], func=filter_func)
@bot.message_handler(content_types=['text'], func=filter_func)
def hotels_amount_text(message: telebot.types.Message) -> None:
    """
    Обработчик - считывает количество отелей

    :param message: предыдущее сообщение в чате Telegram

    """
    nan_message: str = 'Необходимо ввести целое число от 1 до {}. Введите ещё раз'.format(MAX_HOTELS_AMOUNT)
    not_in_range_message: str = nan_message

    user: int = message.chat.id
    chat: int = message.chat.id

    user_state: str = bot.get_state(user_id=user, chat_id=chat).split(':')[1]

    # здесь нужно удалить два сообщений
    # if DELETE_OLD_KEYBOARDS:
    #     with bot.retrieve_data(user, chat) as data:
    #         msg_to_delete: telebot.types.Message = data['usd'].message_to_delete
    #         data['usd'].message_to_delete = None
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=msg_to_delete.id
    #     )
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=message.id
    #     )

    # запоминаем число отелей
    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        try:
            hotels_amount: int = int(message.text)
        except ValueError:
            send_message_helper(bot.send_message, retries=3)(
                chat_id=chat,
                text=nan_message
            )
            select_hotels_amount(message)
            return

        if not value_valid(hotels_amount, 1, MAX_HOTELS_AMOUNT):
            send_message_helper(bot.send_message, retries=3)(
                chat_id=chat,
                text=not_in_range_message
            )
            select_hotels_amount(message)
            return

        data['usd'].hotels_amount = hotels_amount

    """ переходим к выбору нужны ли картинки """

    # переходим в новое состояние
    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        if user_state == 'user_lowprice_in_progress':
            data['usd'].substate = LowpriceSubstates.SELECT_PHOTO_REQUIRED.value
        elif user_state == 'user_highprice_in_progress':
            data['usd'].substate = HighpriceSubstates.SELECT_PHOTO_REQUIRED.value

    select_photo_required(message=message)
