"""
Описание функции

"""
import os

from config import FOLDER_REUSABLE


def cashfile(f_name: str) -> str:
    """
    Формирует относительный путь для размещения файлов для кэширования данных

    :param f_name: имя файла
    :return: относительный путь к файлу

    """
    return os.path.join(FOLDER_REUSABLE, f_name)