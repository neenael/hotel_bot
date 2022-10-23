from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['help'])
def help_user(message: Message) -> None:
    help_list = 'Вот весь список команд:\n\n/help — помощь по командам бота\n' \
                '/lowprice — вывод самых дешёвых отелей в городе\n' \
                '/highprice — вывод самых дорогих отелей в городе \n' \
                '/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра\n' \
                '/history — вывод истории поиска отелей'
    bot.send_message(message.chat.id, help_list)
