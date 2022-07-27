import sys

from telebot import telebot, TeleBot
from telebot.storage import StateMemoryStorage
from typing import *

from classes.countries import Countries
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

# doesn't throw exceptions
bot: TeleBot = TeleBot(token=BOT_TOKEN, state_storage=storage)

try:
    init_ui(bot, retries=3)
except FatalError as e:
    console_message('Завершение работы. Не удалось инициализировать бот. ' + str(e))
    sys.exit(4)




















