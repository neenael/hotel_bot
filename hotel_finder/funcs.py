from loader import bot
from keyboards.reply import buttons
from query import rapidapi_hotels
from telebot.types import ReplyKeyboardRemove, Message
from translate import Translator
from database.db_connection import *
from calibration.tools import *
from states.information import *
from typing import Union

translator = Translator(from_lang='ru', to_lang='en')


def command_init(message: Message, mode: str) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['mode'] = mode
        if not data.get('start_date'):
            today = datetime.datetime.now()
            data['start_date'] = {'year': today.year, 'month': today.month, 'day': today.day}
            data['end_date'] = dict()
        data['request_time'] = '{}:{}'.format(date_validation(datetime.datetime.now().hour),
                                              date_validation(datetime.datetime.now().minute))
        data['request_date'] = '{}-{}-{}'.format(datetime.datetime.today().year, datetime.datetime.today().month,
                                                 datetime.datetime.today().day)
        bot.send_message(message.chat.id, 'Выберите год заселения',
                         reply_markup=buttons.create_years_keyboard(data['start_date']))


def get_checkin_year(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    error = False
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == '→':
            data['start_date']['year'] += 3
            change_years(message, data)
        elif message.text.isdigit():
            if int(message.text) >= data['start_date']['year']:
                bot.set_state(message.from_user.id, state.check_in_month, message.chat.id)
                if data['start_date']['year'] != int(message.text):
                    data['start_date']['year'] = int(message.text)
                    data['start_date']['month'] = 1
                    data['start_date']['day'] = 1
                bot.send_message(message.chat.id, 'Выберите месяц заселения',
                                 reply_markup=buttons.get_month_to_checkin(data['start_date']))
            else:
                error = True
        else:
            error = True

        if error:
            bot.send_message(message.chat.id, 'Ошибка ввода!\nВыберите год заселения',
                             reply_markup=buttons.create_years_keyboard(data['start_date']))


def change_years(message: Message, data: dict) -> None:
    bot.send_message(message.chat.id, 'Выберите год заселения',
                     reply_markup=buttons.create_years_keyboard(data['start_date']))


def get_chekcin_month(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    months_nums = {'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6, 'Июль': 7,
                   'Август': 8, 'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12}
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.title() in get_valid_months(data['start_date']):
            bot.set_state(message.from_user.id, state.check_in_day, message.chat.id)
            data['start_date']['month'] = months_nums.get(message.text)
            bot.send_message(message.chat.id, 'Выберите день заезда',
                             reply_markup=buttons.get_days_to_checkin(data['start_date']))
        else:
            bot.send_message(message.chat.id, 'Ошибка ввода!\nВыберите месяц заселения',
                             reply_markup=buttons.get_month_to_checkin(data['start_date']))


def get_checkin_day(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    error = False
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        today = datetime.datetime.today()
        valid_days = get_days_list(data['start_date'], {'year': today.year, 'month': today.month, 'day': today.day})
        if message.text.isdigit():
            if int(message.text) in valid_days:
                data['start_date']['day'] = int(message.text)
                data['end_date'] = data['start_date'].copy()
                bot.set_state(message.from_user.id, state.check_out_year, message.chat.id)
                bot.send_message(message.chat.id, 'Выберите год выезда',
                                 reply_markup=buttons.create_years_keyboard(data['end_date']))
            else:
                error = True
        else:
            error = True
        if error:
            bot.send_message(message.chat.id, 'Ошибка ввода!\nВыберите день заезда',
                             reply_markup=buttons.get_days_to_checkin(data['start_date']))


def get_checkout_year(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    error = False
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == '→':
            data['start_date']['year'] += 3
            change_years(message, data)
        elif message.text.isdigit():
            if int(message.text) >= data['end_date']['year']:
                bot.set_state(message.from_user.id, state.check_out_month, message.chat.id)
                if data['end_date']['year'] != int(message.text):
                    data['end_date']['year'] = int(message.text)
                    data['end_date']['month'] = 1
                    data['end_date']['day'] = 1
                bot.send_message(message.chat.id, 'Выберите месяц выезда',
                                 reply_markup=buttons.get_month_to_checkout(data['start_date'], data['end_date']))
            else:
                error = True
        else:
            error = True
        if error:
            bot.send_message(message.chat.id, 'Ошибка ввода!\nВыберите год выезда',
                             reply_markup=buttons.create_years_keyboard(data['end_date']))


def get_checkout_month(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    months_nums = {'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6, 'Июль': 7,
                   'Август': 8, 'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12}
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.title() in get_valid_months(data['end_date']):
            bot.set_state(message.from_user.id, state.check_out_day, message.chat.id)
            if (data['start_date']['year'] < data['end_date']['year'] and
                    data['start_date']['month'] < data['end_date']['month']):
                data['end_date']['month'] = months_nums.get(message.text)
                data['end_date']['day'] = 1
            data['end_date']['month'] = months_nums.get(message.text)
            bot.send_message(message.chat.id, 'Выберите день выезда',
                             reply_markup=buttons.get_days_to_checkout(data['start_date'], data['end_date']))
        else:
            bot.send_message(message.chat.id, 'Ошибка ввода!\nВыберите месяц выезда',
                             reply_markup=buttons.get_month_to_checkout(data['start_date'], data['end_date']))


def get_checkout_day(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    error = False
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        valid_days = get_days_list(data['start_date'], data['end_date'])
        if message.text.isdigit():
            if int(message.text) in valid_days:
                data['end_date']['day'] = int(message.text)
                bot.set_state(message.from_user.id, state.city_name, message.chat.id)
                bot.send_message(message.chat.id, 'Введите город', reply_markup=ReplyKeyboardRemove())
            else:
                error = True
        else:
            error = True
        if error:
            bot.send_message(message.chat.id, 'Ошибка ввода!\nВыберите день выезда',
                             reply_markup=buttons.get_days_to_checkout(data['start_date'], data['end_date']))


def get_city(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    try:
        error = False
        msg = bot.send_message(message.chat.id, '_Поиск города..._', parse_mode='Markdown')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            resp = rapidapi_hotels.city_search(translator.translate(message.text.title()))
            if resp:
                bot.edit_message_text(text='Готово✅\nГород поиска - {}'.format(resp['city_name']),
                                      message_id=msg.message_id, chat_id=message.chat.id)
                data['city_users'] = message.text.title()
                data['city_en'] = translator.translate(data['city_users'])
                data['destination_id'] = resp['destination_id']
                data['hotel_list'] = rapidapi_hotels.get_hotels(data)
                bot.send_message(message.chat.id, '*Нашлось {} {}*\n'
                                                  'Сколько из них вывести?'.format(len(data['hotel_list']),
                                                                                   hotel_word(len(data['hotel_list']))),
                                 reply_markup=buttons.num_hotel_suggestion(max_num=len(data['hotel_list'])),
                                 parse_mode='Markdown')
                bot.set_state(message.from_user.id, state.property_search, message.chat.id)
            else:
                error = True

            if error:
                bot.edit_message_text(text='Ошибка⛔️\nТакого города не нашлось',
                                      message_id=msg.message_id, chat_id=message.chat.id)
                bot.send_message(message.chat.id, 'Введите город')
    except [KeyError, TypeError]:
        bot.send_message(message.chat.id, 'Извините, похоже подходящих отелей не нашлось')


def get_city_for_bestdeal(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    try:
        error = False
        msg = bot.send_message(message.chat.id, '_Поиск города..._', parse_mode='Markdown')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            resp = rapidapi_hotels.city_search(translator.translate(message.text.title()))
            if resp:
                bot.edit_message_text(text='Готово✅\nГород поиска - {}'.format(resp['city_name']),
                                      message_id=msg.message_id, chat_id=message.chat.id)
                data['city_users'] = message.text.title()
                data['city_en'] = translator.translate(data['city_users'])
                data['destination_id'] = resp['destination_id']
                data['hotel_list'] = rapidapi_hotels.get_hotels(data)
                bot.set_state(message.from_user.id, state.price_range, message.chat.id)
                try:
                    data['hotel_list'].sort(key=lambda x: float(x.get('ratePlan').get('price').get('current')[1:]))
                except ValueError:
                    data['hotel_list'].sort(
                        key=lambda x: float('.'.join(x.get('ratePlan').get('price').get('current')[1:].split(',')))
                    )
                except AttributeError:
                    pass
                data['min_price'] = number_validation(data['hotel_list'][0]['ratePlan']['price']['current'][1:])
                data['max_price'] = number_validation(data['hotel_list'][-1]['ratePlan']['price']['current'][1:])
                bot.send_message(message.chat.id, 'Введите диапазон цен (от {} до {}).'
                                                  ' Вы можете воспользоваться предложениями снизу или '
                                                  'ввести диапазон вручную в формате'
                                                  ' "мин - макс"'.format(data['min_price'], data['max_price']),
                                 reply_markup=buttons.price_range_suggestions(data['min_price'], data['max_price']))
            else:
                error = True

            if error:
                bot.edit_message_text(text='Ошибка⛔️\nТакого города не нашлось', message_id=msg.message_id,
                                      chat_id=message.chat.id)
                bot.send_message(message.chat.id, 'Введите город')
    except KeyError:
        bot.send_message(message.chat.id, 'Извините, похоже подходящих отелей не нашлось')


def get_price_range(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.set_state(message.from_user.id, state.distance_range, message.chat.id)
        data['min_price'], data['max_price'] = range_converter(message.text)

        data['hotel_list'].sort(key=lambda x: float(x['landmarks'][0]['distance'].split()[0]))
        data['min_distance'] = number_validation(
            data['hotel_list'][0]['landmarks'][0]['distance'].split()[0])
        data['max_distance'] = number_validation(
            data['hotel_list'][-1]['landmarks'][0]['distance'].split()[0])

        bot.send_message(message.chat.id,
                         'Введите диапазон расстояния от центра города (от {} до {}). '
                         'Вы можете воспользоваться предложениями снизу или ввести диапазон'
                         ' вручную в формате "мин - макс"'.format(data['min_distance'],
                                                                  data['max_distance']),
                         reply_markup=buttons.distance_range_suggestions(data['min_distance'],
                                                                         data['max_distance']))


def get_distance_range(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.set_state(message.from_user.id, state.property_search, message.chat.id)
        data['min_distance'], data['max_distance'] = range_converter(message.text)
        data['hotel_list'] = list_with_options(data['hotel_list'], data['min_price'], data['max_price'],
                                               data['min_distance'], data['max_distance'])

        bot.send_message(message.chat.id, '*Нашлось {} {}*\n'
                                          'Сколько из них вывести?'.format(len(data['hotel_list']),
                                                                           hotel_word(len(data['hotel_list']))),
                         reply_markup=buttons.num_hotel_suggestion(max_num=len(data['hotel_list'])),
                         parse_mode='Markdown')


def get_hotels_amount(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    error = False
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit:
            if int(message.text) <= len(data['hotel_list']):
                bot.set_state(message.from_user.id, state.photos_necessity, message.chat.id)
                data['num_hotels_output'] = int(message.text)
                bot.send_message(message.chat.id, 'Нужно ли приложить фото для каждого из отелей?',
                                 reply_markup=buttons.yes_or_no())
            else:
                error = True
        else:
            error = True
        if error:
            bot.send_message(message.chat.id,
                             'Ошибка ввода!\nВведите количество отелей (не более {})'.format(len(data['hotel_list'])),
                             reply_markup=buttons.num_hotel_suggestion(max_num=len(data['hotel_list'])))


def get_photos_necessity(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.title() == 'Да':
            data['photos_necessity'] = True
            bot.set_state(message.from_user.id, state.photos_amount, message.chat.id)
            bot.send_message(message.chat.id, 'Введите количество фото (до 10)',
                             reply_markup=buttons.num_photo_suggestion())
        elif message.text.title() == 'Нет':
            data['photos_necessity'] = False
        else:
            bot.send_message(message.chat.id, 'Ошибка ввода!\nНужно ответить либо "Да", либо "Нет"',
                             reply_markup=buttons.yes_or_no())

    if message.text.title() == 'Нет':
        output(message, state)


def get_photos_num(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    error = False
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            if 0 < int(message.text) <= 10:
                data['photos_num'] = int(message.text)
            else:
                error = True
        else:
            error = True

    if error:
        bot.send_message(message.chat.id, 'Ошибка ввода!\nВведите количество фото (от 1 до 10)',
                         reply_markup=buttons.num_photo_suggestion())
    else:
        output(message, state)


def output(message: Message, state: Union[LowpriceStates, HihgpriceStates, BestdealStates]) -> None:
    msg = bot.send_message(message.chat.id, '_Загрузка..._', parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
    is_deleted = False

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['hotel_list'] = rapidapi_hotels.get_properties_list(data, data['hotel_list'])
        text = []

        start_date = datetime.date(day=int(data['start_date']['day']), month=int(data['start_date']['month']),
                                   year=int(data['start_date']['year']))
        end_date = datetime.date(day=int(data['end_date']['day']), month=int(data['end_date']['month']),
                                 year=int(data['end_date']['year']))
        summary_days = abs(end_date - start_date)

        for hotel in data['hotel_list']:
            text.append('*{}*'.format(hotel['name']))
            text.append('⭐' * hotel['stars'])
            text.append('Адрес: {}'.format(hotel['address']))
            text.append('Расстояние до центра города: {}'.format(hotel['city_center']))
            text.append('Цена за сутки: ${}'.format(hotel['cost']))
            text.append('Цена за период с {}.{}.{} по {}.{}.{} ({} сут.): ${}'.format(data['start_date']['year'],
                                                                                      data['start_date']['month'],
                                                                                      data['start_date']['day'],
                                                                                      data['end_date']['year'],
                                                                                      data['end_date']['month'],
                                                                                      data['end_date']['day'],
                                                                                      summary_days.days,
                                                                                      hotel['cost'] * summary_days.days
                                                                                      ))
            if not is_deleted:
                is_deleted = True
                bot.delete_message(message.chat.id, msg.id)

            if data['photos_necessity']:
                hotel['photos_list'][0].caption = '\n'.join(text)
                hotel['photos_list'][0].parse_mode = 'Markdown'
                bot.send_media_group(message.chat.id, hotel['photos_list'])
            else:
                bot.send_message(message.chat.id, '\n'.join(text), parse_mode="Markdown",
                                 reply_markup=ReplyKeyboardRemove())
            text.clear()
        with db:
            Request.create(telegram_id=message.from_user.id,
                           request_time=data.get('request_time'),
                           request_date=data.get('request_date'),
                           checkin='-'.join(map(str, data['start_date'].values())),
                           checkout='-'.join(map(str, data['end_date'].values())),
                           mode=data.get('mode'),
                           location_id=data.get('destination_id'),
                           city_en=data.get('city_en'),
                           city_ru=data.get('city_users'),
                           hotels_num=data.get('num_hotels_output'),
                           photo_nes=data.get('photos_necessity'),
                           photos_num=data.get('photos_num'),
                           min_price=data.get('min_price'),
                           max_price=data.get('max_price'),
                           min_distance=data.get('min_distance'),
                           max_distance=data.get('max_distance'))
        data.clear()
    bot.set_state(message.from_user.id, state.neutral_status, message.chat.id)
