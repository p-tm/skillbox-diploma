"""
Описание функции

"""
import pickle

from telebot import telebot

from classes.hotel import Hotel
from classes.user_state_data import UserStateData
from commands.menu import menu
from config import LowpriceSubstates, SUBSTATE_NONE, STORE_DATA_LOCALLY, LOCAL_STORAGE
from functions.cashfile import cashfile
from functions.get_usd import get_usd
from functions.print_results_data import print_results_data
from functions.send_message_helper import send_message_helper
from loader import bot, countries


def show_results(message: telebot.types.Message) -> None:
    """
    Выводит результаты поиска отелей

    :param message: предыдущее сообщение в чате Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    nothing_found_message: str = 'По Вашему запросу ничего не найдено'

    if usd.hotels.size == 0:

        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=nothing_found_message
        )

    else:

        x: int = usd.hotels.size % 10
        found: str = ''
        end_word: str = ''
        if x == 0 or x in range(5,20) or x in range(25,30):
            found = 'найдено'
            end_word = 'отелей'
        elif x == 1:
            found = 'найден'
            end_word = 'отель'
        elif x in (2, 3, 4):
            found = 'найдено'
            end_word = 'отеля'

        suitable_hotels_message: str = 'Список подходящих отелей:'
        suitable_amount_message: str = 'По Вашему запросу {} {} {}'.format(found, usd.hotels.size, end_word)

        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=suitable_hotels_message
        )
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text=suitable_amount_message
        )

        print_results_data(message=message, usd=usd)

    """ логгирование - записываем результаты поиска """
    bobj: 'binary_object' = pickle.dumps(usd)
    usd.history.add_rec('RSLT', bobj.__str__())

    """ записываем все данные из countries """
    if STORE_DATA_LOCALLY:
        f_name: str = cashfile(LOCAL_STORAGE)
        bobj: 'binary_object' = pickle.dumps(countries)
        with open(f_name, mode='w', encoding='utf-8', errors='replace') as f:
            f.write(bobj.__str__())

    """ на этом процесс закончен, выдаём главное меню для новго выбора """

    horiz_delimiter = '----------------------------------------------------------------------'

    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=horiz_delimiter
    )

    menu(message=message)
