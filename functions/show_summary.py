from telebot import telebot

from functions.send_message_helper import send_message_helper
from loader import bot, countries



def show_summary(message: telebot.types.Message) -> None:
    """
    Формирует сообщение с итоговой суммой выбранных опций

    :param message: предыдущее сообщение в чате Telegram

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    with bot.retrieve_data(user, chat) as data:

        country_key = data['usd'].selected_country_id
        city_key = data['usd'].selected_city_id

        out: str = 'Итак, Ваши критерии поиска:\n\n' \
              '<i>Страна:</i> {}\n' \
              '<i>Город:</i> {}\n' \
              '<i>Дата заезда:</i> {}\n' \
              '<i>Дата выезда:</i> {}\n' \
              '<i>Количество ночей:</i> {}\n' \
              '<i>Количество отелей:</i> {}\n'.format(
            countries[country_key].nicename,
            countries[country_key].cities[city_key].name,
            data['usd'].checkin_date.strftime('%d.%m.%Y'),
            data['usd'].checkout_date.strftime('%d.%m.%Y'),
            'заглушка',
            data['usd'].hotels_amount
        )

    msg: telebot.types.Message = send_message_helper(bot.send_message, retries=3)(
        chat_id=chat,
        text=out,
        parse_mode='HTML'
    )

    with bot.retrieve_data(user, chat) as data:
        data['usd'].last_message = msg


