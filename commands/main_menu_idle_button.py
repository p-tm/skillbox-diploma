"""
Команда от кнопки на которую назначена команда MainMenuCommands.NONE (используется для отладки)

"""
from telebot import telebot

from classes.user_state import UserState
from config import MainMenuCommands
from loader import bot, main_menu_buttons_callback_factory


@bot.callback_query_handler(
    func=None,
    state=[UserState.user_selects_request],
    filter_main_menu=main_menu_buttons_callback_factory.filter(cmd_id=str(MainMenuCommands.NONE.value))
)
def main_menu_idle_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик нажатий "пустых" кнопок главного меню

    :param call: сообщение от кнопки

    """
    bot.answer_callback_query(
        callback_query_id=call.id,
        show_alert=True,
        # text='Неизвестная команда.\nОбратитесь к разработчику')
        text='Эта кнопка пока не работает'
    )