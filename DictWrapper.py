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
        super().__init__()

    @property
    def size(self):
        return len(self)