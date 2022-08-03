from enum import Enum

BOT_TOKEN = '5547620893:AAHaqK42H3J52nvX2MjNeBR4su3APKt9Olc' # токен бота (генерирует @BotFather)
FOLDER_REUSABLE = 'reusable'    # пака в которой лежат файлы с кэшированной информацией
MAX_KEYS_PER_KEYBOARD = 30      # количество кнопок на частичной клавиатуре
DELETE_OLD_KEYBOARDS = True     # True = удалять предыдущую частичную клавиатуру
MAX_HOTELS_AMOUNT = 20          # максимальное количество отелей (сервер может отдать максимум 25)
MAX_PHOTOS_AMOUNT = 5            # сервер отдаёт сразу всё, поэтому ограничение - надо проверять, что пришло с сервера
GET_HOTELS_FROM_SERVER = False

COUNTRIES_API_HEADERS = {
    "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
    "X-RapidAPI-Host": "country-list5.p.rapidapi.com"
}
CITIES_API_HEADERS = {
    "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
    "X-RapidAPI-Host": "city-list.p.rapidapi.com"
}
HOTELS_API_HEADERS = {
    "X-RapidAPI-Key": "fba64e5cf9msh04aa44d741bf7c4p107cf8jsn92e55fbb6b9f",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


class YES_NO(Enum):
    """ Для реализации клавиатуры с кнопками "да/нет" """
    NO = 1
    YES = 2


class MAIN_MENU_COMMANDS(Enum):
    """ Числовые идентификаторы команд для главного меню """
    NONE = 0        # нет команды
    START = 1       # /start
    LOWPRICE = 2    # /lowprice
    HIGHPRICE = 3   # /highprice
    BESTDEAL = 4    # /bestdeal
    STOP = 5        # /stop
    HISTORY = 6     # /history
    HELP = 7        # /help


""" шаблоны для кнопок главного меню """
MAIN_MENU_BUTTONS = [
    {'id': MAIN_MENU_COMMANDS.LOWPRICE.value, 'caption': '✨  Подобрать самые дешёвые отели'},
    {'id': MAIN_MENU_COMMANDS.NONE.value, 'caption': '💲  Подобрать самые дорогие отели'},
    {'id': MAIN_MENU_COMMANDS.NONE.value, 'caption': '👍  Подобрать самые подходящие отели'},
    {'id': MAIN_MENU_COMMANDS.HISTORY.value, 'caption': '📜  Посмотреть историю поиска'},
    {'id': MAIN_MENU_COMMANDS.NONE.value, 'caption': 'ℹ  Получить справку о работе с ботом'}
]


class LOWPRICE_SUBSTATES(Enum):
    """ Числовые идентификаторы состояний при выполнении "основной" команды /lowprice """
    NONE = 0                    # нет
    SELECT_COUNTRY = 1          # пользователь выбирает страну
    SELECT_CITY = 2             # пользователь выбирает город
    SELECT_HOTELS_AMOUNT = 3    # пользователь выбирает количество отелей
    SELECT_PHOTO_REQUIRED = 4   # пользователь выбирает нужно ли фото
    SELECT_PHOTOS_AMOUNT = 5    # пользователь выбирает количество фото
    SELECT_CHECKIN_DATE = 6     # пользователь выбирает дату заезда
    SELECT_CHECKOUT_DATE = 7    # пользователь выбирает дату выезда
    SHOW_SUMMARY = 8            # выводим резюме по выбранным опциям
    REQUEST_HOTELS = 9          # запрашиваем отели
    SHOW_RESULTS = 10           # выводим результаты запроса
