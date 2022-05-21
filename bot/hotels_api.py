import requests
from datetime import datetime

from constants import (
    DATE_TEMPLATES,
    DJANGO_DATE_FORMAT,
)


class HotelsAPI:
    URL = "http://127.0.0.1:8000/hotels/api"

    @staticmethod
    def date_transform(booking_data):
        # TODO Try to granulate below code
        for booking_date in ["booking_start", "booking_end"]:
            for date_format in DATE_TEMPLATES:
                try:
                    bot_format_date = booking_data[booking_date]
                    obj_date = datetime.strptime(bot_format_date, date_format)
                    django_format_date = datetime.strftime(obj_date, DJANGO_DATE_FORMAT)
                    booking_data[booking_date] = django_format_date
                    break
                except ValueError:
                    continue

    @staticmethod
    def get_hotels_by_city(city):
        API_URL = f"{HotelsAPI.URL}/hotels"
        res = requests.get(API_URL, params={"city": city}).json()
        return res

    @staticmethod
    def get_cities():
        API_URL = f"{HotelsAPI.URL}/cities"
        res: list = requests.get(API_URL).json()
        return res

    @staticmethod
    def make_reservation(booking_data):
        API_URL = f"{HotelsAPI.URL}/booking/"
        HotelsAPI.date_transform(booking_data)
        print(f"Making reservation with user data {booking_data}")
        res = requests.post(API_URL, json=booking_data)
        return res
