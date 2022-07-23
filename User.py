from typing import *
#from telebot import telebot
from enums import *
from Arrays import FlowManagers, Hotels
from FM_LowPrice import FM_LowPrice

class User:
    """

    Аттрибуты:
    ---------



    Методы:
    ------



    """
    def __init__(self, id, telname, full_name):
        super().__init__()

        self._id = id
        self._telname = telname
        self._full_name = full_name
        self._bot = None
        self._selected_country = None
        self._selected_city = None
        self._current_flow = BASE_COMMANDS.NONE.value
        self._hotels_amount = 4
        self._photo_required = False
        self._photo_amount = 2
        self._fms = FlowManagers()
        self._hotels = Hotels()

        self._fms['lowprice'] = FM_LowPrice(self)
        #self.fms['highprice'] = None


    def connect_bot(self, bot: 'telebot.TeleBot'):
        self._bot = bot
        [item.connect_bot(bot) for item in self.fms.values()]

    def stop_all_flows(self, msg: 'telebot.types.Message'):
        for item in self.fms.values():
            if item.busy:
                item.stop(msg)
                self._bot.send_message(msg.chat.id, 'Выполнение команды {} прервано.'.format(item.flowname))

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def selected_country(self):
        return self._selected_country

    @selected_country.setter
    def selected_country(self, sc):
        self._selected_country = sc

    @property
    def selected_city(self):
        return self._selected_city

    @selected_city.setter
    def selected_city(self, sc):
        self._selected_city = sc

    @property
    def photo_required(self):
        return self._photo_required

    @photo_required.setter
    def photo_required(self, yes_no):
        self._photo_required = yes_no

    @property
    def fms(self):
        return self._fms

    @property
    def hotels(self):
        return self._hotels
