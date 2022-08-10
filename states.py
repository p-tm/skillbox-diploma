from enum import Enum

SUBSTATE_NONE = 0   # состояние второго поряда UserStateData.substate

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
    SELECT_MIN_PRICE = 58        # ввод минимальной цены
    SELECT_MAX_PRICE = 59        # ввод маскимальной цены
    SELECT_MIN_DISTANCE = 60     # ввод минимального расстояния до центра
    SELECT_MAX_DISTANCE = 61     # ввод маскимального расстояния до центра
    SHOW_SUMMARY = 62            # выводим резюме по выбранным опциям
    REQUEST_HOTELS = 63          # запрашиваем отели
    SHOW_RESULTS = 64            # выводим результаты запроса
