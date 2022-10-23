from hotel_finder.funcs import *
from telebot.types import Message


@bot.message_handler(commands=['highprice'])
def highprice_init(message: Message) -> None:
    bot.set_state(message.from_user.id, HihgpriceStates.check_in_year, message.chat.id)
    command_init(message, 'PRICE_HIGHEST_FIRST')


@bot.message_handler(state=HihgpriceStates.check_in_year)
def hp_checkin_year(message: Message) -> None:
    get_checkin_year(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.check_in_month)
def hp_checkin_month(message: Message) -> None:
    get_chekcin_month(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.check_in_day)
def hp_checkin_day(message: Message) -> None:
    get_checkin_day(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.check_out_year)
def hp_checkout_year(message: Message) -> None:
    get_checkout_year(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.check_out_month)
def hp_checkout_month(message: Message) -> None:
    get_checkout_month(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.check_out_day)
def hp_checkout_day(message: Message) -> None:
    get_checkout_day(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.city_name)
def hp_city_input(message: Message) -> None:
    get_city(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.property_search)
def hp_hotels_amount(message: Message) -> None:
    get_hotels_amount(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.photos_necessity)
def hp_photos_necessity(message: Message) -> None:
    get_photos_necessity(message, HihgpriceStates)


@bot.message_handler(state=HihgpriceStates.photos_amount)
def hp_photos_num(message: Message) -> None:
    get_photos_num(message, HihgpriceStates)
