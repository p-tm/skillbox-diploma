class GetCountriesFailure(Exception):
    """
    Класс:
    -----
    Исключение - не удалось получить список стран

    """
    def __init__(self, message: str) -> None:
        super().__init__(message)


