#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a simple echo bot using decorators and webhook with flask
# It echoes any incoming text messages and does not use the polling method.

from botInit import *
import telebot.types as types


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    print(flask.request.get_data().decode('utf-8'))
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_messages([update.message])
        return ''
    else:
        flask.abort(403)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start', 'проблема'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
    Добрый день. Как вас зовут?
    """)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    markup = types.ReplyKeyboardMarkup()
    items = [types.KeyboardButton(i) for i in range(10)]
    markup.add(*items)

    try:
        chat_id = message.chat.id
        name = message.text
        msg = bot.reply_to(message, 'Введите ваш номер телефона?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_number_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_number_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        msg = bot.reply_to(message, 'В чем проблема?(Введите пожалуйста суть)??')
        bot.register_next_step_handler(msg, process_title_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_title_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        msg = bot.reply_to(message, 'Опищите проблему подробнее')
        bot.register_next_step_handler(msg, process_problem_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_problem_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
    except Exception as e:
        bot.reply_to(message, 'oooops')


@app.before_first_request
def add_hook():
    # Remove webhook, it fails sometimes the set if there is a previous webhook
    # Set webhook
    print(config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH)
    bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                    certificate=open(config.WEBHOOK_SSL_CERT, 'r'))


bot.remove_webhook()
# Start flask server
app.run(host=config.WEBHOOK_LISTEN,
        port=config.WEBHOOK_PORT,
        ssl_context=context,
        debug=True)
