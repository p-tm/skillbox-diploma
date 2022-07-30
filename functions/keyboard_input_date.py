from telebot import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

from functions.send_message_helper import send_message_helper
from loader import bot, input_date_callback_factory

# input_date_callback_factory = CallbackData('type', 'content', prefix='date')


class InputDateCallbackFilter(AdvancedCustomFilter):
    """
    Фильтрация callback_data - выделяем данные, которые относятся к клавиатуре ввода даты

    """
    key = 'filter_input_date'

    def check(self, call: telebot.types.CallbackQuery, config: CallbackDataFilter) -> bool:
        """
        Функция фильтрации

        """
        x = config.check(query=call)
        return x


bot.add_custom_filter(InputDateCallbackFilter())

def keyboard_input_date():
    buttons = [
        [
            InlineKeyboardButton(text=str(i), callback_data=input_date_callback_factory.new(type='D',  content=str(i)))
            for i in range(1, 1 + 7)
        ],
        [
            InlineKeyboardButton(text=str(i), callback_data=input_date_callback_factory.new(type='D',  content=str(i)))
            for i in range(8, 8 + 7)
        ],
        [
            InlineKeyboardButton(text=str(i), callback_data=input_date_callback_factory.new(type='D',  content=str(i)))
            for i in range(15, 15 + 7)
        ],
        [
            InlineKeyboardButton(text=str(i), callback_data=input_date_callback_factory.new(type='D',  content=str(i)))
            for i in range(22, 22 + 7)
        ],
        [
            InlineKeyboardButton(text='29', callback_data=input_date_callback_factory.new(type='D', content=29)),
            InlineKeyboardButton(text='30', callback_data=input_date_callback_factory.new(type='D', content=30)),
            InlineKeyboardButton(text='31', callback_data=input_date_callback_factory.new(type='D', content=31)),
            InlineKeyboardButton(text='-', callback_data=input_date_callback_factory.new(type='idle', content='idle')),
            InlineKeyboardButton(text='-', callback_data=input_date_callback_factory.new(type='idle', content='idle')),
            InlineKeyboardButton(text='-', callback_data=input_date_callback_factory.new(type='idle', content='idle')),
            InlineKeyboardButton(text='-', callback_data=input_date_callback_factory.new(type='idle', content='idle'))
        ],
        [
            InlineKeyboardButton(text='янв', callback_data=input_date_callback_factory.new(type='M', content=1)),
            InlineKeyboardButton(text='фев', callback_data=input_date_callback_factory.new(type='M', content=2)),
            InlineKeyboardButton(text='мар', callback_data=input_date_callback_factory.new(type='M', content=3)),
            InlineKeyboardButton(text='апр', callback_data=input_date_callback_factory.new(type='M', content=4)),
            InlineKeyboardButton(text='май', callback_data=input_date_callback_factory.new(type='M', content=5)),
            InlineKeyboardButton(text='июн', callback_data=input_date_callback_factory.new(type='M', content=6))
        ],
        [
            InlineKeyboardButton(text='июл', callback_data=input_date_callback_factory.new(type='M', content=7)),
            InlineKeyboardButton(text='авг', callback_data=input_date_callback_factory.new(type='M', content=8)),
            InlineKeyboardButton(text='сен', callback_data=input_date_callback_factory.new(type='M', content=9)),
            InlineKeyboardButton(text='окт', callback_data=input_date_callback_factory.new(type='M', content=10)),
            InlineKeyboardButton(text='ноя', callback_data=input_date_callback_factory.new(type='M', content=11)),
            InlineKeyboardButton(text='дек', callback_data=input_date_callback_factory.new(type='M', content=12))
        ],
        [
            InlineKeyboardButton(text='2022', callback_data=input_date_callback_factory.new(type='Y', content=2022)),
            InlineKeyboardButton(text='2023', callback_data=input_date_callback_factory.new(type='Y', content=2023))
        ],
        [
            InlineKeyboardButton(text='Готово', callback_data=input_date_callback_factory.new(type='enter', content='enter'))
        ]
    ]

    return InlineKeyboardMarkup(buttons)



@bot.callback_query_handler(
    func=None,
    filter_input_date=input_date_callback_factory.filter(type='D')
)
def day_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку

    :param call: telebot.types.CallbackQuery

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data = input_date_callback_factory.parse(callback_data=call.data)

    day = int(callback_data['content'])

    old = call.message.text
    new = '{}{:02d}{}'.format(old[:-10], day, old[-8:])
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=call.message.message_id,
        text=new,
        parse_mode='HTML',
        reply_markup=keyboard_input_date()
    )


@bot.callback_query_handler(
    func=None,
    filter_input_date=input_date_callback_factory.filter(type='M')
)
def month_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку выбора страны

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data = input_date_callback_factory.parse(callback_data=call.data)

    month = int(callback_data['content'])

    old = call.message.text
    new = '{}{:02d}{}'.format(old[:-7], month, old[-5:])
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=call.message.message_id,
        text=new,
        parse_mode='HTML',
        reply_markup=keyboard_input_date()
    )

@bot.callback_query_handler(
    func=None,
    filter_input_date=input_date_callback_factory.filter(type='Y')
)
def year_button(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик события нажатия на кнопку выбора страны

    :param call: telebot.types.CallbackQuery
    :return: None

    """
    user: int = call.message.chat.id
    chat: int = call.message.chat.id

    callback_data = input_date_callback_factory.parse(callback_data=call.data)

    year = int(callback_data['content'])

    old = call.message.text
    new = old[:-4] + str(year)
    send_message_helper(bot.edit_message_text, retries=3)(
        chat_id=chat,
        message_id=call.message.message_id,
        text=new,
        parse_mode='HTML',
        reply_markup=keyboard_input_date()
    )
