from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def basket() -> InlineKeyboardMarkup:
    basket_button = InlineKeyboardMarkup()
    basket_button.add(InlineKeyboardButton(text='🗑', callback_data='delete_history'))
    return basket_button
