DELIMITERS = [":", "-", ".", "/", " "]
DATE_TEMPLATES = [f"%d{delimiter}%m{delimiter}%Y" for delimiter in DELIMITERS]
DJANGO_DATE_FORMAT = "%Y-%m-%d"

FUNC_MAPPER = {
    None: {
        "previous_func": None,
        "next_func": "get_name",
        "dict_key": None,
        "ok_msg": "",
        "err_msg": "",
        "validators": []
    },
    "get_name": {
        "previous_func": None,
        "next_func": "get_booking_start",
        "dict_key": "guest_name",
        "ok_msg": "Set Booking start [dd/mm/yyyy]",
        "err_msg": "",
        "validators": []
    },
    "get_booking_start": {
        "previous_func": "get_name",
        "next_func": "get_booking_end",
        "dict_key": "booking_start",
        "ok_msg": "Set Booking end [dd/mm/yyyy]",
        "err_msg": "",
        "validators": ["date_validator"]
    },
    "get_booking_end": {
        "previous_func": "get_booking_start",
        "next_func": "get_persons",
        "dict_key": "booking_end",
        "ok_msg": "How many persons will stay?",
        "err_msg": "",
        "validators": ["date_validator"]
    },
    "get_persons": {
        "previous_func": "get_booking_end",
        "next_func": "get_city",
        "dict_key": "persons",
        "ok_msg": "What city you want to stay?",
        "err_msg": "",
        "validators": ["persons_validator"]
    },
    "get_city": {
        "previous_func": "get_persons",
        "next_func": "get_hotel",
        "dict_key": "city",
        "ok_msg": "What hotel did you choose?",
        "err_msg": "",
        "validators": ["city_validator"]
    },
    "get_hotel": {
        "previous_func": "get_city",
        "next_func": None,
        "dict_key": "hotel",
        "ok_msg": "We are finding a hotel for you parameters",
        "err_msg": "",
        "validators": ['hotel_in_city_validator']
    },
}
