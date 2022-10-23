from hotel_finder.funcs import *
from telebot.types import Message


@bot.message_handler(commands=['lowprice'])
def lowprice_init(message: Message) -> None:
    bot.set_state(message.from_user.id, LowpriceStates.check_in_year, message.chat.id)
    command_init(message, 'PRICE')


@bot.message_handler(state=LowpriceStates.check_in_year)
def lp_checkin_year(message: Message) -> None:
    get_checkin_year(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.check_in_month)
def lp_checkin_month(message: Message) -> None:
    get_chekcin_month(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.check_in_day)
def lp_checkin_day(message: Message) -> None:
    get_checkin_day(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.check_out_year)
def lp_checkout_year(message: Message) -> None:
    get_checkout_year(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.check_out_month)
def lp_checkout_month(message: Message) -> None:
    get_checkout_month(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.check_out_day)
def lp_checkout_day(message: Message) -> None:
    get_checkout_day(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.city_name)
def lp_city(message: Message) -> None:
    get_city(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.property_search)
def lp_hotels_amount(message: Message) -> None:
    get_hotels_amount(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.photos_necessity)
def lp_photos_necessity(message: Message) -> None:
    get_photos_necessity(message, LowpriceStates)


@bot.message_handler(state=LowpriceStates.photos_amount)
def lp_photos_num(message: Message) -> None:
    get_photos_num(message, LowpriceStates)
