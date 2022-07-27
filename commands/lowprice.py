from classes.user_state_data import UserStateData

from telebot import telebot
from telebot.storage.base_storage import StateContext

from config import MAIN_MENU_COMMANDS, LOWPRICE_SUBSTATES
from loader import bot, storage

from commands.menu import main_menu_buttons_callback_factory
from commands.select_country import select_country

from classes.user_state import UserState


@bot.message_handler(commands=['lowprice'])
def lowprice_text(message: telebot.types.Message) -> None:
    """
    Функция:
    -------
    Обрабочик команды '/lowprice' если команда введена текстом

    :param message: telebot.types.Message
        - сообщение от пользователя
    :return: None

    """
    user: int = message.chat.id
    chat: int = message.chat.id
    bot.set_state(user_id=user, state=UserState.user_lowprice_in_progress, chat_id=chat)

    with bot.retrieve_data(user, chat) as data:
        data['usd'].substate = LOWPRICE_SUBSTATES.SELECT_COUNTRY.value

    select_country(
        message=message,
        bot=bot
    )


@bot.callback_query_handler(
    func=None,
    filter_main_menu=main_menu_buttons_callback_factory.filter(cmd_id=str(MAIN_MENU_COMMANDS.LOWPRICE.value))
)
def lowprice_button(call: telebot.types.CallbackQuery):
    """
    Функция:
    -------
    Обрабочик команды '/lowprice' если команда введена кнопкой

    :param call: telebot.types.CallbackQuery
        - сообщение от кнопки
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id
    bot.set_state(user_id=user, state=UserState.user_lowprice_in_progress, chat_id=chat)

    with bot.retrieve_data(user, chat) as data:
        data['usd'].substate = LOWPRICE_SUBSTATES.SELECT_COUNTRY.value

    select_country(
        message=call.message,
        bot=bot
    )




