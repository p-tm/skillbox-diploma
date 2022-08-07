"""
Загрузка

"""
import os
import pickle
import sys

from telebot import TeleBot
from telebot.callback_data import CallbackData
from telebot.custom_filters import StateFilter, IsDigitFilter
from telebot.storage import StateMemoryStorage
from typing import TextIO

from classes.countries import Countries
from classes.help_parser import HelpParser
from config import BOT_TOKEN, STORE_DATA_LOCALLY, LOCAL_STORAGE, HELP_SOURCE
from exceptions.data_unavalible import DataUnavailible
from exceptions.fatal_error import FatalError
from functions.cashfile import cashfile
from functions.console_message import console_message
from functions.countries_per_world import countries_per_world
from functions.init_ui import init_ui


countries: Countries = Countries()
read_from_server: bool = True

if STORE_DATA_LOCALLY:

    f_name: str = cashfile(LOCAL_STORAGE)
    if os.path.exists(f_name):
        f: TextIO
        with open(f_name, mode='r', encoding='utf-8', errors='replace') as f:
            content: str = f.read()
        countries = pickle.loads(eval(content))
        read_from_server = False

if read_from_server:

    try:
        countries_per_world(countries)
    except DataUnavailible as e:
        console_message('Завершение работы. Не удалось получить перечень стран. ' + str(e))
        sys.exit(4)

# doesn't throw exceptions
storage: StateMemoryStorage = StateMemoryStorage()

main_menu_buttons_callback_factory = CallbackData('cmd_id', prefix='cmd_main')
select_country_buttons_callback_factory = CallbackData('cmd_id', prefix='country')
select_city_buttons_callback_factory = CallbackData('cmd_id', prefix='city')
yesno_buttons_callback_factory = CallbackData('cmd_id', prefix='yes_no')
input_date_callback_factory = CallbackData('type', 'content', prefix='date')
select_help_callback_factory = CallbackData('cmd_id', prefix='help')

# doesn't throw exceptions
bot: TeleBot = TeleBot(token=BOT_TOKEN, state_storage=storage)

# message filters
bot.add_custom_filter(StateFilter(bot=bot))
bot.add_custom_filter(IsDigitFilter())
# bot.add_custom_filter(IsCommandFilter()) # TODO по-моему не нужно
# следующие операции не получается вызвать здесь из-за circular reference
# bot.add_custom_filter(MainMenuCallbackFilter())
# bot.add_custom_filter(SelectCountryCallbackFilter())
# bot.add_custom_filter(SelectCityCallbackFilter())
# bot.add_custom_filter(YesNoCallbackFilter())
# bot.add_custom_filter(InputDateCallbackFilter())

try:
    init_ui(retries=3)
except FatalError as e:
    console_message('Завершение работы. Не удалось инициализировать бот. ' + str(e))
    sys.exit(4)

f_name: str = HELP_SOURCE
help_parser = HelpParser(f_name)


