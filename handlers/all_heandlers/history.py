from loader import bot
from database.db_connection import *
from query import rapidapi_hotels
from telebot.types import ReplyKeyboardRemove, Message, CallbackQuery
from keyboards.inline.buttons import *
from calibration.tools import *


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    with db:
        is_empty = True
        for request in Request.select().where(Request.telegram_id == message.from_user.id):
            is_empty = False
            request_button = InlineKeyboardMarkup()
            request_button.add(InlineKeyboardButton(text='Перейти к запросу', callback_data=request.id))
            bot.send_message(message.chat.id, '📍*{city}*\n'
                                              '_{date1} - {date2}_\n'
                                              '{mode}\n'
                                              'Запрос от _{request_date}'
                                              ' ({time})_'.format(city=request.city_ru,
                                                                  date1=reformat_date(request.checkin),
                                                                  date2=reformat_date(request.checkout),
                                                                  mode=get_the_mode(request.mode),
                                                                  request_date=reformat_date(request.request_date),
                                                                  time=request.request_time),
                             reply_markup=request_button, parse_mode='Markdown')

    if is_empty:
        bot.send_message(message.chat.id, 'История поиска пуста')
    else:
        bot.send_message(message.chat.id, 'Очистить историю поиска', reply_markup=basket())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: CallbackQuery) -> None:
    with db:
        if call.data == 'delete_history':
            for request in Request.select().where(Request.telegram_id == int(call.from_user.id)):
                request.delete_instance()
            bot.send_message(call.message.chat.id, 'История поиска очищена')
        else:

            for request in Request.select().where(Request.id == int(call.data)):

                msg = bot.send_message(call.message.chat.id, '_Загрузка..._', parse_mode='Markdown',
                                       reply_markup=ReplyKeyboardRemove())
                is_deleted = False

                data = {'destination_id': request.location_id,
                        'start_date':
                            {'year': request.checkin.year,
                             'month': request.checkin.month,
                             'day': request.checkin.day},
                        'end_date':
                            {'year': request.checkout.year,
                             'month': request.checkout.month,
                             'day': request.checkout.day},
                        'mode': request.mode,
                        'num_hotels_output': request.hotels_num,
                        'photos_necessity': request.photo_nes,
                        'photos_num': request.photos_num,
                        'request_time': '{}:{}'.format(datetime.datetime.now().hour,
                                                       datetime.datetime.now().minute),
                        'request_date': '{}-{}-{}'.format(datetime.datetime.today().year,
                                                          datetime.datetime.today().month,
                                                          datetime.datetime.today().day),
                        'city_en': request.city_en,
                        'city_users': request.city_ru,
                        'min_price': request.min_price,
                        'max_price': request.max_price,
                        'min_distance': request.min_distance,
                        'max_distance': request.max_distance
                        }

                data['hotel_list'] = rapidapi_hotels.get_hotels(data)
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
                    text.append('Цена за сутки: {}'.format(hotel['cost']))
                    text.append('Цена за период с {}.{}.{} по {}.{}.{}'
                                ' ({} суток): ${}'.format(data['start_date']['year'],
                                                          data['start_date']['month'],
                                                          data['start_date']['day'],
                                                          data['end_date']['year'],
                                                          data['end_date']['month'],
                                                          data['end_date']['day'], summary_days.days,
                                                          hotel['cost'] * summary_days.days))
                    if not is_deleted:
                        is_deleted = True
                        bot.delete_message(call.message.chat.id, msg.id)

                    if data['photos_necessity']:
                        hotel['photos_list'][0].caption = '\n'.join(text)
                        hotel['photos_list'][0].parse_mode = 'Markdown'
                        bot.send_media_group(call.message.chat.id, hotel['photos_list'])
                    else:
                        bot.send_message(call.message.chat.id, '\n'.join(text), parse_mode="Markdown",
                                         reply_markup=ReplyKeyboardRemove())
                    text.clear()
                with db:
                    Request.create(telegram_id=call.from_user.id,
                                   request_time=data['request_time'],
                                   request_date=data['request_date'],
                                   checkin='-'.join(map(str, data['start_date'].values())),
                                   checkout='-'.join(map(str, data['end_date'].values())),
                                   mode=data['mode'], location_id=data['destination_id'],
                                   city_en=data['city_en'],
                                   city_ru=data['city_users'],
                                   hotels_num=data['num_hotels_output'],
                                   photo_nes=data['photos_necessity'],
                                   photos_num=data['photos_num'])
