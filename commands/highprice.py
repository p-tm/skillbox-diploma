"""
Команда "/highprice"

"""
from telebot import telebot
from typing import Any, Dict

from classes.user_state import UserState
from commands.select_country import select_country
from config import HighpriceSubstates, MainMenuCommands
from functions.send_message_helper import send_message_helper
from loader import bot, main_menu_buttons_callback_factory

@bot.message_handler(
    state=[UserState.user_selects_request],
    commands=['highprice']
)
def highprice_text(message: telebot.types.Message) -> None:
    """
    Обработчик команды '/highprice' если команда введена текстом

    :param message: предыдущее сообщение в чате Telegram

    """
    highprice(message=message)

@bot.callback_query_handler(
    func=None,
    state=[UserState.user_selects_request],
    filter_main_menu=main_menu_buttons_callback_factory.filter(cmd_id=str(MainMenuCommands.HIGHPRICE.value))
)
def highprice_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик команды '/highprice' если команда введена кнопкой

    :param call: сообщение от кнопки

    """
    highprice(message=call.message)


def highprice(message: telebot.types.Message) -> None:
    """
    Основной функционал команды '/highprice'

    :param message:

    """
    user: int = message.chat.id
    chat: int = message.chat.id
    bot.set_state(user_id=user, chat_id=chat, state=UserState.user_highprice_in_progress)

    highprice_started_message: str = 'Итак, подибраем самые дорогие отели'
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=highprice_started_message
    )

    data: Dict[str, Any]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        data['usd'].header_message = msg
        data['usd'].substate = HighpriceSubstates.SELECT_COUNTRY.value

    data['usd'].history.add_rec('UCMD', '/highprice')

    select_country(message=message)