from telebot.handler_backends import State, StatesGroup

class UserState(StatesGroup):
    user_started_bot = State()
    user_selects_request = State()
    user_lowprice_in_progress = State()