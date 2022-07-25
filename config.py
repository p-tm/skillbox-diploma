from enum import Enum

BOT_TOKEN = '5547620893:AAHaqK42H3J52nvX2MjNeBR4su3APKt9Olc'
FOLDER_REUSABLE = 'reusable'


class MAIN_MENU_COMMANDS(Enum):
    NONE = 0
    START = 1
    LOWPRICE = 2
    HIGHPRICE = 3
    BESTDEAL = 4
    STOP = 5
    HISTORY = 6
    HELP = 7


MAIN_MENU_BUTTONS = [
    {'id': MAIN_MENU_COMMANDS.LOWPRICE.value, 'caption': '✨  Подобрать самые дешёвые отели'},
    {'id': MAIN_MENU_COMMANDS.NONE.value, 'caption': '💲  Подобрать самые дорогие отели'},
    {'id': MAIN_MENU_COMMANDS.NONE.value, 'caption': '👍  Подобрать самые подходящие отели'},
    {'id': MAIN_MENU_COMMANDS.NONE.value, 'caption': '📜  Посмотреть историю поиска'},
    {'id': MAIN_MENU_COMMANDS.NONE.value, 'caption': 'ℹ  Получить справку о работе с ботом'}
]


class LOWPRICE_SUBSTATES(Enum):

    NONE = 0
    SELECT_COUNTRY = 1
    SELECT_CITY = 2
    SELECT_HOTELS_AMOUNT = 3
    SELECT_PHOTO_REQUIRED = 4
    SELECT_PHOTOS_AMOUNT = 5
    SELECT_CHECKIN_DATE = 6
    SELECT_CHECKOUT_DATE = 7
