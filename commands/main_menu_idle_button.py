from typing import *

from telebot import telebot

from loader import bot
from commands.menu import main_menu_buttons_callback_factory
from config import MAIN_MENU_COMMANDS

@bot.callback_query_handler(
    func=None,
    filter_main_menu=main_menu_buttons_callback_factory.filter(cmd_id=str(MAIN_MENU_COMMANDS.NONE.value))
)
# @bot.callback_query_handler(func=None)
def main_menu_idle_button(call: telebot.types.CallbackQuery):
    bot.answer_callback_query(
        callback_query_id=call.id,
        show_alert=True,
        # text='Неизвестная команда.\nОбратитесь к разработчику')
        text='Эта кнопка пока не работает'
    )