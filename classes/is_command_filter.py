"""
Описание класса

"""
from telebot.custom_filters import SimpleCustomFilter


class IsCommandFilter(SimpleCustomFilter):
    """
    Вроде бы не нужен

    """
    key = 'is_command'

    def check(self, message):
        return message.text.startswith('/')

