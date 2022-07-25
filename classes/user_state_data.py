class UserStateData:
    """
    Класс:
    _____
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

