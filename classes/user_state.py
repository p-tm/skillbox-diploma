"""
Описание класса

"""
from telebot.handler_backends import State, StatesGroup

class UserState(StatesGroup):
    """
    Состояния

    """
    user_none = State()
    user_started_bot = State()
    user_selects_request = State()
    user_lowprice_in_progress = State()
    user_highprice_in_progress = State()

    user_history_in_progress = State()