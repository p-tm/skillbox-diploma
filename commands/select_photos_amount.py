from telebot import telebot

from commands.select_checkin_date import select_checkin_date
from config import DELETE_OLD_KEYBOARDS, LOWPRICE_SUBSTATES
from functions.send_message_helper import send_message_helper
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

    with bot.retrieve_data(user, chat) as data:
        # data['usd'].message_to_delete = msg
        data['usd'].last_message = msg

def filter_func(message: telebot.types.Message) -> bool:
    """
    Фильтр для сообщения в котором вводится кол-во фотографий

    :param message: сообщение к которому прицеплена клавиатура
    :return: True = сообщение прошло через фильтр

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    with bot.retrieve_data(user, chat) as data:
        return data['usd'].substate == LOWPRICE_SUBSTATES.SELECT_PHOTOS_AMOUNT.value


@bot.message_handler(is_digit=True, content_types=['text'], func=filter_func)
def photos_amount_text(message: telebot.types.Message) -> None:
    """
    Обработчик

    :param message:

    """
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
        data['usd'].photos_amount = int(message.text)

    """ переходим к выбору даты заезда """

    # переходим в новое состояние
    with bot.retrieve_data(user, chat) as data:
        data['usd'].substate = LOWPRICE_SUBSTATES.SELECT_CHECKIN_DATE.value

    select_checkin_date(message=message)