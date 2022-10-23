from hotel_finder.funcs import *
from telebot.types import Message


@bot.message_handler(commands=['bestdeal'])
def best_init(message: Message) -> None:
    bot.set_state(message.from_user.id, BestdealStates.check_in_year, message.chat.id)
    command_init(message, 'BEST_SELLER')


@bot.message_handler(state=BestdealStates.check_in_year)
def bd_checkin_year(message: Message) -> None:
    get_checkin_year(message, BestdealStates)


@bot.message_handler(state=BestdealStates.check_in_month)
def bd_checkin_month(message: Message) -> None:
    get_chekcin_month(message, BestdealStates)


@bot.message_handler(state=BestdealStates.check_in_day)
def bd_checkin_day(message: Message) -> None:
    get_checkin_day(message, BestdealStates)


@bot.message_handler(state=BestdealStates.check_out_year)
def bd_checkout_year(message: Message) -> None:
    get_checkout_year(message, BestdealStates)


@bot.message_handler(state=BestdealStates.check_out_month)
def bd_checkout_month(message: Message) -> None:
    get_checkout_month(message, BestdealStates)


@bot.message_handler(state=BestdealStates.check_out_day)
def bd_checkout_day(message: Message) -> None:
    get_checkout_day(message, BestdealStates)


@bot.message_handler(state=BestdealStates.city_name)
def bd_city_input(message: Message) -> None:
    get_city_for_bestdeal(message, BestdealStates)


@bot.message_handler(state=BestdealStates.price_range)
def price_range(message: Message) -> None:
    get_price_range(message, BestdealStates)


@bot.message_handler(state=BestdealStates.distance_range)
def distance_range(message: Message) -> None:
    get_distance_range(message, BestdealStates)


@bot.message_handler(state=BestdealStates.property_search)
def bd_hotels_amount(message: Message) -> None:
    get_hotels_amount(message, BestdealStates)


@bot.message_handler(state=BestdealStates.photos_necessity)
def bd_photos_necessity(message: Message) -> None:
    get_photos_necessity(message, BestdealStates)


@bot.message_handler(state=BestdealStates.photos_amount)
def bd_photos_num(message: Message) -> None:
    get_photos_num(message, BestdealStates)
