#from telebot import telebot
from enum import Enum
#from User import User


class FlowManager:
    """
    Класс:
    -----
    Описание сущности "Менеджер хода выполнения команды"

    Примечание:
    ----------
    Используется как базовый класс для реализации общих базовых методов,
    на наследования от него строятся менеджеры для индивидуальных команд

    Аттрибуты:
    ---------
    _busy: bool
        - менеджер "занят" (команда активна, в ходе выполнения)
    _state: int
        - текущий шаг выполнения
    _max_steps: int
        - всего шагов
    _bot: PcTelBot
        - Telegram-bot, с которым взаимодействует менеджер
    _user: User
        - ссылка на объект User - это пользователь, который запустил команду (менеджера)
    _flow_name: str
        - название команды (используется для удоства, например, для выдачи в сообщения)

    Методы:
    ------



    """
    def __init__(self, flow: Enum, user: 'User'):

        max_steps = 0
        for x in flow:
            max_steps = x.value if x.value > max_steps else max_steps

        self._busy = False
        self._state = 0
        self._max_steps = max_steps
        self._bot = None
        self._user = user
        self._flow_name = ''


    def connect_bot(self, bot: 'telebot.TeleBot'):
        """
        Функция (метод объекта):
        -----------------------
        :param bot:
        :return:
        """
        self._bot = bot

    def start(self, msg: 'telebot.types.Message'):
        """
        Функция (метод объекта):
        -----------------------
        :param msg:
        :return:
        """
        self._busy = True
        self._state = 1

    def stop(self, msg: 'telebot.types.Message'):
        """
        Функция (метод объекта):
        -----------------------
        :param msg:
        :return:
        """
        self._busy = False
        self._state = 0

    def next_state(self, msg: 'telebot.types.Message', *, next_state: int = None):
        """
        Функция (метод объекта):
        -----------------------
        :param msg:
        :param next_state:
        :return:
        """

        if not self._busy:
            return

        if next_state is not None:
            if next_state <= self._max_steps:
                self._state = next_state
            else:
                self._state = 0
                self._busy = False
        else:
            if self._state + 1 <= self._max_steps:
                self._state += 1
            else:
                self._state = 0
                self._busy = False

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def busy(self):
        return self._busy

    @property
    def state(self):
        return self._state

    @property
    def flowname(self):
        return self._flow_name
