# 5128476850:AAHf5Phs_UGRpfdJzElovnKd7Yy1WuMCwjY
import os

from telebot import (
    TeleBot,
    types
)


from bot.utils import validate
from hotels_api import HotelsAPI
from constants import FUNC_MAPPER
from msg_templates import (
    HELP,
    TYPE_CITY,
    BOOKING_NAME,
)

TELEGRAM_API_KEY = "5307876588:AAGcDCiuMEAsaIMFDJKWCeEbauLwbKVdoFM"
bot = TeleBot(TELEGRAM_API_KEY)
api = HotelsAPI()
booking_data = {}


# /help
@bot.message_handler(commands=["help"])
def help_handler(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=HELP.format(message.from_user.first_name)
    )


# /hotels
@bot.message_handler(commands=["hotels"])
def get_hotel_first_stage(message: types.Message):
    msg = bot.send_message(message.chat.id, TYPE_CITY)
    bot.register_next_step_handler(msg, get_hotels_by_city)


def get_hotels_by_city(msg: types.Message):
    print(f"Get Hotels By City: {msg}")
    city = msg.text
    hotels = api.get_hotels_by_city(city=city)
    print(f"Hotels: {hotels}")
    if hotels:
        [bot.send_message(msg.chat.id, str(hotel)) for hotel in hotels]


# /book_hotel
@bot.message_handler(commands=["book_hotel"])
def book_hotel_entry(msg: types.Message):
    print('Start Booking')
    msg = bot.send_message(msg.chat.id, BOOKING_NAME)
    bot.register_next_step_handler(
        msg,
        lambda msg: book_hotel(msg, "get_name")
    )


def book_hotel(msg: types.Message, current_func):
    print('book_hotel func was called')
    user_id = msg.from_user.id
    chat_id = msg.chat.id

    previous_func = FUNC_MAPPER[current_func].get("previous_func")
    previous_msg = FUNC_MAPPER[previous_func]["ok_msg"]

    print(f"\n[Current]:{current_func}\n[Previous]:{previous_func}\n[Message]:{msg.text}")

    validate(msg, current_func, FUNC_MAPPER)

    current_msg = FUNC_MAPPER[current_func]["ok_msg"]
    err_msg = FUNC_MAPPER[current_func]["err_msg"]
    dict_key = FUNC_MAPPER[current_func]["dict_key"]
    next_func = FUNC_MAPPER[current_func]["next_func"]

    if err_msg:
        next_func = current_func
        current_msg = f"{err_msg}\n{previous_msg}"
    else:
        booking_data.setdefault(user_id, {})[dict_key] = msg.text

    print(f"Booking data: {booking_data}")
    msg = bot.send_message(msg.chat.id, current_msg)
    if not next_func:
        make_reservation(user_id, chat_id)
    register_next_func(next_func=next_func, msg=msg)


def register_next_func(next_func, msg):
    print(f"[Next Function]: {next_func}")
    bot.register_next_step_handler(
        msg,
        lambda msg: book_hotel(msg, next_func)
    )


def make_reservation(user_id: int, chat_id: int):
    user_booking_data = booking_data.get(user_id, {})
    res = HotelsAPI.make_reservation(user_booking_data)
    bot.send_message(chat_id, res)
    booking_data.clear()


if __name__ == "__main__":
    print("Bot is pooling ... 🤖")
    bot.infinity_polling()
