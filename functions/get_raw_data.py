import os
from typing import *

from api.api_calls import ApiCalls
from exceptions.data_unavalible import DataUnavailible
from functions.cashfile import cashfile


def get_raw_data(*, force: bool, fname: str, func: Callable, **func_kwa) -> Dict[str, Any]:
    """
    Функция используется при удалённых запросах и проверяет, есть ли уже эти данные в кэш-файле
    если есть, то данные берутся из файла

    :param force: всегда читать из удалённого источника
    :param fname: имя кэш-файла (без относительного пути)
    :param func: функция, которая получает данные
    :param **func_kwa: аргументы для функции func

    :return:

    """
    f_name = cashfile(fname)    # добавляем относительный путь

    if not os.path.exists(f_name) or force:

        try:
            #countries_raw: Dict = ApiCalls().get_countries_per_world()
            raw_data: Dict[str, Any] = func(**func_kwa)
        except DataUnavailible:
            raise

        f: Iterable[str]
        with open(f_name, 'w', errors='replace') as f:
            f.write(str(raw_data))
    else:
        f: Iterable[str]
        with open(f_name, 'r', errors='replace') as f:
            raw_data: Dict[str, Any] = eval(f.read())

    return raw_data
