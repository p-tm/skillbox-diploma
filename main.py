from loader import bot

from commands.start import start
from commands.menu import menu
from commands.main_menu_idle_button import main_menu_idle_button
from commands.lowprice import lowprice_text, lowprice_button
from commands.select_country import select_country


if __name__ == '__main__':

    # bot.add_custom_filter(MainMenuCallbackFilter())

    bot.infinity_polling()
