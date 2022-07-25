import sys

from typing import *

from telebot import telebot
from telebot import types as tt
from telebot.storage import StateMemoryStorage

from classes.countries import Countries

from config import BOT_TOKEN

from functions.countries_per_world import countries_per_world
from functions.init_ui import init_ui

countries = Countries()

try:
    countries_per_world(countries)
except Exception as e:
    print(e)
    sys.exit(1)

storage = StateMemoryStorage()

bot: telebot.TeleBot = telebot.TeleBot(
    token=BOT_TOKEN,
    state_storage=storage
)

init_ui(bot)


















