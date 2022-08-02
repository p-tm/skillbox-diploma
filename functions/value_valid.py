from typing import *


def value_valid(
        val: Union[int, float],
        min_val: Union[int, float],
        max_val: Union[int, float]
) -> bool:
    """
    Проверка на диапазон ввода числа

    :param val:
    :param min_val:
    :param max_val:
    :return: True если значение находится в заданном диапазоне TODO везде попроавить

    """
    return True if min_val <= val <= max_val else False
