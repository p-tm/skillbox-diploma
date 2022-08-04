"""
Вывод резюме по выбранным опциям

"""
from telebot import telebot
from typing import Any, Dict

from classes.user_state_data import UserStateData
from config import HighpriceSubstates, LowpriceSubstates
from exceptions.data_unavalible import DataUnavailible
from functions.console_message import console_message
from functions.hotels_per_city import hotels_per_city
from functions.send_message_helper import send_message_helper
from functions.show_results import show_results
from loader import bot, countries



def show_summary(message: telebot.types.Message) -> None:
    """
    Формирует сообщение с итоговой суммой выбранных опций

    :param message: предыдущее сообщение в чате Telegram

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    user_state: str = bot.get_state(user_id=user, chat_id=chat).split(':')[1]

    data: Dict[str, Any]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        summary_message: str = data['usd'].summary()

        # country_key = data['usd'].selected_country_id
        # city_key = data['usd'].selected_city_id
        #
        # resume_message: str = (
        #     'Итак, Ваши критерии поиска:\n\n'
        #     '<i>Страна:</i> {}\n'
        #     '<i>Город:</i> {}\n'
        #     '<i>Дата заезда:</i> {}\n'
        #     '<i>Дата выезда:</i> {}\n'
        #     '<i>Количество ночей:</i> {}\n'
        #     '<i>Количество отелей:</i> {}\n'
        #     '<i>Показывать фото:</i> {}'
        # )
        #
        # out: str = resume_message.format(
        #     countries[country_key].nicename,
        #     countries[country_key].cities[city_key].name,
        #     data['usd'].checkin_date.strftime('%d.%m.%Y'),
        #     data['usd'].checkout_date.strftime('%d.%m.%Y'),
        #     data['usd'].nights,
        #     data['usd'].hotels_amount,
        #     'Да' if data['usd'].photo_required else 'Нет'
        # )
        #
        # if data['usd'].photo_required:
        #     resume_message += '\n<i>Количество фото:</i> {}'
        #
        #     out: str = resume_message.format(
        #         countries[country_key].nicename,
        #         countries[country_key].cities[city_key].name,
        #         data['usd'].checkin_date.strftime('%d.%m.%Y'),
        #         data['usd'].checkout_date.strftime('%d.%m.%Y'),
        #         data['usd'].nights,
        #         data['usd'].hotels_amount,
        #         'Да' if data['usd'].photo_required else 'Нет',
        #         data['usd'].photos_amount
        #     )

    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=summary_message,
        parse_mode='HTML'
    )

    data: Dict[str, UserStateData] # TODO исправить везде
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        data['usd'].last_message = msg

    """ переходим к запросу информации об отелях """

    # переходим в новое состояние
    data: Dict[str, Any]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        if user_state == 'user_lowprice_in_progress':
            data['usd'].substate = LowpriceSubstates.REQUEST_HOTELS.value
        elif user_state == 'user_highprice_in_progress':
            data['usd'].substate = HighpriceSubstates.REQUEST_HOTELS.value


    please_wait_message: str = 'Пожалуста подождите. Выполнятеся запрос к удалённому серверу.'

    # просим подождать
    send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=please_wait_message
    )
    # запрашиваем список отелей (удалённый запрос)
    try:
        hotels_per_city(message)
    except DataUnavailible as e:
        console_message('Не могу получить список отелей.' + str(e))
        send_message_helper(bot.send_message, retries=3)(
            user_id=user,
            chat_id=chat,
            text="🚫 Не могу получить список отелей."
         )

    """ переходим к отображению информации об отелях """

    # переходим в новое состояние
    data: Dict[str, Any]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        if user_state == 'user_lowprice_in_progress':
            data['usd'].substate = LowpriceSubstates.SHOW_RESULTS.value
        elif user_state == 'user_highprice_in_progress':
            data['usd'].substate = HighpriceSubstates.SHOW_RESULTS.value

    show_results(message)
