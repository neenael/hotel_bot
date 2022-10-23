from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from calibration.tools import *


def create_years_keyboard(start_date: dict) -> ReplyKeyboardMarkup:
    years = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    min_year = start_date['year']
    years.add(KeyboardButton(str(min_year)),
              KeyboardButton(str(min_year + 1)),
              KeyboardButton(str(min_year + 2)),
              KeyboardButton('→'))
    return years


def get_month_to_checkin(start_date: dict) -> ReplyKeyboardMarkup:
    months_list = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                   'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    if start_date['year'] == datetime.datetime.today().year:
        months_list = months_list[start_date['month']:]

    months = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    while len(months_list) >= 3:
        months.row(KeyboardButton(months_list.pop(0)),
                   KeyboardButton(months_list.pop(0)),
                   KeyboardButton(months_list.pop(0)))
    if len(months_list) == 2:
        months.row(KeyboardButton(months_list.pop(0)), KeyboardButton(months_list.pop(0)))
    elif len(months_list) == 1:
        months.row(KeyboardButton(months_list.pop(0)))

    return months


def get_month_to_checkout(min_date: dict, end_date: dict) -> ReplyKeyboardMarkup:
    months_list = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                   'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    if end_date['year'] == min_date['year']:
        months_list = months_list[min_date['month']:]

    months = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    while len(months_list) >= 3:
        months.row(KeyboardButton(months_list.pop(0)),
                   KeyboardButton(months_list.pop(0)),
                   KeyboardButton(months_list.pop(0)))
    if len(months_list) == 2:
        months.row(KeyboardButton(months_list.pop(0)), KeyboardButton(months_list.pop(0)))
    elif len(months_list) == 1:
        months.row(KeyboardButton(months_list.pop(0)))
    return months


def get_days_to_checkin(start_date: dict) -> ReplyKeyboardMarkup:
    days_num = monthrange(year=start_date['year'], month=start_date['month'])[1]
    if start_date['year'] == datetime.datetime.today().year and start_date['month'] == datetime.datetime.today().month:
        start_day = start_date['day']
    else:
        start_day = 1
    days = ReplyKeyboardMarkup(resize_keyboard=True)
    days_list = list(range(start_day, days_num + 1))
    while len(days_list) >= 5:
        days.row(KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)))

    if len(days_list) == 4:
        days.row(KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)))
    elif len(days_list) == 3:
        days.row(KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)))
    elif len(days_list) == 2:
        days.row(KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)))
    elif len(days_list) == 1:
        days.row(KeyboardButton(days_list.pop(0)))

    return days


def get_days_to_checkout(min_date: dict, end_date: dict) -> ReplyKeyboardMarkup:
    days_num = monthrange(year=end_date['year'], month=end_date['month'])[1]
    if end_date['year'] == min_date['year'] and end_date['month'] == min_date['month']:
        start_day = end_date['day']
    else:
        start_day = 1
    days = ReplyKeyboardMarkup(resize_keyboard=True)
    days_list = list(range(start_day, days_num + 1))
    while len(days_list) >= 5:
        days.row(KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)))

    if len(days_list) == 4:
        days.row(KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)))
    elif len(days_list) == 3:
        days.row(KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)))
    elif len(days_list) == 2:
        days.row(KeyboardButton(days_list.pop(0)),
                 KeyboardButton(days_list.pop(0)))
    elif len(days_list) == 1:
        days.row(KeyboardButton(days_list.pop(0)))

    return days


def yes_or_no() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Да'), KeyboardButton('Нет'))
    return keyboard


def num_hotel_suggestion(max_num=25) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if max_num == 25:
        keyboard.add(KeyboardButton('3'), KeyboardButton('5'), KeyboardButton('10'))
    elif 3 <= max_num < 25:
        keyboard.add(KeyboardButton(str(max_num//3)), KeyboardButton(str(max_num//3*2)), KeyboardButton(str(max_num)))
    elif max_num == 2:
        keyboard.add(KeyboardButton(str(max_num // 2)), KeyboardButton(str(max_num)))
    elif max_num == 1:
        keyboard.add(KeyboardButton(str(max_num)))
    return keyboard


def num_photo_suggestion(max_num=10) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if max_num == 10:
        keyboard.add(KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('5'))
    elif 3 <= max_num < 10:
        keyboard.add(KeyboardButton(str(max_num//3)), KeyboardButton(str(max_num//3*2)), KeyboardButton(str(max_num)))
    elif max_num == 2:
        keyboard.add(KeyboardButton(str(max_num // 2)), KeyboardButton(str(max_num)))
    elif max_num == 1:
        keyboard.add(KeyboardButton(str(max_num)))
    return keyboard


def price_range_suggestions(min_price: Union[int, float], max_price: Union[int, float]) -> ReplyKeyboardMarkup:
    suggestions = ReplyKeyboardMarkup(resize_keyboard=True)
    middle_price = number_validation((min_price + max_price) / 2)
    suggestions.add(
        KeyboardButton('${} - ${}'.format(min_price, middle_price)),
        KeyboardButton('${} - ${}'.format(middle_price, max_price))
    )
    return suggestions


def distance_range_suggestions(min_distance: Union[int, float], max_distance: Union[int, float]) -> ReplyKeyboardMarkup:
    suggestions = ReplyKeyboardMarkup(resize_keyboard=True)
    middle_range = number_validation((min_distance + max_distance) / 2)
    suggestions.add(
        KeyboardButton('{} - {}'.format(min_distance, middle_range)),
        KeyboardButton('{} - {}'.format(middle_range, max_distance))
    )
    return suggestions
