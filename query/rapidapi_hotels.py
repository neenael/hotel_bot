from typing import Any
import requests
import json
from translate import Translator
from telebot.types import InputMediaPhoto
import os
from calibration.tools import *

translator = Translator(from_lang='ru', to_lang='en')
translator_ru = Translator(from_lang='en', to_lang='ru')


def city_search(city: str) -> Union[dict[str, Union[int, Any]], bool]:
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "en_US", "currency": "USD"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.ok:
            query_result = json.loads(response.text)
            return {'city_name': translator_ru.translate(query_result['suggestions'][0]['entities'][0]['name']).title(),
                    'destination_id': int(query_result['suggestions'][0]['entities'][0]['destinationId'])}
    except Exception:
        return False


def get_hotels(data: dict) -> list:
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": "{}".format(data['destination_id']),
                   "pageNumber": "1",
                   "pageSize": "25",
                   "checkIn": "{}-{}-{}".format(data['start_date']['year'],
                                                date_validation(data['start_date']['month']),
                                                date_validation(data['start_date']['day'])),
                   "checkOut": "{}-{}-{}".format(data['end_date']['year'],
                                                 date_validation(data['end_date']['month']),
                                                 date_validation(data['end_date']['day'])),
                   "adults1": "1", "sortOrder": data['mode']}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.ok:
        result = json.loads(response.text)
        return result['data']['body']['searchResults']['results']


def get_properties_list(data: dict, hotel_list: list) -> list:
    hotel_list_pro = []

    for hotel in hotel_list:
        try:
            hotel_item = dict()
            hotel_item['id'] = hotel['id']
            hotel_item['name'] = hotel['name']
            hotel_item['stars'] = round(float(hotel['starRating']))
            hotel_item['address'] = hotel['address']['streetAddress']
            hotel_item['city_center'] = hotel['landmarks'][0]['distance']
            hotel_item['cost'] = number_validation(hotel['ratePlan']['price']['current'][1:])
            if data['photos_necessity']:
                hotel_item['photos_list'] = get_photos(hotel_item['id'], data['photos_num'])
            hotel_list_pro.append(hotel_item)
            if len(hotel_list_pro) == data['num_hotels_output']:
                break
        except KeyError:
            pass
    return hotel_list_pro


def get_photos(hotel_id: int, number: int) -> list:
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": "{}".format(hotel_id)}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        result = json.loads(response.text)
        all_photos = []
        for link in result['hotelImages'][:number]:
            all_photos.append(InputMediaPhoto(link['baseUrl'].format(size='z')))

        return all_photos
    except Exception:
        pass
