from typing import *
from requests import exceptions
from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter, StateFilter

from classes.user_state import UserState
from config import MAIN_MENU_COMMANDS, MAIN_MENU_BUTTONS
from functions.send_message_helper import send_message_helper
from loader import bot, storage, main_menu_buttons_callback_factory

#main_menu_buttons_callback_factory = CallbackData('cmd_id', prefix='cmd_main')


class MainMenuCallbackFilter(AdvancedCustomFilter):
    key = 'filter_main_menu'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


bot.add_custom_filter(MainMenuCallbackFilter())


def keyboard_select_main_cmd() -> telebot.types.InlineKeyboardMarkup:
    """
    Создаёт виртуальную клавиатуру с кнопками для выбора основной команды

    :return: клавиатура

    """
    buttons = [
        [
            InlineKeyboardButton(
                text=button['caption'],
                callback_data=main_menu_buttons_callback_factory.new(cmd_id=button['id'])
            )
        ]
        for button in MAIN_MENU_BUTTONS
    ]

    return InlineKeyboardMarkup(buttons)


#@bot.message_handler(commands=['menu'])
def menu(message: telebot.types.Message) -> None:
    """
    Обработчик команды "/menu"

    :param message: telebot.types.Message - сообщение от пользователя
    :return: None

    """
    user: int = message.chat.id
    chat: int = message.chat.id
    bot.set_state(user_id=user, state=UserState.user_selects_request, chat_id=chat)

    kbrd_select_main_cmd: telebot.types.InlineKeyboardMarkup = keyboard_select_main_cmd()

    please_select_message = 'Пожалуйста, выберите. что Вас интересует:'
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=please_select_message,
        reply_markup=kbrd_select_main_cmd
    )

    with bot.retrieve_data(user, chat) as data:
    #    data['usd'].message_to_delete = msg
        data['usd'].last_message = msg





