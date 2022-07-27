import os

from config import FOLDER_REUSABLE


def cashfile(f_name: str) -> str:
    """
    Формирует относительный путь для размещения файлов для кэширования данных

    :param f_name: str - имя файла
    :return: str - относительный путь к файлу

    """
    return os.path.join(FOLDER_REUSABLE, f_name)