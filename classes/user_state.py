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
    user_bestdeal_in_progress = State()
    user_history_in_progress = State()

    USER_NONE = 'user_none'
    USER_STARTED_BOT = 'user_started_bot'
    USER_SELECTS_REQUEST = 'user_selects_request'
    USER_LOWPRICE_IN_PROGRESS = 'user_lowprice_in_progress'
    USER_HIGHPRICE_IN_PROGRESS = 'user_highprice_in_progress'
    USER_BESTDEAL_IN_PROGRESS = 'user_bestdeal_in_progress'
    USER_HISTORY_IN_PROGRESS = 'user_history_in_progress'
