from enum import Enum

class YES_NO(Enum):

    NO = 1
    YES = 2

class BASE_COMMANDS(Enum):

    NONE = 0
    START = 1
    HELP = 2
    LOWPRICE = 3
    HIGHPRICE = 4
    BESTDEAL = 5


class LOWPRICE_FLOW(Enum):

    NONE = 0
    START = 1
    GET_COUNTRY = 2
    GET_CITIES = 3
    GET_AMOUNT = 4
    GET_NEED_PICS = 5
    GET_PICS_AMOUNT = 6
    GET_CHECKIN_DATE = 7
    GET_CHECKOUT_DATE = 8
    GET_HOTELS = 9
    PRINT_RESULTS = 10


class HIGHPRICE_FLOW(Enum):

    NONE = 0
    START = 1
    GET_COUNTRY = 2
    GET_CITIES = 3
    GET_AMOUNT = 4
    GET_NEED_PICS = 5
    GET_PICS_AMOUNT = 6
    GET_CHECKIN_DATE = 7
    GET_CHECKOUT_DATE = 8
    GET_HOTELS = 9





