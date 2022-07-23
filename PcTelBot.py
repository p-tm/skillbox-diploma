import os
import copy
import math
from requests import exceptions

from typing import *
from enums import *
from globals import *
from telebot import telebot, TeleBot, types as tt
#from telebot import types as tt
from User import User
from Country import Country
from City import City
from Hotel import Hotel
from Arrays import Users, Cities, Countries
from ApiCalls import ApiCalls

from PcTelBotExceptions import GetCountriesFailure


class PcTelBot(TeleBot):
    """
    Класс:
    -----
    Собственно бот, реализует взаимодействие с приложение "Telegram" через библиотеку "pyTelegramBotAPI"

    Аттрибуты:
    ---------


    Методы:
    ------


    """
    def __init__(self, token, parse_mode):

        super().__init__(token, parse_mode)

        self._bot_users = Users()
        self._countries = Countries()

        self.init_class_methods()
        self.init_ui()

        try:
            self.countries_per_world()
        except Exception:
            raise

    def init_class_methods(self) -> None:
        """
        Функция:
        -------
        Инициализация методов-обработчиков команд

        :return: None

        """
        decor_text_commands_handler: Callable = self.message_handler(func=lambda x: True)
        decor_buttons_handler: Callable = self.callback_query_handler(func=lambda x: True)

        decor_text_commands_handler(self.text_commands_handler)
        decor_buttons_handler(self.buttons_handler)

    def init_ui(self) -> None:
        """
        Функция:
        -------
        Инициализация элементов интерфейса пользователя

        :return: None

        """
        self.set_my_commands([
            tt.BotCommand('/start', 'Перезапуск бота'),
            tt.BotCommand('/help', 'Помощь'),
            tt.BotCommand('/menu', 'Вызов меню команд'),
            tt.BotCommand('/stop', 'Прервать текущий запрос'),
            tt.BotCommand('/lowprice', 'Подобрать самые дешёвые отели')
        ])

        # markup = tt.ReplyKeyboardMarkup(resize_keyboard=True)
        # tt.ReplyKeyboardRemove()

    def countries_per_world(self):
        """
        Формирует список стран

        Список стран является аттрибутом бота, он одинаков для всех пользователей
        Список стран считывается один раз при запуске бота, но т.к. в данной конкретной работе
        допустимое количество обращений к удалённой базе ограничено, при считывании мы
        формируем файл, и при следующем считывании проверяем наличие этого файла.
        Если файл существует - читаем не из удалённой базы, а из файла


        :return: None
        :raises: GetCountriesFailure

        """
        f_name: str = 'countries_raw.txt'
        f_name = cashfile(f_name)

        if not os.path.exists(f_name):

            countries_raw: List[Dict]
            ret_code: int

            countries_raw, ret_code = ApiCalls().get_countries_per_world()

            if countries_raw is not None:
                with open(f_name, 'w') as f_con:
                    f_con.write(str(countries_raw))
            else:
                raise GetCountriesFailure('Не удалось получить список стран')

        else:

            with open(f_name, 'r') as f_con:
                countries_raw = eval(f_con.read())

        # TODO переделать - если файл существует, то и структуру обновлять не надо
        # TODO получается, что когда бот запускается это один раз должно произойти
        # TODO и в остальных местах тоже

        def add_country(item):
            self._countries[item['id']] = Country(item['id'], item['iso'], item['countryname'], item['nicename'])

        # for item in countries_raw:
        #     self.countries[item['id']] = Country(item['id'], item['iso'], item['countryname'], item['nicename'])

        [add_country(item) for item in countries_raw]

    def cities_per_country(self, cid: int, msg: telebot.types.Message):
        """
        Формирует спискок городов для выбранной страны

        В идеале, нужно сформировать список всех стран и городов по странам один раз при запуске бота.
        Но, т.к. в данной конкретной работе....

        :param cid:
        :return:

        """
        country = self._countries[cid]
        f_name = 'cities_raw_' + country.iso + '.txt'
        f_name = cashfile(f_name)

        if not os.path.exists(f_name):

            cities_raw: List[Dict]
            ret_code: int

            cities_raw, ret_code = ApiCalls().get_cities_per_country(country.iso)

            if cities_raw is not None:
                with open(f_name, 'w', errors='replace') as f_cit:
                    f_cit.write(str(cities_raw))
            else:
                self.send_message(msg.chat.id, "Не удалось получить список городов для страны {}".format(country.nicename))
                return

        else:

            with open(f_name, 'r', errors='replace') as f_cit:
                cities_raw = eval(f_cit.read())

        def add_city(item):
            country.cities[item['id']] = City(item['id'], item['country'], item['name'], item['population'])

        [add_city(item) for item in cities_raw if item['population'] >= 10000]

    #def hotels_per_city(self, country_id: int, city_id: int):
    def hotels_per_city(self, user: User, msg: telebot.types.Message):
        """

        :param user:
        :return:

        """
        country = self._countries[user.selected_country]
        city = country.cities[user.selected_city]
        f_name = 'city_did_raw_' + country.iso + '_' + city.name + '.txt'
        f_name = cashfile(f_name)

        if not os.path.exists(f_name):

            locations_raw: List[Dict]
            ret_code: int

            locations_raw, ret_code = ApiCalls().get_city_destination_id(city.name)

            if locations_raw is not None:
                with open(f_name, 'w', errors='replace') as f_did:
                    f_did.write(str(locations_raw))
            else:
                self.send_message(msg.chat.id, "Не удалось получить destination_id в городе{}".format(city.name))
                return

        else:

            with open(f_name, 'r', errors='replace') as f_did:
                locations_raw = eval(f_did.read())

        locations_list = locations_raw['suggestions'][0]['entities'] # "0" is for CITY_GROUP

        def add_destination_id(item):
            city.dids.append(item['destinationId'])

        [add_destination_id(item) for item in locations_list]


        a = 1

        # теперь собственно для каждого отеля надо запросить детали
        # чтобы запросить детали уже нужны вроде даты

        # тут надо каждый раз честно запрашивать, потому что
        # перечень возвращаемых отелей разный для разных юзеров
        # и даже для разных запросов одного юзера

        f_name = 'hotels_raw_' + country.iso + '_' + city.name + '.txt'
        f_name = cashfile(f_name)

        if not os.path.exists(f_name):

            hotels_raw: List[Dict]
            ret_code: int

            hotels_raw, ret_code = ApiCalls().get_hotels_per_city(self, user)

            if hotels_raw is not None:
                with open(f_name, 'w', errors='replace') as f_hot:
                    f_hot.write(str(hotels_raw))
            else:
                self.send_message(msg.chat.id, "Не удалось получить список отелей в городе{}".format(city.name))
                return

        else:

            with open(f_name, 'r', errors='replace') as f_hot:
                hotels_raw = eval(f_hot.read())

        hotels_list = hotels_raw['data']['body']['searchResults']['results']

        user.hotels.clear()

        def add_hotel(item):
            hotel = Hotel(
                item['id'],
                user.selected_country,
                user.selected_city,
                item['name'],
                item['ratePlan']['price']['current'],
                item['landmarks'][0]['distance']
            )

            hotel.country = country.nicename
            hotel.city = city.name
            user.hotels[item['id']] = hotel

        [add_hotel(item) for item in hotels_list]

        # проверим, нужно ли запрашивать фото

        if user.photo_required:

            for item in user.hotels.values():

                # Фото можно на запрашивать а взять из файла, если есть,
                # потому что все юзеры, если запрашивают фото отеля,
                # то получают одно и то же

                f_name = 'photos_raw_' + country.iso + '_' + city.name + '_' + str(item.id) + '.txt'
                f_name = cashfile(f_name)

                if not os.path.exists(f_name):

                    photos_raw: Dict
                    ret_code: int

                    photos_raw, ret_code = ApiCalls().get_hotel_pictures(item.id)

                    if photos_raw is not None:
                        with open(f_name, 'w', errors='replace') as f_pht:
                            f_pht.write(str(photos_raw))
                    else:
                        self.send_message(msg.chat.id, "Не удалось получить фотографии для отеля {}".format(item.name))
                        return

                else:

                    with open(f_name, 'r', errors='replace') as f_pht:
                        photos_raw = eval(f_pht.read())

                photos_list = photos_raw['hotelImages']

                item.images.clear()

                def add_image(rec):
                    image_url_template = rec['baseUrl']
                    image_url = image_url_template.replace('{size}', 'z')
                    item.images.append(image_url)

                [add_image(rec) for i, rec in enumerate(photos_list) if i < user.photo_amount]



    def text_commands_handler(self, msg):
        """
        Функция:
        -------
        Обработчик текстовых команд

        :param msg: telebot.types.Message
            -
        :return:

        """

        #user_id = msg.from_user.id
        user_id = msg.chat.id

        if not self._bot_users.size and not msg.text == '/start':
            self.send_message(msg.chat.id, 'Для начала работы необходимо выполнить команду "/start"')
            return

        def amount_valid(amount: int, min_val: int, max_val: int) -> bool:
            return True if min_val <= amount <= max_val else False

        if msg.content_type == 'text':

            #if msg.text == '/cmd ' + str(BASE_COMMANDS.START.value) or msg.text == '/start':
            if msg.text == '/start':
                self.start(msg)
            elif msg.text == '/menu':
                self.menu(msg)
            elif msg.text == '/stop':
                self.stop(msg)
            #elif msg.text == '/cmd ' + str(BASE_COMMANDS.LOWPRICE.value) or msg.text == '/lowprice':
            elif msg.text == '/lowprice':
                self.lowprice(msg)

            elif msg.text.isdigit():

                if self._bot_users[user_id].fms['lowprice'].state == LOWPRICE_FLOW.GET_AMOUNT.value:
                    try:
                        amount = int(msg.text)
                    except TypeError:
                        self.send_message(msg.chat.id, 'Необходимо ввести число от 1 до 20\nВведите ещё раз')
                    else:
                        if amount_valid(amount, 1, 20):
                            self._bot_users[user_id].hotels_amount = amount
                            self._bot_users[user_id].fms['lowprice'].next_state(msg)
                        else:
                            self.send_message(msg.chat.id, 'Значение должно быть от 1 до 20.\nВведите ещё раз')

                elif self._bot_users[user_id].fms['lowprice'].state == LOWPRICE_FLOW.GET_PICS_AMOUNT.value:
                    try:
                        amount = int(msg.text)
                    except TypeError:
                        self.send_message(msg.chat.id, 'Необходимо ввести число от 1 до 5\nВведите ещё раз')
                    else:
                        if amount_valid(amount, 1, 5):
                            self._bot_users[user_id].photo_amount = amount
                            self._bot_users[user_id].fms['lowprice'].next_state(msg)
                        else:
                            self.send_message(msg.chat.id, 'Значение должно быть от 1 до 5.\nВведите ещё раз')

                else:
                    self.unknown(msg)

            else:
                self.unknown(msg)

    def buttons_handler(self, call):
        """
        Функция:
        -------
        Обработчик команд с inline-кнопок

        :param call: telebot.types.CallbackQuery
            -
        :return:

        """
        def execute_simple_command(cmd_id: int, user_id: int) -> None:
            """
            Функция:
            -------
            Обработчик команд без дополнтельного префикса

            :param id: int
                - id команды
            :param user_id: int
                - ижентификатор пользователя
            :return:

            """
            if cmd_id == BASE_COMMANDS.LOWPRICE.value:
                self.lowprice(call.message)

        def execute_prefix_command(cmd_prefix: str, cmd_id: int, user_id: int) -> None:
            """
            Функция:
            -------
            Обработчик команд с дополнтельным префиксом

            :param cmd_prefix: str
                -
            :param id: int
                - id команды
            :param user_id: int
                - ижентификатор пользователя
            :return: None

            """
            user = self._bot_users[user_id]

            if cmd_prefix == 'country': # команда от кнопок выбора страны
                user.selected_country = cmd_id
                user.fms['lowprice'].next_state(call.message)

            elif cmd_prefix == 'city': # команда от кнопок выбора города
                user.selected_city = cmd_id
                user.fms['lowprice'].next_state(call.message)
                #user.fms['lowprice'].next_state(call.message, next_state=LOWPRICE_FLOW.GET_HOTELS.value)

            elif cmd_prefix == 'photo': # надо ли загружать фото
                user.photo_required = True if cmd_id == YES_NO.YES.value else False
                if user.photo_required:
                    user.fms['lowprice'].next_state(call.message)
                else:
                    user.fms['lowprice'].next_state(call.message, next_state=LOWPRICE_FLOW.GET_CHECKIN_DATE.value)

            elif cmd_prefix == 'cd': # кнопки в календаре - № дня
                old_msg = call.message.text
                new_msg = '{}{:02d}{}'.format(old_msg[:-10], cmd_id, old_msg[-8:])
                self.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=new_msg,
                    parse_mode='HTML',
                    reply_markup=self.keyboard_calender()
                )

            elif cmd_prefix == 'cm': # кнопки в календаре - № месяца
                old_msg = call.message.text
                new_msg = '{}{:02d}{}'.format(old_msg[:-7], cmd_id, old_msg[-5:])
                self.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=new_msg,
                    parse_mode='HTML',
                    reply_markup=self.keyboard_calender()
                )

            elif cmd_prefix == 'cy': # кнопки в календаре - № года
                old_msg = call.message.text
                new_msg = old_msg[:-4] + str(cmd_id)
                self.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=new_msg,
                    parse_mode='HTML',
                    reply_markup=self.keyboard_calender()
                )

            elif cmd_prefix == 'cready':
                if user.fms['lowprice'].state == LOWPRICE_FLOW.GET_CHECKIN_DATE.value:
                    user.checkin_date = call.message.text
                elif user.fms['lowprice'].state == LOWPRICE_FLOW.GET_CHECKOUT_DATE.value:
                    user.checkout_date = call.message.text
                user.fms['lowprice'].next_state(call.message)


            a = 1



        user_id = call.message.chat.id

        if not call.data.startswith('/'):
            self.answer_callback_query(
                callback_query_id=call.id,
                show_alert=True,
                #text='Неизвестная команда.\nОбратитесь к разработчику')
                text='Эта кнопка пока не работает')
            return

        command: str = call.data.lstrip('/')
        command_decomposed: List[str] = command.split()





        if len(command_decomposed) == 2:
            cmd_id = int(command_decomposed[1])
            execute_simple_command(cmd_id, user_id)
        elif len(command_decomposed) == 3:
            cmd_prefix = command_decomposed[1]
            cmd_id = int(command_decomposed[2])
            execute_prefix_command(cmd_prefix, cmd_id, user_id)
        else:
            self.answer_callback_query(
                callback_query_id=call.id,
                show_alert=True,
                text='Неизвестная команда.\nОбратитесь к разработчику')
            return

    def keyboard_select_main_cmd(self):

        buttons = [
                [tt.InlineKeyboardButton(text='✨  Подобрать самые дешёвые отели', callback_data='/cmd ' + str(BASE_COMMANDS.LOWPRICE.value))],
                [tt.InlineKeyboardButton(text='💲  Подобрать самые дорогие отели', callback_data='1')],
                [tt.InlineKeyboardButton(text='👍  Подобрать самые подходящие отели', callback_data='1')],
                [tt.InlineKeyboardButton(text='📜  Посмотреть историю поиска', callback_data='1')],
                [tt.InlineKeyboardButton(text='ℹ  Получить справку о работе с ботом', callback_data='1')]
        ]

        return tt.InlineKeyboardMarkup(buttons)

    def keyboard_select_country(self):

        countries = list(self._countries.values())
        number_of_keyboards = math.ceil(self._countries.size / 100)

        kb_parts = []

        buttons = [
            [
                tt.InlineKeyboardButton(
                    text = countries[j * 3 + i].nicename,
                    callback_data = '/cmd country ' + str(countries[j * 3 + i].id)
                )
                for i in range(3)
                if j * 3 + i < self._countries.size
            ]
            for j in range(0, int(100/3))
        ]

        kb_parts.append(buttons)

        buttons = [
            [
                tt.InlineKeyboardButton(
                    text = countries[j * 3 + i].nicename,
                    callback_data = '/cmd country ' + str(countries[j * 3 + i].id)
                )
                for i in range(3)
                if j * 3 + i < self._countries.size
            ]
            for j in range(int(100/3), int(200/3))
        ]

        kb_parts.append(buttons)

        buttons = [
            [
                tt.InlineKeyboardButton(
                    text = countries[j * 3 + i].nicename,
                    callback_data = '/cmd country ' + str(countries[j * 3 + i].id)
                )
                for i in range(3)
                if j * 3 + i < self._countries.size
            ]
            for j in range(int(200/3), int(self._countries.size/3) + 1)
        ]

        kb_parts.append(buttons)

        keyboards = [tt.InlineKeyboardMarkup(item) for item in kb_parts]

        return keyboards

    def keyboard_select_city(self, cid: int):

        cities = list(self._countries[cid].cities.values())
        number_of_keyboards = math.ceil(self._countries[cid].cities.size / 100)

        kb_parts = []

        buttons = [
            [
                tt.InlineKeyboardButton(
                    text = cities[j * 3 + i].name,
                    callback_data ='/cmd city ' + str(cities[j * 3 + i].id)
                )
                for i in range(3)
                if j * 3 + i < self._countries[cid].cities.size
            ]
            for j in range(0, int(100/3))
        ]

        kb_parts.append(buttons)

        buttons = [
            [
                tt.InlineKeyboardButton(
                    text = cities[j * 3 + i].name,
                    callback_data ='/cmd city ' + str(cities[j * 3 + i].id)
                )
                for i in range(3)
                if j * 3 + i < self._countries[cid].cities.size
            ]
            for j in range(int(100/3), int(200/3))
        ]

        kb_parts.append(buttons)

        kb_parts.append(buttons)

        buttons = [
            [
                tt.InlineKeyboardButton(
                    text=cities[j * 3 + i].name,
                    callback_data='/cmd city ' + str(cities[j * 3 + i].id)
                )
                for i in range(3)
                if j * 3 + i < self._countries[cid].cities.size
            ]
            for j in range(int(200/3), int(self._countries[cid].cities.size) + 1)
        ]

        kb_parts.append(buttons)

        keyboards = [tt.InlineKeyboardMarkup(item) for item in kb_parts]

        return keyboards

    def keyboard_yes_no(self, cmd_prefix: str) -> telebot.types.InlineKeyboardMarkup:

        buttons: List[List[telebot.types.InlineKeyboardButton]] = [
            [
                tt.InlineKeyboardButton(text='✔️Да', callback_data='/cmd ' + cmd_prefix + ' ' + str(YES_NO.YES.value)),
                tt.InlineKeyboardButton(text='❌ Нет', callback_data='/cmd ' + cmd_prefix + ' ' + str(YES_NO.NO.value))
            ]
        ]

        return tt.InlineKeyboardMarkup(buttons)

    def keyboard_calender(self):

        buttons = [
            [
                tt.InlineKeyboardButton(text='2022', callback_data='/cmd cy 2022'),
                tt.InlineKeyboardButton(text='2023', callback_data='/cmd cy 2023')
            ],
            # [
            #     tt.InlineKeyboardButton(text='---', callback_data='1')
            # ],
            [
                tt.InlineKeyboardButton(text='янв', callback_data='/cmd cm 1'),
                tt.InlineKeyboardButton(text='фев', callback_data='/cmd cm 2'),
                tt.InlineKeyboardButton(text='мар', callback_data='/cmd cm 3'),
                tt.InlineKeyboardButton(text='апр', callback_data='/cmd cm 4'),
                tt.InlineKeyboardButton(text='май', callback_data='/cmd cm 5'),
                tt.InlineKeyboardButton(text='июн', callback_data='/cmd cm 6')
            ],
            [
                tt.InlineKeyboardButton(text='июл', callback_data='/cmd cm 7'),
                tt.InlineKeyboardButton(text='авг', callback_data='/cmd cm 8'),
                tt.InlineKeyboardButton(text='сен', callback_data='/cmd cm 9'),
                tt.InlineKeyboardButton(text='окт', callback_data='/cmd cm 10'),
                tt.InlineKeyboardButton(text='ноя', callback_data='/cmd cm 11'),
                tt.InlineKeyboardButton(text='дек', callback_data='/cmd cm 12')
            ],
            # [
            #     tt.InlineKeyboardButton(text='---', callback_data='1')
            # ]
            [
                tt.InlineKeyboardButton(text=str(i), callback_data='/cmd cd ' + str(i))
                for i in range(1, 1 + 7)
            ],
            [
                tt.InlineKeyboardButton(text=str(i), callback_data='/cmd cd ' + str(i))
                for i in range(8, 8 + 7)
            ],
            [
                tt.InlineKeyboardButton(text=str(i), callback_data='/cmd cd ' + str(i))
                for i in range(15, 15 + 7)
            ],
            [
                tt.InlineKeyboardButton(text=str(i), callback_data='/cmd cd ' + str(i))
                for i in range(22, 22 + 7)
            ],
            [
                tt.InlineKeyboardButton(text='29', callback_data='/cmd cd 29'),
                tt.InlineKeyboardButton(text='30', callback_data='/cmd cd 30'),
                tt.InlineKeyboardButton(text='31', callback_data='/cmd cd 31'),
                tt.InlineKeyboardButton(text='Готово', callback_data='/cmd cready 1')
            ]
        ]

        return tt.InlineKeyboardMarkup(buttons)

    def unknown(self, msg):
        """
        Функция:
        -------
        Обработка неизвестной текстовой команды

        :param msg:
        :return:
        """

        if msg.text.startswith('/'):
            out = 'Эта команда пока не работает'
        else:
            out = 'Вы ввели текст: "{}",\n но я понимаю только команды\n' \
                  'Чтобы начать вводить команду наберите "/"'.format(
                msg.text
                )

        self.send_message(msg.chat.id, out)

    def start(self, msg):

        user_id = msg.chat.id

        if user_id not in self._bot_users.keys():
            self._bot_users[user_id] = User(
                msg.chat.id,
                msg.chat.username,
                msg.chat.first_name + ' ' + msg.chat.last_name
            )
            self._bot_users[user_id].connect_bot(self)



        hello_message: str = 'Здравствуйте!\n\n' \
                    'Это бот по поиску и подбору отелей\n\n' \
                    'Если я правильно понимаю, Вы - <b>{}</b>\n'.format(msg.from_user.full_name)

        try:
            self.send_message(
                msg.chat.id,
                hello_message,
                parse_mode='HTML'
                )
        except (exceptions.ConnectTimeout, exceptions.ReadTimeout):
            #self.stop_polling()
            a = 1
            raise
        finally:
            self.menu(msg)

    def menu(self, msg):

        kbrd_select_main_cmd: telebot.types.InlineKeyboardMarkup = self.keyboard_select_main_cmd()

        try:
            self.send_message(
                msg.chat.id,
                'Пожалуйста, выберите. что Вас интересует:',
                reply_markup=kbrd_select_main_cmd
            )
        except exceptions.ReadTimeout:
            raise

    def stop(self, msg):

        user_id = msg.chat.id
        self._bot_users[user_id].stop_all_flows(msg)

    def lowprice(self, msg):

        user_id = msg.chat.id
        self._bot_users[user_id].current_command = BASE_COMMANDS.LOWPRICE.value
        self._bot_users[user_id].fms['lowprice'].start(msg)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def countries(self):
        return self._countries












