import telebot
import flask
from telebot import types
from db import DbHandler
from config
from keyboa import Keyboa

WEBHOOK_URL_BASE = "https://{}:{}".format(config.WEBHOOK_HOST, config.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(config.TOKEN)

bot = telebot.TeleBot(config.TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

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


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
