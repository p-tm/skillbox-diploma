"""
Реализация шага по выбору пункта хелпа

"""
from telebot import telebot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.menu import menu
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from loader import bot, select_help_callback_factory, help_parser


class SelectHelpPageFilter(AdvancedCustomFilter):
    """
    Фильтрация callback_data - выделяем данные, которые относятся к клавиатуре выбора страны

    """
    key = 'filter_select_help_page'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter) -> bool:
        """
        Функция фильтрации - пропускает сообщения от кнопок выбора страны

        :return: True = пропустить сообщение

        """

        usd: UserStateData = get_usd(message=call.message)
        if usd is None:
            return False

        return usd.state == UserState.USER_HELP_IN_PROGRESS and config.check(query=call)


bot.add_custom_filter(SelectHelpPageFilter())

@bot.callback_query_handler(
    func=None,
    state=[UserState.user_help_in_progress],
    filter_select_help_page=select_help_callback_factory.filter()
)
def select_help(call: telebot.types.CallbackQuery) -> None:

    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return

    command: str = select_help_callback_factory.parse(callback_data=call.data)['cmd_id']

    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=help_parser.get_next_page(command),
        parse_mode='HTML'
    )

    """ на этом процесс закончен, выдаём главное меню для новго выбора """

    horiz_delimiter = '----------------------------------------------------------------------'

    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=horiz_delimiter
    )

    menu(message=call.message)




