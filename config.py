"""
Описание конфигурационных данных (констант)

"""
from enum import Enum

BOT_TOKEN = '5547620893:AAHaqK42H3J52nvX2MjNeBR4su3APKt9Olc' # токен бота (генерирует @BotFather)
FOLDER_REUSABLE = 'reusable'    # пака в которой лежат файлы с кэшированной информацией
MAX_KEYS_PER_KEYBOARD = 30      # количество кнопок на частичной клавиатуре
DELETE_OLD_KEYBOARDS = True     # True = удалять предыдущую частичную клавиатуру
MAX_HOTELS_AMOUNT = 20          # максимальное количество отелей (сервер может отдать максимум 25)
MAX_PHOTOS_AMOUNT = 5           # сервер отдаёт сразу всё, поэтому ограничение - надо проверять,
                                # что пришло с сервера
MAX_PRICE = 1000                # максимальная стоимость 1000$/ночь
MAX_DISTANCE = 20.0             # максимальное расстояние от центра

GET_HOTELS_FROM_SERVER = True   # за данными по отелям обращаться к серверу (не читать данные из файла)
STORE_DATA_LOCALLY = False       # запоминать все нaкопленные данные в файл
                                # чтобы можно было посмотреть историю поиска после перезапуска бота

LOCAL_STORAGE = 'countries.cash'    # файл для хранения накопленных данных
HELP_SOURCE = 'help_source.html'    # содержание хелпа

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


class YesNo(Enum):
    """ Для реализации клавиатуры с кнопками "да/нет" """
    NO = 1
    YES = 2


class MainMenuCommands(Enum):
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
    {'id': MainMenuCommands.LOWPRICE.value, 'caption': '✨  Подобрать самые дешёвые отели'},
    {'id': MainMenuCommands.HIGHPRICE.value, 'caption': '💲  Подобрать самые дорогие отели'},
    {'id': MainMenuCommands.BESTDEAL.value, 'caption': '👍  Подобрать по цене и расположению'},
    {'id': MainMenuCommands.HISTORY.value, 'caption': '📜  Посмотреть историю поиска'},
    {'id': MainMenuCommands.HELP.value, 'caption': 'ℹ  Получить справку о работе с ботом'}
]

SUBSTATE_NONE = 0

class LowpriceSubstates(Enum):
    """ Числовые идентификаторы состояний при выполнении "основной" команды /lowprice """
    SELECT_COUNTRY = 11          # пользователь выбирает страну
    SELECT_CITY = 12             # пользователь выбирает город
    SELECT_HOTELS_AMOUNT = 13    # пользователь выбирает количество отелей
    SELECT_PHOTO_REQUIRED = 14   # пользователь выбирает нужно ли фото
    SELECT_PHOTOS_AMOUNT = 15    # пользователь выбирает количество фото
    SELECT_CHECKIN_DATE = 16     # пользователь выбирает дату заезда
    SELECT_CHECKOUT_DATE = 17    # пользователь выбирает дату выезда
    SHOW_SUMMARY = 18            # выводим резюме по выбранным опциям
    REQUEST_HOTELS = 19          # запрашиваем отели
    SHOW_RESULTS = 20            # выводим результаты запроса


class HighpriceSubstates(Enum):
    """ Числовые идентификаторы состояний при выполнении "основной" команды /highprice """
    SELECT_COUNTRY = 31          # пользователь выбирает страну
    SELECT_CITY = 32             # пользователь выбирает город
    SELECT_HOTELS_AMOUNT = 33    # пользователь выбирает количество отелей
    SELECT_PHOTO_REQUIRED = 34   # пользователь выбирает нужно ли фото
    SELECT_PHOTOS_AMOUNT = 35    # пользователь выбирает количество фото
    SELECT_CHECKIN_DATE = 36     # пользователь выбирает дату заезда
    SELECT_CHECKOUT_DATE = 37    # пользователь выбирает дату выезда
    SHOW_SUMMARY = 38            # выводим резюме по выбранным опциям
    REQUEST_HOTELS = 39          # запрашиваем отели
    SHOW_RESULTS = 40            # выводим результаты запроса

class BestdealSubstates(Enum):
    """ Числовые идентификаторы состояний при выполнении "основной" команды /highprice """
    SELECT_COUNTRY = 51          # пользователь выбирает страну
    SELECT_CITY = 52             # пользователь выбирает город
    SELECT_HOTELS_AMOUNT = 53    # пользователь выбирает количество отелей
    SELECT_PHOTO_REQUIRED = 54   # пользователь выбирает нужно ли фото
    SELECT_PHOTOS_AMOUNT = 55    # пользователь выбирает количество фото
    SELECT_CHECKIN_DATE = 56     # пользователь выбирает дату заезда
    SELECT_CHECKOUT_DATE = 57    # пользователь выбирает дату выезда
    SELECT_MIN_PRICE = 58
    SELECT_MAX_PRICE = 59
    SELECT_MIN_DISTANCE = 60
    SELECT_MAX_DISTANCE = 61
    SHOW_SUMMARY = 62            # выводим резюме по выбранным опциям
    REQUEST_HOTELS = 63          # запрашиваем отели
    SHOW_RESULTS = 64           # выводим результаты запроса

POPULAR_COUNTRIES = ('US','RU','TR','EG','ES','GR')

