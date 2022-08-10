"""
Команда "/highprice"

"""
from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_country import select_country
from config import MainMenuCommands
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from loader import bot, main_menu_buttons_callback_factory
from states import HighpriceSubstates


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
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    bot.set_state(user_id=usd.user, chat_id=usd.chat, state=UserState.user_highprice_in_progress)

    highprice_started_message: str = 'Итак, подибраем самые дорогие отели'
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=highprice_started_message
    )

    usd.header_message = msg
    usd.substate = HighpriceSubstates.SELECT_COUNTRY.value
    usd.history.add_rec('UCMD', '/highprice')

    select_country(message=message)
