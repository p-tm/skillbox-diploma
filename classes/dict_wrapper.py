class DictWrapper(dict):
    """
    Класс:
    -----
    Обёртка на встроенный dict

    Примечания:
    ----------
    Пока хочу только сделать удобный доступ к размеру словаря

    Аттрибуты:
    ---------
    --

    Методы:
    ------
    --

    """
    def __init__(self):
        """
        Функция (метод экземпляра)
        -------------------------
        Конструктор
        
        """
        super().__init__()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    геттеры и сеттеры

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def size(self):
        return len(self)