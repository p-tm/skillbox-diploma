"""
Описание класса

"""
from dataclasses import dataclass
from typing import Iterable, Optional, TextIO
from classes.log_record import LogRecord

@dataclass
class HistoryLog:
    """
    Описание сущности "история"

    """
    _filename: Optional[str] = None    # имя файла с историей

    def init_logger(self, uid: int, cid: int) -> None:
        """
        Инициализация - формируем имя файла истории (оно включает chat_id и user_id)

        :param uid: user_id
        :param cid: chat_id

        """
        self._filename = 'histories/{}_{}.log'.format(uid, cid)

    def add_rec(self, rtype: str, text: str) -> None:
        """
        Добавление записи в файл истории

        :param rtype:
        :param text:

        """
        # logging.info(LogRecord().create(rtype, text))
        f: TextIO
        with open(self._filename, mode='a', encoding='utf-8', errors='replace') as f:
            f.write(LogRecord().create(rtype, text))

    def get_from_file(self) -> Iterable[LogRecord]:
        """
        Получение записей из файла истории

        :yield: запись из файла, преобразованная в тип LogRecord

        """
        f: TextIO
        with open(self._filename, mode='r', encoding='utf-8', errors='replace') as f:
            line: str
            for line in f:
                lr: LogRecord = LogRecord()
                lr.decode(line)
                yield lr

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''





