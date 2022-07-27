from loader import bot

from commands.start import start
from commands.menu import menu
from commands.main_menu_idle_button import main_menu_idle_button
from commands.lowprice import lowprice_text, lowprice_button
from commands.select_country import select_country
from functions.console_message import console_message

if __name__ == '__main__':

    ''' сама эта функция ничего не бросает, но внутренние бросают и поймать их нельзя '''
    try:
        bot.infinity_polling()
    except Exception as e:
        console_message(str(e))



