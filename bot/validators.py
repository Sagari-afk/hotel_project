from datetime import datetime
from typing import Union

from constants import DATE_TEMPLATES
from hotels_api import HotelsAPI

# TODO check that booking_end is not lower or not equal to booking_start
date_data = {}


def persons_validator(validate_persons_amount: str) -> Union[None, str]:
    try:
        persons_int = int(validate_persons_amount.strip())
    except ValueError:
        return f"err: unsupported (not integer) data format: {validate_persons_amount}"

    if 5 > persons_int > 0:
        return None
    else:
        return f"err: too many persons: {persons_int}"


def date_validator(validate_date: str, user_id) -> Union[None, str]:
    today = datetime.now()
    for date_template in DATE_TEMPLATES:
        try:
            booking_date = datetime.strptime(validate_date, date_template)
            if booking_date > today:
                print(f"date: {validate_date} successfully validated")
                return None
            else:
                return f"err: we need time machine here: {validate_date}"
        except ValueError:
            print(f"{validate_date} incorrect data format for template: {date_template}")
    return f"err: unsupported date format: {validate_date}"


def booking_end_validator(validate_date: str) -> Union[None, str]:
    pass


def city_validator(validate_city: str) -> Union[None, str]:
    cities: list = HotelsAPI.get_cities()
    if validate_city.strip() in cities:
        return None
    else:
        return f"err: unsupported city: {validate_city}  -  we don't have hotels in this city"


# TODO Check if Hotel exist in User' chosen city
def hotel_in_city_validator(validate_hotel: str) -> Union[None, str]:
    pass


if __name__ == "__main__":
    for test_data in [
        "26051988",
        "26.05.1988",
        "26/05/1988",
        "08-05-2022",
        "26:05:2022",
        "26 05 1988"
    ]:
        print(date_validator(test_data))
