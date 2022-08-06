"""
Описание функции

"""
from datetime import datetime


def console_message(msg: str) -> None:
    """
    Выводит сообщение в консоль с указанием времени

    :param msg: текст сообщения

    """
    print(
        '{}: {}'.format(
            datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3],
            msg
        )
    )