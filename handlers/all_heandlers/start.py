from loader import bot
from telebot.types import ReplyKeyboardRemove, Message


@bot.message_handler(commands=['start', 'restart'])
def start(message: Message) -> None:
    if message.text == '/restart':
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, 'Бот перезапущен', reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Привет👋\nЯ бот, который поможет подобрать подходящий отель\n'
                                          'Для навигации воспользуйтесь кнопкой МЕНЮ в нижней части экрана\n'
                                          'Если возникнут трудности, напишите команду /help')
