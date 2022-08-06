"""
Команда "/bestdeal"

"""
from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.menu import main_menu_buttons_callback_factory
from commands.select_country import select_country
from config import BestdealSubstates, DELETE_OLD_KEYBOARDS, MainMenuCommands
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from loader import bot


@bot.message_handler(
    state=[UserState.user_selects_request],
    commands=['bestdeal']
)
def bestdeal_text(message: telebot.types.Message) -> None:
    """
    Обработчик команды '/bestdeal' если команда введена текстом

    :param message: предыдущее сообщение в чате Telegram

    """
    bestdeal(message=message)


@bot.callback_query_handler(
    func=None,
    state=[UserState.user_selects_request],
    filter_main_menu=main_menu_buttons_callback_factory.filter(cmd_id=str(MainMenuCommands.BESTDEAL.value))
)
def bestdeal_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик команды '/bestdeal' если команда введена кнопкой

    :param call: сообщение от кнопки

    """
    bestdeal(message=call.message)


def bestdeal(message: telebot.types.Message) -> None:
    """
    Основной функционал команды '/bestdeal'

    :param message:

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    bot.set_state(user_id=usd.user, chat_id=usd.chat, state=UserState.user_bestdeal_in_progress)

    bestdeal_started_message: str = 'Итак, подибраем отели по цене и расстоянию до центра'
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=bestdeal_started_message
    )

    usd.header_message = msg
    usd.substate = BestdealSubstates.SELECT_COUNTRY.value
    usd.history.add_rec('UCMD', '/bestdeal')

    select_country(message=message)
