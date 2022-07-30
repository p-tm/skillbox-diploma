from telebot.custom_filters import SimpleCustomFilter


class IsCommandFilter(SimpleCustomFilter):

    key = 'is_command'

    def check(self, message):
        return message.text.startswith('/')

