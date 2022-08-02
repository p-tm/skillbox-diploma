from telebot import telebot
from typing import *

from classes.user_state_data import UserStateData
from commands.select_checkin_date import select_checkin_date
from config import DELETE_OLD_KEYBOARDS, LOWPRICE_SUBSTATES, MAX_PHOTOS_AMOUNT
from functions.send_message_helper import send_message_helper
from functions.value_valid import value_valid
from loader import bot


def select_photos_amount(message: telebot.types.Message) -> None:
    """
    Выбор количества фотографий

    :param message: предыдущее сообщение для передачи user и chat

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    # приглашение
    msg: telebot.types.Message  = send_message_helper(bot.send_message)(
        chat_id=chat,
        text='Введите количество фотографий:'
    )

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user, chat) as data:
        # data['usd'].message_to_delete = msg
        data['usd'].last_message = msg


def filter_func(message: telebot.types.Message) -> bool:
    """
    Фильтр для сообщения в котором вводится кол-во фотографий

    :param message: сообщение к которому прицеплена клавиатура
    :return: True если сообщение прошло через фильтр

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        return data['usd'].substate == LOWPRICE_SUBSTATES.SELECT_PHOTOS_AMOUNT.value


# @bot.message_handler(is_digit=True, content_types=['text'], func=filter_func)
@bot.message_handler(content_types=['text'], func=filter_func)
def photos_amount_text(message: telebot.types.Message) -> None:
    """
    Обработчик - считывает требуемое количество фотографий

    :param message: предыдущее сообщение в чате Telegram

    """
    nan_message: str = 'Необходимо ввести целое число от 1 до {}. Введите ещё раз'.format(MAX_PHOTOS_AMOUNT)
    not_in_range_message: str = nan_message

    user: int = message.chat.id
    chat: int = message.chat.id

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

    # запоминаем требуемое количество картинок
    with bot.retrieve_data(user, chat) as data:
        try:
            photos_amount = int(message.text)
        except ValueError:
            send_message_helper(bot.send_message, retries=3)(
                chat_id=chat,
                text=nan_message
            )
            select_photos_amount(message)
            return

        if not value_valid(photos_amount, 1, MAX_PHOTOS_AMOUNT):
            send_message_helper(bot.send_message, retries=3)(
                chat_id=chat,
                text=not_in_range_message
            )
            select_photos_amount(message)
            return

        data['usd'].photos_amount = photos_amount

    """ переходим к выбору даты заезда """

    # переходим в новое состояние
    with bot.retrieve_data(user, chat) as data:
        data['usd'].substate = LOWPRICE_SUBSTATES.SELECT_CHECKIN_DATE.value

    select_checkin_date(message=message)
