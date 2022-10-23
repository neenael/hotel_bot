from typing import Union
from datetime import date
from calendar import monthrange
import datetime

def range_converter(line: str) -> list:
    line = line.split('-')
    result = []
    for section in line:
        number = list(section)
        while ' ' in number:
            number.remove(' ')
        while '$' in number:
            number.remove('$')
        number = ''.join(number)
        try:
            result.append(int(number))
        except ValueError:
            result.append(float(number))

    if not(0 <= result[0] <= result[1]):
        raise ValueError

    return result


def number_validation(num: Union[int, float, str, any]) -> Union[int, float]:
    if isinstance(num, int):
        return num
    if isinstance(num, float):
        return round(num, 1)
    if isinstance(num, str):
        if num.isdigit():
            return int(num)
        if '.' in num:
            return round(float(num), 1)
        if ',' in num:
            return round(float('.'.join(num.split(','))), 1)
    return 0


def get_the_mode(mode: str) -> str:
    if mode == 'PRICE':
        return 'Дешевые отели'
    if mode == 'PRICE_HIGHEST_FIRST':
        return 'Дорогие отели'
    if mode == 'BEST_SELLER':
        return 'Выгодные отели'


def reformat_date(date_str: date) -> str:
    months = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
              'ноября', 'декабря']
    return '{} {} {}'.format(int(date_str.day), months[int(date_str.month)], int(date_str.year))


def clean(list_items: list) -> list:
    result = []
    for item in list_items:
        try:
            if item['ratePlan']['price']['current']:
                result.append(item)
        except KeyError:
            pass
    return result


def date_validation(number: int) -> str:
    number = str(number)
    if len(number) == 1:
        return '0' + number
    return number


def list_with_options(hotel_list: list, min_price: Union[int, float, str, any], max_price: Union[int, float, str, any],
                      min_distance: Union[int, float, str, any], max_distance: Union[int, float, str, any]):
    sorted_hotel_list = []
    for hotel in hotel_list:
        try:
            if (number_validation(min_price) <= number_validation(
                    hotel.get('ratePlan').get('price').get('current')[1:]) <= number_validation(max_price) and
                    number_validation(min_distance) <= number_validation(
                        hotel['landmarks'][0]['distance'].split()[0]) <= number_validation(max_distance)):
                sorted_hotel_list.append(hotel)
        except AttributeError:
            pass
    return sorted_hotel_list


def get_days_list(start_date: dict, end_date: dict) -> list:
    days_num = monthrange(year=start_date['year'], month=start_date['month'])[1]
    if start_date['year'] == end_date['year'] and start_date['month'] == end_date['month']:
        start_day = start_date['day']
    else:
        start_day = 1
    return list(range(start_day, days_num + 1))


def get_valid_months(date: dict) -> str:
    months_nums = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                   'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    month_name = months_nums[date['month']:]
    return month_name


def hotel_word(number: int) -> str:
    if number == 1:
        return 'отель'
    if 2 <= number <= 4:
        return 'отеля'
    return 'отелей'
