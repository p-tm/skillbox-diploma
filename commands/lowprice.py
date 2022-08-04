"""
Команда "/lowprice"

"""
from telebot import telebot
from typing import Any, Dict

from classes.user_state import UserState
from commands.menu import main_menu_buttons_callback_factory
from commands.select_country import select_country
from config import DELETE_OLD_KEYBOARDS, MainMenuCommands, LowpriceSubstates
from functions.send_message_helper import send_message_helper
from loader import bot


@bot.message_handler(
    state=[UserState.user_selects_request],
    commands=['lowprice']
)
def lowprice_text(message: telebot.types.Message) -> None:
    """
    Обработчик команды '/lowprice' если команда введена текстом

    :param message: предыдущее сообщение в чате Telegram

    """
    lowprice(message=message)


@bot.callback_query_handler(
    func=None,
    state=[UserState.user_selects_request],
    filter_main_menu=main_menu_buttons_callback_factory.filter(cmd_id=str(MainMenuCommands.LOWPRICE.value))
)
def lowprice_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик команды '/lowprice' если команда введена кнопкой

    :param call: сообщение от кнопки

    """
    lowprice(message=call.message)


def lowprice(message: telebot.types.Message) -> None:
    """
    Основной функционал команды '/lowprice'

    :param message:

    """
    user: int = message.chat.id
    chat: int = message.chat.id
    bot.set_state(user_id=user, chat_id=chat, state=UserState.user_lowprice_in_progress)

    lowprice_started_message: str = 'Итак, подибраем самые дешёвые отели'
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=lowprice_started_message
    )

    data: Dict[str, Any]
    with bot.retrieve_data(user, chat) as data:
        data['usd'].header_message = msg
        data['usd'].substate = LowpriceSubstates.SELECT_COUNTRY.value

    data['usd'].history.add_rec('UCMD', '/lowprice')

    select_country(message=message)
