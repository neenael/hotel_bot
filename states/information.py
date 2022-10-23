from telebot.handler_backends import State, StatesGroup


class LowpriceStates(StatesGroup):
    neutral_status = State()
    update_years = State()
    check_in_year = State()
    check_in_month = State()
    check_in_day = State()
    check_out_year = State()
    check_out_month = State()
    check_out_day = State()
    city_name = State()
    price_range = State()
    distance_range = State()
    property_search = State()
    photos_necessity = State()
    photos_amount = State()


class HihgpriceStates(StatesGroup):
    neutral_status = State()
    update_years = State()
    check_in_year = State()
    check_in_month = State()
    check_in_day = State()
    check_out_year = State()
    check_out_month = State()
    check_out_day = State()
    city_name = State()
    price_range = State()
    distance_range = State()
    property_search = State()
    photos_necessity = State()
    photos_amount = State()


class BestdealStates(StatesGroup):
    neutral_status = State()
    update_years = State()
    check_in_year = State()
    check_in_month = State()
    check_in_day = State()
    check_out_year = State()
    check_out_month = State()
    check_out_day = State()
    city_name = State()
    price_range = State()
    distance_range = State()
    property_search = State()
    photos_necessity = State()
    photos_amount = State()