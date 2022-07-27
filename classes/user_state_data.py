class UserStateData:
    """
    Хранение данных (состояния) конкретного пользователя в конкретном чате

    Аттрибуты:
    ---------
    _substate: int (enum)

    Методы:
    ------
    """


    def __init__(self):
        self._substate = None
        self._selected_country_id = None
        self._selected_city_id = None
        self._hotels_amount = None
        self._photo_required = None
        self._photos_amount = None
        self._keyboard_maker = {}

        self.reinit_keyboard()

    def set_keyboard_data(self, *, case: str, current: int, last: int):
        self._keyboard_maker['case'] = case
        self._keyboard_maker['current'] = current
        self._keyboard_maker['last'] = last

    def retrieve_keyboard_data(self):
        return self._keyboard_maker['case'], self._keyboard_maker['current'], self._keyboard_maker['last']

    def next_keyboard(self):
        current = self._keyboard_maker['current']
        last = self._keyboard_maker['last']
        next = current + 1
        if next <= last:
            self._keyboard_maker['current'] = next
            return next
        return 0

    def reinit_keyboard(self):
        self._keyboard_maker['case'] = 'none'
        self._keyboard_maker['current'] = 0
        self._keyboard_maker['last'] = 0



    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def substate(self):
        return self._substate

    @substate.setter
    def substate(self, st):
        self._substate = st

    @property
    def selected_country_id(self):
        return self._selected_country_id

    @selected_country_id.setter
    def selected_country_id(self, id):
        self._selected_country_id = id

    @property
    def keyboard_maker(self):
        return self._keyboard_maker

