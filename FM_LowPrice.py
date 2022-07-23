from enums import *
from FlowManager import FlowManager
#from telebot import telebot
#from User import User


class FM_LowPrice(FlowManager):
    """
    Класс:
    -----


    Аттрибуты:
    ---------


    Методы:
    ------


    """
    def __init__(self,  user: 'User'):
        super().__init__(LOWPRICE_FLOW, user)
        self._flow_name = '/lowprice'


    def start(self, msg: 'telebot.types.Message'):
        super().start(msg)
        self.next_state(msg)
        #self.next_state(msg, next_state=LOWPRICE_FLOW.GET_CITIES.value)


    def next_state(self, msg: 'telebot.types.Message', *, next_state: int = None):

        super().next_state(msg, next_state=next_state)

        user = self._user
        bot = self._bot

        if self._state == LOWPRICE_FLOW.GET_COUNTRY.value:

            keyboards = self._bot.keyboard_select_country()

            #self._bot.send_message(msg.chat.id, 'Шаг 1.')
            bot.send_message(
                msg.chat.id,
                '☑️Выберите страну:\n',
                reply_markup=keyboards[0]
            )
            bot.send_message(
                msg.chat.id,
                '...\n',
                reply_markup=keyboards[1]
            )
            bot.send_message(
                msg.chat.id,
                '...\n',
                reply_markup=keyboards[2]
            )

        elif self._state == LOWPRICE_FLOW.GET_CITIES.value:

            #self._user.selected_country = 177  # Russia

            bot.cities_per_country(self._user.selected_country, msg)

            keyboards = self._bot.keyboard_select_city(self._user.selected_country)

            #self._bot.send_message(msg.chat.id, 'Шаг 2.')
            bot.send_message(
                msg.chat.id,
                '☑️Выберите город:\n',
                reply_markup=keyboards[0]
            )
            bot.send_message(
                msg.chat.id,
                '...\n',
                reply_markup=keyboards[1]
            )
            bot.send_message(
                msg.chat.id,
                '...\n',
                reply_markup=keyboards[2]
            )

        elif self._state == LOWPRICE_FLOW.GET_AMOUNT.value:

            #self._bot.send_message(msg.chat.id, 'Шаг 3.')
            bot.send_message(
                msg.chat.id,
                '## Введите количество отелей (от 1 до 20):'
            )

        elif self._state == LOWPRICE_FLOW.GET_NEED_PICS.value:

            #self._bot.send_message(msg.chat.id, 'Шаг 4.')
            bot.send_message(
                msg.chat.id,
                '## Хотите ли получить фотографии отелей?:',
                reply_markup=self._bot.keyboard_yes_no('photo')
            )

        elif self._state == LOWPRICE_FLOW.GET_PICS_AMOUNT.value:

            #self._bot.send_message(msg.chat.id, 'Шаг 5.')
            self._bot.send_message(
                msg.chat.id,
                '## Введите количество фотографий (от 1 до 5):'
            )

        elif self._state == LOWPRICE_FLOW.GET_CHECKIN_DATE.value:

            #self._bot.send_message(msg.chat.id, 'Шаг 6.')
            self._bot.send_message(
                msg.chat.id,
                '## Выберите дату заезда: __.__.____',
                #parse_mode='HTML',
                reply_markup=self._bot.keyboard_calender()
            )

        elif self._state == LOWPRICE_FLOW.GET_CHECKOUT_DATE.value:

            #self._bot.send_message(msg.chat.id, 'Шаг 7.')
            self._bot.send_message(
                msg.chat.id,
                '## Выберите дату выезда: __.__.____',
                #parse_mode='HTML',
                reply_markup=self._bot.keyboard_calender()
            )

        elif self._state == LOWPRICE_FLOW.GET_HOTELS.value:

            #self._user.selected_country = 177  # Russia
            #self._user.selected_city = 2023469 # Irkutsk

            #self._bot.hotels_per_city(self._user.selected_country, self._user.selected_city)
            bot.hotels_per_city(self._user, msg)
            self.next_state(msg)


        elif self._state == LOWPRICE_FLOW.PRINT_RESULTS.value:

            keylist = list(self._user.hotels.keys())
            #key = list(self._user.hotels.keys())[0]

            #self._bot.send_message(msg.chat.id, 'Шаг 8.')

            out = 'Итак, Ваши критерии поиска:\n\n' \
                  '<i>Страна:</i> {}\n' \
                  '<i>Город:</i> {}\n' \
                  '<i>Дата заезда:</i> {}\n' \
                  '<i>Дата выезда:</i> {}\n' \
                  '<i>Количество ночей:</i> {}'.format(
                self._bot.countries[self._user.selected_country].nicename,
                self._bot.countries[self._user.selected_country].cities[self._user.selected_city].name,
                'заглушка',
                'заглушка',
                'заглушка'
            )

            self._bot.send_message(
                msg.chat.id,
                out,
                parse_mode='HTML'
            )

            self._bot.send_message(
                msg.chat.id,
                '## Список подходящих отелей:'
            )
            for key in keylist:
                bot.send_message(
                    msg.chat.id,
                    user.hotels[key].print_to_telegram(),
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )

                #lst = [self._user.hotels[key].images[0], self._user.hotels[key].images[1]]
                #self._bot.send_photo(msg.chat.id, photo=lst)
                for ph in user.hotels[key].images:
                    bot.send_photo(
                        msg.chat.id,
                        photo=ph
                    )

            self.next_state(msg)

            a = 1









