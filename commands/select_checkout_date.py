"""
Реализация шага по выбору даты выезда

"""
from datetime import datetime

from telebot import telebot

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_min_price import select_min_price
from config import DELETE_OLD_KEYBOARDS
from functions.get_usd import get_usd
from functions.keyboard_input_date import keyboard_input_date
from functions.console_message import console_message
from functions.send_message_helper import send_message_helper
from functions.show_summary import show_summary
from functions.keyboard_input_date import keyboard_input_date, input_date_callback_factory
from functions.reenter_date import reenter_date
from loader import bot
from states import BestdealSubstates, LowpriceSubstates, HighpriceSubstates


def select_checkout_date(message: telebot.types.Message) -> None:
    """
    Выбор даты выезда

    :param message:

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    keyboard: telebot.types.InlineKeyboardMarkup = keyboard_input_date()

    # приглашение
    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=usd.chat,
        text='Выберите дату выезда: __.__.____',
        reply_markup=keyboard
    )

    usd.last_message = msg


def filter_func(call: telebot.types.CallbackQuery) -> bool:
    """
    Функция фильтрации
    Условие: находимся в состоянии SELECT_CHECKOUT_DATE
    Пропускает сообщение от кнопки "Готово"

    :param call: telebot.types.CallbackQuery
    :return: bool: True = фильтр пройдён

    """
    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return False

    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        return usd.substate == LowpriceSubstates.SELECT_CHECKOUT_DATE.value
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        return usd.substate == HighpriceSubstates.SELECT_CHECKOUT_DATE.value
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        return usd.substate == BestdealSubstates.SELECT_CHECKOUT_DATE.value

    return False


@bot.callback_query_handler(
    func=filter_func,
    filter_input_date=input_date_callback_factory.filter(type='enter')
)
def enter_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку "готово"

    :param call:

    """
    faulty_input_message: str = 'Некорректное значение даты. Пожалуйста, введите ещё раз'

    usd: UserStateData = get_usd(message=call.message)
    if usd is None:
        return

    #callback_data: Dict[str, str] = input_date_callback_factory.parse(callback_data=call.data)
    try:
        checkout_date = datetime.strptime(call.message.text[-10:], '%d.%m.%Y')
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
        usd.checkout_date = checkout_date
    except ValueError as e:
        console_message(str(e))
        reenter_date(call.message, str(e))
        return

    more_than_28_message: str = (
        'Количество ночей не должно превышать 28.'
        'Максимально допустимая дата выезда {}'
        ' Пожалуйста, введите ещё раз'
    ).format(usd.max_checkout_date.strftime('%d.%m.%Y'))

    # пересчитываем кол-во ночей и проверяем что оно не более 28
    less_than_28: bool = usd.calculate_nights()
    if not less_than_28:
        console_message(more_than_28_message)
        reenter_date(call.message, more_than_28_message)
        return

    # удаляем клавиатуру
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=usd.chat,
        message_id=call.message.id,
        text='Выберите дату заезда: {}'.format(checkout_date.strftime('%d.%m.%Y'))
    )

    """ переходим к отображению резюме по выбранным опциям """

    # переходим в новое состояние
    if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
        usd.substate = LowpriceSubstates.SHOW_SUMMARY.value
        show_summary(message=call.message)
    elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
        usd.substate = HighpriceSubstates.SHOW_SUMMARY.value
        show_summary(message=call.message)
    elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
        usd.substate = BestdealSubstates.SELECT_MIN_PRICE.value
        select_min_price(message=call.message)


