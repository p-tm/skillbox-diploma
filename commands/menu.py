from typing import *
from requests import exceptions
from telebot import telebot, types as tt
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

from classes.user_state import UserState
from config import MAIN_MENU_COMMANDS, MAIN_MENU_BUTTONS
from loader import bot, storage

main_menu_buttons_callback_factory = CallbackData('cmd_id', prefix='cmd_main')


class MainMenuCallbackFilter(AdvancedCustomFilter):
    key = 'filter_main_menu'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter):
        x = config.check(query=call)
        return x

bot.add_custom_filter(MainMenuCallbackFilter())

def keyboard_select_main_cmd() -> telebot.types.InlineKeyboardMarkup:
    """
    Функция:
    -------
    Создаёт виртуальную клавиатуру с кнопками для выбора основной команды

    :return: telebot.types.InlineKeyboardMarkup
        - объект: клавиатура

    """
    buttons = [
        [
            tt.InlineKeyboardButton(
                text=button['caption'],
                callback_data=main_menu_buttons_callback_factory.new(cmd_id=button['id'])
            )
        ]
        for button in MAIN_MENU_BUTTONS
    ]

    return tt.InlineKeyboardMarkup(buttons)


@bot.message_handler(commands=['menu'])
def menu(message: telebot.types.Message) -> None:
    """
    Функция:
    -------
    Обработчик команды "/menu"

    :param message: telebot.types.Message
        - сообщение от пользователя
    :return: None

    """

    user: int = message.chat.id
    chat: int = message.chat.id
    bot.set_state(user_id=user, state=UserState.user_selects_request, chat_id=chat)

    st = storage
    ccc = bot.retrieve_data(user, chat)

    kbrd_select_main_cmd: telebot.types.InlineKeyboardMarkup = keyboard_select_main_cmd()

    try:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите. что Вас интересует:',
            reply_markup=kbrd_select_main_cmd
        )
    except exceptions.ReadTimeout:
        raise

