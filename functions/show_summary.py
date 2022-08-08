"""
Описание функции

"""
from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from config import BestdealSubstates, HighpriceSubstates, LowpriceSubstates
from exceptions.data_unavalible import DataUnavailible
from functions.console_message import console_message
from functions.get_usd import get_usd
from functions.hotels_per_city import hotels_per_city
from functions.send_message_helper import send_message_helper
from functions.show_results import show_results
from functions.start_new import start_new
from loader import bot, countries


def show_summary(message: telebot.types.Message) -> None:
    """
    Формирует сообщение с итоговой суммой выбранных опций

    :param message: предыдущее сообщение в чате Telegram

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    summary_message: str = usd.summary()

    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=summary_message,
        parse_mode='HTML'
    )

    usd.last_message = msg

    """ переходим к запросу информации об отелях """

    # переходим в новое состояние
    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        usd.substate = LowpriceSubstates.REQUEST_HOTELS.value
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        usd.substate = HighpriceSubstates.REQUEST_HOTELS.value
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.REQUEST_HOTELS.value

    please_wait_message: str = 'Пожалуйста подождите. Выполняется запрос к удалённому серверу.'

    # просим подождать
    send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text=please_wait_message
    )
    # запрашиваем список отелей (удалённый запрос)
    try:
        hotels_per_city(message)
    except DataUnavailible as e:
        console_message('Не могу получить список отелей.' + str(e))
        send_message_helper(bot.send_message, retries=3)(
            chat_id=usd.chat,
            text="🚫 Не могу получить список отелей."
         )
        start_new(message=message, usd=usd)
        return

    """ переходим к отображению информации об отелях """

    # переходим в новое состояние

    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        usd.substate = LowpriceSubstates.SHOW_RESULTS.value
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        usd.substate = HighpriceSubstates.SHOW_RESULTS.value
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SHOW_RESULTS.value

    show_results(message)
