
class Country:
    """
    Класс:
    -----
    Описание сущности "Страна"


    Аттрибуты:
    ---------


    Методы:
    ------


    """

    # !!! сохраняем id для страны и для города
    # потому что потом по id будем связывать их с кнопками на экране

    def __init__(self, id, iso, countryname, nicename):
        self._id = id
        self._iso = iso
        self._countryname = countryname
        self._nicename = nicename
        #self._cities = Cities()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def id(self):
        return self._id

    @property
    def iso(self):
        return self._iso

    @property
    def nicename(self):
        return self._nicename

    @property
    def cities(self):
        return self._cities
