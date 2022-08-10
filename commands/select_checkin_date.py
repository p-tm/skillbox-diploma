"""
Реализация шага по выбору даты заезда

"""
from datetime import datetime

from telebot import telebot
from typing import Dict

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_checkout_date import select_checkout_date
from config import DELETE_OLD_KEYBOARDS
from functions.get_usd import get_usd
from functions.keyboard_input_date import keyboard_input_date
from functions.console_message import console_message
from functions.send_message_helper import send_message_helper
from functions.keyboard_input_date import keyboard_input_date, input_date_callback_factory
from functions.reenter_date import reenter_date
from loader import bot
from states import BestdealSubstates, LowpriceSubstates, HighpriceSubstates


def select_checkin_date(message: telebot.types.Message) -> None:
    """
    Выбор даты заезда

    :param message:

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    keyboard: telebot.types.InlineKeyboardMarkup = keyboard_input_date()

    # приглашение
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text='Выберите дату заезда: __.__.____',
        reply_markup=keyboard
    )

    usd.message_to_delete = msg
    usd.last_message = msg


def filter_func(call: telebot.types.CallbackQuery) -> bool:
    """
    Функция фильтрации
    Условие: находимся в состоянии SELECT_CHECKIN_DATE
    Пропускает сообщение от кнопки "Готово"

    :param call: telebot.types.CallbackQuery
    :return: bool: True = фильтр пройдён

    """
    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return False

    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        return usd.substate == LowpriceSubstates.SELECT_CHECKIN_DATE.value
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        return usd.substate == HighpriceSubstates.SELECT_CHECKIN_DATE.value
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        return usd.substate == BestdealSubstates.SELECT_CHECKIN_DATE.value

    return False

@bot.callback_query_handler(
    func=filter_func,
    filter_input_date=input_date_callback_factory.filter(type='enter')
)
def enter_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку "готово"

    :param call: telebot.types.CallbackQuery

    """
    faulty_input_message: str = 'Некорректное значение даты. Пожалуйста, введите ещё раз'

    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return

    #callback_data: Dict[str, str] = input_date_callback_factory.parse(callback_data=call.data)
    try:
        checkin_date = datetime.strptime(call.message.text[-10:], '%d.%m.%Y')
    except ValueError as e:
        console_message(str(e))
        reenter_date(call.message, faulty_input_message)
        return

    # удаляем клавиатуру
    # if DELETE_OLD_KEYBOARDS:
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=call.message.id
    #     )

    try:
        usd.checkin_date = checkin_date
    except ValueError as e:
        console_message(str(e))
        reenter_date(call.message, str(e))
        return

    # удаляем клавиатуру
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=usd.chat,
        message_id=call.message.id,
        text='Выберите дату заезда: {}'.format(checkin_date.strftime('%d.%m.%Y'))
    )

    """ переходим к выбору даты выезда """

    # переходим в новое состояние
    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        usd.substate = LowpriceSubstates.SELECT_CHECKOUT_DATE.value
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        usd.substate = HighpriceSubstates.SELECT_CHECKOUT_DATE.value
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SELECT_CHECKOUT_DATE.value

    select_checkout_date(message=call.message)

