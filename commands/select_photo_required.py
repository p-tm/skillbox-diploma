"""
Реализация шага по выбору нужны ли фото

"""
from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter
from typing import Any, Dict, List

from classes.user_state import UserState
from classes.user_state_data import UserStateData
from commands.select_checkin_date import select_checkin_date
from commands.select_photos_amount import select_photos_amount
from config import DELETE_OLD_KEYBOARDS
from functions.get_usd import get_usd
from functions.send_message_helper import send_message_helper
from loader import bot, yesno_buttons_callback_factory
from states import BestdealSubstates, LowpriceSubstates, HighpriceSubstates, YesNo

# yesno_buttons_callback_factory = CallbackData('cmd_id', prefix='yes_no')


class YesNoCallbackFilter(AdvancedCustomFilter):
    """
    Фильтрация callback_data - выделяем данные, которые относятся к клавиатуре да/нет

    """
    key = 'filter_select_yes_no'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter) -> bool:
        """
        Функция фильтрации

        """
        usd: UserStateData = get_usd(message=call.message)
        if usd is None:
            return False

        is_photo_required: bool = False
        if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
            is_photo_required = usd.substate == LowpriceSubstates.SELECT_PHOTO_REQUIRED.value
        elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
            is_photo_required = usd.substate == HighpriceSubstates.SELECT_PHOTO_REQUIRED.value
        elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
            is_photo_required = usd.substate == BestdealSubstates.SELECT_PHOTO_REQUIRED.value

        return is_photo_required and config.check(query=call)


bot.add_custom_filter(YesNoCallbackFilter())


def keyboard_yes_no() -> telebot.types.InlineKeyboardMarkup:

    buttons: List[List[telebot.types.InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text='✔️Да',
                callback_data=yesno_buttons_callback_factory.new(cmd_id=YesNo.YES.value)
            ),
            InlineKeyboardButton(
                text='❌ Нет',
                callback_data=yesno_buttons_callback_factory.new(cmd_id=YesNo.NO.value)
            )
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def select_photo_required(message: telebot.types.Message) -> None:
    """
    Выбор - нужны ли картинки

    :param message:

    """
    usd: UserStateData = get_usd(message=message)
    if usd is None:
        return

    keyboard: telebot.types.InlineKeyboardMarkup = keyboard_yes_no()

    msg: telebot.types.Message = send_message_helper(bot.send_message)(
        chat_id=usd.chat,
        text='Нужно ли показывать фото:',
        reply_markup=keyboard
    )

    usd.last_message = msg


@bot.callback_query_handler(
    func=None,
    filter_select_yes_no=yesno_buttons_callback_factory.filter()
)
def photo_required_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку да/нет

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    usd: UserStateData = get_usd(message=call.message)

    callback_data: Dict[str, str] = yesno_buttons_callback_factory.parse(callback_data=call.data)

    # удаляем клавиатуру
    # if DELETE_OLD_KEYBOARDS:
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=call.message.id
    #     )

    photo_required = int(callback_data['cmd_id']) == YesNo.YES.value

    usd.photo_required = True if photo_required else False

    if photo_required:

        """ переходим к выбору количества картинок """
        # переходим в новое состояние
        if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
            usd.substate = LowpriceSubstates.SELECT_PHOTOS_AMOUNT.value
        elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
            usd.substate = HighpriceSubstates.SELECT_PHOTOS_AMOUNT.value
        elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
            usd.substate = BestdealSubstates.SELECT_PHOTOS_AMOUNT.value

        select_photos_amount(message=call.message)

    else:

        """ переходим к выбору даты заезда """
        # переходим в новое состояние
        if usd.state == UserState.USER_LOWPRICE_IN_PROGRESS:
            usd.substate = LowpriceSubstates.SELECT_CHECKIN_DATE.value
        elif usd.state == UserState.USER_HIGHPRICE_IN_PROGRESS:
            usd.substate = HighpriceSubstates.SELECT_CHECKIN_DATE.value
        elif usd.state == UserState.USER_BESTDEAL_IN_PROGRESS:
            usd.substate = BestdealSubstates.SELECT_CHECKIN_DATE.value

        select_checkin_date(message=call.message)
