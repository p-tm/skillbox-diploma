import sys

from telebot import telebot, TeleBot
from telebot.callback_data import CallbackData
from telebot.custom_filters import StateFilter, IsDigitFilter
from telebot.storage import StateMemoryStorage
from typing import *

from classes.countries import Countries
from classes.is_command_filter import IsCommandFilter
from config import BOT_TOKEN
from exceptions.data_unavalible import DataUnavailible
from exceptions.fatal_error import FatalError
from functions.console_message import console_message
from functions.countries_per_world import countries_per_world
from functions.init_ui import init_ui



countries: Countries = Countries()

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
    init_ui(bot, retries=3)
except FatalError as e:
    console_message('Завершение работы. Не удалось инициализировать бот. ' + str(e))
    sys.exit(4)














