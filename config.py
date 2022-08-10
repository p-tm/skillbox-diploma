"""
Описание конфигурационных данных (констант)

"""
from enum import Enum
from states import MainMenuCommands

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
STORE_DATA_LOCALLY = True       # запоминать все нaкопленные данные в файл
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

""" шаблоны для кнопок главного меню """
MAIN_MENU_BUTTONS = [
    {'id': MainMenuCommands.LOWPRICE.value, 'caption': '✨  Подобрать самые дешёвые отели'},
    {'id': MainMenuCommands.HIGHPRICE.value, 'caption': '💲  Подобрать самые дорогие отели'},
    {'id': MainMenuCommands.BESTDEAL.value, 'caption': '👍  Подобрать по цене и расположению'},
    {'id': MainMenuCommands.HISTORY.value, 'caption': '📜  Посмотреть историю поиска'},
    {'id': MainMenuCommands.HELP.value, 'caption': 'ℹ  Получить справку о работе с ботом'}
]

POPULAR_COUNTRIES = ('US','RU','TR','EG','ES','GR')

