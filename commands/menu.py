"""
Главное меню (выбор основной команды)

"""
from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from config import MainMenuCommands, MAIN_MENU_BUTTONS
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from loader import bot, storage, main_menu_buttons_callback_factory
from states import SUBSTATE_NONE

#main_menu_buttons_callback_factory = CallbackData('cmd_id', prefix='cmd_main')


class MainMenuCallbackFilter(AdvancedCustomFilter):
    """
    Фильтр

    """
    key = 'filter_main_menu'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter):
        """
        Функция фильтрации

        :param call:
        :param config:
        :return: True = сообщение прошло через фильтр

        """
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

    :param message: сообщение от пользователя

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    # "исходное" состояние - демонстрируется главное меню
    bot.set_state(user_id=usd.user, state=UserState.user_selects_request, chat_id=usd.chat)
    usd.substate = SUBSTATE_NONE
    usd.reinit_keyboard()

    kbrd_select_main_cmd: telebot.types.InlineKeyboardMarkup = keyboard_select_main_cmd()

    please_select_message: str = 'Пожалуйста, выберите, что Вас интересует:'
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=please_select_message,
        reply_markup=kbrd_select_main_cmd
    )

    usd.last_message = msg
