"""
Команда "/history"

"""
from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.menu import menu, main_menu_buttons_callback_factory
from config import DELETE_OLD_KEYBOARDS, MainMenuCommands
from functions.get_usd import get_usd
from functions.print_results_data import print_results_data
from functions.send_message_helper import send_message_helper
from loader import bot

@bot.message_handler(
    state=[UserState.user_selects_request],
    commands=['history']
)
def history_text(message: telebot.types.Message) -> None:
    """
    Обработчик команды '/lowprice' если команда введена текстом

    :param message: предыдущее сообщение в чате Telegram

    """
    history(message)

@bot.callback_query_handler(
    func=None,
    state=[UserState.user_selects_request],
    filter_main_menu=main_menu_buttons_callback_factory.filter(cmd_id=str(MainMenuCommands.HISTORY.value))
)
def history_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик команды '/lowprice' если команда введена кнопкой

    :param call: сообщение от кнопки

    """
    history(call.message)

def history(message: telebot.types.Message) -> None:
    """
    Основной функционал команды '/history'

    :param message: предыдущее сообщение из чата Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    bot.set_state(user_id=usd.user, chat_id=usd.chat, state=UserState.user_history_in_progress)

    history_started_message: str = 'История запросов пользователя <b>{} {}</b>'.format(
        message.chat.first_name,
        message.chat.last_name
    )
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=history_started_message,
        parse_mode='HTML'
    )

    """  логгирование """
    usd.history.add_rec('UCMD', '/history')

    for rec in usd.history.get_from_file():

        if rec.type == 'UCMD':

            text: str = '{} {}'.format(rec.dt, rec.content)
            send_message_helper(bot.send_message, retries=3)(
                chat_id=usd.chat,
                text=text
            )

        elif rec.type == 'RSLT':

            usd: UserStateData = rec.usd
            summary_message: str = usd.summary(history=True)
            send_message_helper(bot.send_message, retries=3)(
                chat_id=usd.chat,
                text=summary_message,
                parse_mode='HTML'
            )
            suitable_hotels_message: str = 'Список подходящих отелей:'
            send_message_helper(bot.send_message, retries=3)(
                chat_id=usd.chat,
                text=suitable_hotels_message
            )
            print_results_data(message, usd)

    """ на этом процесс закончен, выдаём главное меню для новго выбора """

    horiz_delimiter = '----------------------------------------------------------------------'

    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=horiz_delimiter
    )
    menu(message=message)
