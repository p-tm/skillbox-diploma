"""
Реализация шага по выбору нужны ли фото

"""
from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter
from typing import Any, Dict, List

from classes.user_state_data import UserStateData
from commands.select_checkin_date import select_checkin_date
from commands.select_photos_amount import select_photos_amount
from config import DELETE_OLD_KEYBOARDS, HighpriceSubstates, LowpriceSubstates, YesNo
from functions.send_message_helper import send_message_helper
from loader import bot, yesno_buttons_callback_factory

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
        user: int = call.message.chat.id
        chat: int = call.message.chat.id

        check_state: str = bot.get_state(user_id=user, chat_id=chat)
        if check_state is None:
            return False

        user_state: str = check_state.split(':')[1]

        data: Dict[str, Any]
        is_photo_required: bool
        with bot.retrieve_data(user_id=user, chat_id=chat) as data:
            if user_state == 'user_lowprice_in_progress':
                is_photo_required = data['usd'].substate == LowpriceSubstates.SELECT_PHOTO_REQUIRED.value
            elif user_state == 'user_highprice_in_progress':
                is_photo_required = data['usd'].substate == HighpriceSubstates.SELECT_PHOTO_REQUIRED.value
            else:
                is_photo_required = False

        return is_photo_required and config.check(query=call)


bot.add_custom_filter(YesNoCallbackFilter())


def keyboard_yes_no() -> telebot.types.InlineKeyboardMarkup:

    buttons: List[List[telebot.types.InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text='✔️Да',
                callback_data=yesno_buttons_callback_factory.new(cmd_id=YesNo.YES.value)),
            InlineKeyboardButton(
                text='❌ Нет',
                callback_data=yesno_buttons_callback_factory.new(cmd_id=YesNo.NO.value))
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def select_photo_required(message: telebot.types.Message) -> None:
    """
    Выбор - нужны ли картинки

    :param message:

    """
    user: int = message.chat.id
    chat: int = message.chat.id
    keyboard: telebot.types.InlineKeyboardMarkup = keyboard_yes_no()

    msg: telebot.types.Message = send_message_helper(bot.send_message)(
        chat_id=chat,
        text='Нужно ли показывать фото:',
        reply_markup=keyboard
    )

    data: Dict[str, UserStateData]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        # data['usd'].message_to_delete = msg
        data['usd'].last_message = msg


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
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    user_state: str = bot.get_state(user_id=user, chat_id=chat).split(':')[1]

    callback_data: Dict[str, str] = yesno_buttons_callback_factory.parse(callback_data=call.data)

    # удаляем клавиатуру
    # if DELETE_OLD_KEYBOARDS:
    #     send_message_helper(bot.delete_message, retries=3)(
    #         chat_id=chat,
    #         message_id=call.message.id
    #     )

    photo_required = int(callback_data['cmd_id']) == YesNo.YES.value

    # запоминаем информацию
    with bot.retrieve_data(user, chat) as data:
        data['usd'].photo_required = True if photo_required else False



    if photo_required:
        """ переходим к выбору количества картинок """
        # переходим в новое состояние
        with bot.retrieve_data(user, chat) as data:
            if user_state == 'user_lowprice_in_progress':
                data['usd'].substate = LowpriceSubstates.SELECT_PHOTOS_AMOUNT.value
            elif user_state == 'user_highprice_in_progress':
                data['usd'].substate = HighpriceSubstates.SELECT_PHOTOS_AMOUNT.value
        select_photos_amount(message=call.message)
    else:
        """ переходим к выбору даты заезда """
        # переходим в новое состояние
        with bot.retrieve_data(user, chat) as data:
            if user_state == 'user_lowprice_in_progress':
                data['usd'].substate = LowpriceSubstates.SELECT_CHECKIN_DATE.value
            elif user_state == 'user_highprice_in_progress':
                data['usd'].substate = HighpriceSubstates.SELECT_CHECKIN_DATE.value
        select_checkin_date(message=call.message)
