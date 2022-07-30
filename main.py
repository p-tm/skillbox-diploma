from loader import bot

from commands.main_menu_idle_button import main_menu_idle_button
from commands.start import start
from commands.stop import stop
from commands.lowprice import lowprice
from commands.unexpected_command import unexpected_command
from functions.console_message import console_message

if __name__ == '__main__':

    ''' сама эта функция ничего не бросает, но внутренние бросают и поймать их нельзя '''
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        console_message(str(e))



