"""
Основной модуль

"""
import commands
from functions.console_message import console_message
from loader import bot

if __name__ == '__main__':

    """ сама эта функция ничего не бросает, но внутренние бросают и поймать их нельзя """
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        console_message(str(e))
