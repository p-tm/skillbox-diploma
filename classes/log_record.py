import pickle

from classes.user_state_data import UserStateData
from dataclasses import dataclass
from datetime import datetime

from typing import *

@dataclass
class LogRecord:

    _dt: Optional[str] = None               # дата и время
    _type: Optional[str] = None             # тип записи
    _content: Optional[str] = None          # содержание
    _usd: Optional[UserStateData] = None    # данные пользователя

    def create(self, rtype: str, text: str) -> str:
        """
        Создаёт запись (текст) для записи в файл истории
        Запись имеет формат '<дата и время> <тип> <содержание>'
        Время записывается с разрешением до [мс]

        :param rtype: тип записи
            - 'UCMD' - пользовательская команда
            - 'RSLT' - результаты поиска
        :param text: содержание записи
        :return: строка записи для файла истории

        """
        rec: str = '{} {} {}\n'.format(
            datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3],
            rtype,
            text
        )
        return rec

    def decode(self, line: str) -> None:
        """
        Декодирование (расшифровка) записи из файла

        :param line: запись из файла

        """
        xline: str = line.rstrip('\n')
        self._dt = xline[:23]
        self._type = xline[24:28]
        self._content = xline[29:]
        if self._type == 'RSLT':
            self._usd = pickle.loads(eval(self._content))

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def dt(self):
        return self._dt

    @property
    def type(self):
        return self._type

    @property
    def content(self):
        return self._content

    @property
    def usd(self):
        return self._usd


