"""
Описание функции

"""
from telebot import telebot
from typing import Any, Dict, Optional

from classes.user_state_data import UserStateData
from loader import bot


def get_usd(message: telebot.types.Message) -> Optional[UserStateData]:
    """
    Опеределяет, какой пользователь отправил сообщение
    Вытаскивает данные этого ползователя

    :param message: предыдущее сообщение чата Telegram
    :return: данные конкретного пользователя

    """
    user: int = message.chat.id
    chat: int = message.chat.id

    check_state: str = bot.get_state(user_id=user, chat_id=chat)
    if check_state is None:
        return None

    user_state: str = check_state.split(':')[1]

    data: Dict[str, Any]
    with bot.retrieve_data(user_id=user, chat_id=chat) as data:
        data['usd'].user = user
        data['usd'].chat = chat
        data['usd'].state = user_state
        return data['usd']
