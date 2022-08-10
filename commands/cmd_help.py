"""
Команда "/help"

"""
from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import TextIO, List, Match, Optional, Iterable

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.menu import main_menu_buttons_callback_factory
from config import DELETE_OLD_KEYBOARDS, MainMenuCommands, HELP_SOURCE
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from loader import bot, select_help_callback_factory, help_parser


def keyboard_select_help(help_buttons: List):
    buttons = [
        [InlineKeyboardButton(
            text=val,
            callback_data=select_help_callback_factory.new(cmd_id=val))
        ]
        for val in help_buttons
    ]

    keyboard: telebot.types.InlineKeyboardMarkup = InlineKeyboardMarkup(buttons)
    return keyboard


@bot.message_handler(
    state=[UserState.user_selects_request],
    commands=['help']
)
def help_text(message: telebot.types.Message) -> None:
    """
    Обработчик команды '/help' если команда введена текстом

    :param message: предыдущее сообщение в чате Telegram

    """
    cmd_help(message=message)


@bot.callback_query_handler(
    func=None,
    state=[UserState.user_selects_request],
    filter_main_menu=main_menu_buttons_callback_factory.filter(cmd_id=str(MainMenuCommands.HELP.value))
)
def help_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик команды '/help' если команда введена кнопкой

    :param call: сообщение от кнопки

    """
    cmd_help(message=call.message)


def cmd_help(message: telebot.types.Message) -> None:
    """
    Основной функционал команды '/help'

    :param message: предыдущее сообщение из чата Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    bot.set_state(user_id=usd.user, chat_id=usd.chat, state=UserState.user_help_in_progress)

    help_buttons: List = help_parser.get_help_buttons()

    keyboard: telebot.types.InlineKeyboardMarkup = keyboard_select_help(help_buttons)

    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=help_parser.get_main_page(),
        parse_mode='HTML',
        reply_markup=keyboard
    )

    usd.history.add_rec('UCMD', '/highprice')