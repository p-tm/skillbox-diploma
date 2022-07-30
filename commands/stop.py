from telebot import telebot

from classes.user_state import UserState
from commands.menu import menu
from config import DELETE_OLD_KEYBOARDS
from functions.send_message_helper import send_message_helper
from loader import bot

@bot.message_handler(commands=['stop'])
def stop(message: telebot.types.Message) -> None:
    """
    Прерывание выполнения команды

    :param message: предыдущее сообщение в чате Telegram

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    # здесь нужно удалить два сообщений
    # if DELETE_OLD_KEYBOARDS:
    #     with bot.retrieve_data(user, chat) as data:
    #         header_msg: telebot.types.Message = data['usd'].header_message
    #         data['usd'].header_message = None
    #         msg_to_delete: telebot.types.Message = data['usd'].message_to_delete
    #         data['usd'].message_to_delete = None
    #         data['usd'].reinit_keyboard()
    #         data['usd'].substate = 0
    #
    #     if header_msg is not None:
    #         send_message_helper(bot.delete_message, retries=3)(
    #             chat_id=chat,
    #             message_id=header_msg.id
    #         )
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=msg_to_delete.id
    #     )
        # send_message_helper(bot.delete_message, retries=3)(
        #     chat_id=chat,
        #     message_id=message.id
        # )

    # сбрасываем все значимые состояния
    bot.set_state(user_id=user, state=UserState.user_started_bot, chat_id=chat)

    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        data['usd'].reinit_keyboard()
        data['usd'].substate = 0

    menu(message=message)


