import telebot
from telebot import types
from db import DbHandler
from config import TOKEN
from keyboa import Keyboa

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def topic(message):
    db = DbHandler()
    topics = db.get_topics()
    kb = Keyboa(items=topics, alignment=True).keyboard
    bot.send_message(message.chat.id, 'Hello! I am Ted and I am ready to help you to find a Tedtalk video. Please, select a topic: ', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    to_send = 'There are some videos related to your topic: '
    db = DbHandler()
    links = db.get_urls_by_topic(call.data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for link in links:
        butt = types.InlineKeyboardButton(link[0], url=link[1])
        markup.add(butt)
    bot.send_message(call.message.chat.id, to_send, reply_markup=markup)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.polling(none_stop=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
