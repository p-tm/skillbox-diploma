import os

from typing import *

FOLDER_REUSABLE = 'reusable'
BOT_TOKEN = '5547620893:AAHaqK42H3J52nvX2MjNeBR4su3APKt9Olc'

def cashfile(f_name: str) -> str:
    """
    Функция:
    -------
    Формирует относительный путь для размещения файлов для кэширования данных

    :param f_name: str
        - имя файла
    :return: str
        - относительный путь к файлу

    """
    return os.path.join(FOLDER_REUSABLE, f_name)