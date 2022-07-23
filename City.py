class City:
    """
    Класс:
    -----
    Описание сущности "Город"

    Аттрибуты:
    ---------


    Методы:
    ------


    """
    def __init__(self, id, ciso, name, population) -> None:
        """
        Функция (метод объекта):
        -----------------------
        Конструктор

        :return: None

        """
        self._id: int = id
        self._country_iso = ciso
        self._name = name
        self._population = population
        self._dids = []  # это список destination_id которые выдаёт hotels.com.api

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    @property
    def id(self):
        return self._id

    # @property
    # def country_iso(self):
    #     return self.__country_iso

    @property
    def name(self):
        return self._name

    # @property
    # def population(self):
    #     return self.__population

    @property
    def dids(self):
        return self._dids
