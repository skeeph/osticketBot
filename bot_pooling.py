# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import telebot
from telebot import types
from ticket import Ticket

import config

bot = telebot.TeleBot(config.TOKEN)

tickets = {}


@bot.message_handler(commands=['problem'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
    Добрый день. Как вас зовут?
    """)
    tickets[message.chat.id] = Ticket()
    tickets[message.chat.id].sender = "%d@%d" % (message.from_user.id, message.chat.id)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    markup = types.ReplyKeyboardMarkup()
    items = [types.KeyboardButton(str(i)) for i in range(10)]
    markup.add(*items)

    try:
        chat_id = message.chat.id
        x = tickets[message.chat.id]
        x.name = message.text
        msg = bot.reply_to(message, 'Введите ваш номер телефона?')
        bot.register_next_step_handler(msg, process_number_step)
    except Exception as e:
        bot.reply_to(message, type(e))


def process_number_step(message):
    try:
        chat_id = message.chat.id
        tickets[message.chat.id].number = message.text
        msg = bot.reply_to(message, 'В чем проблема?(Введите пожалуйста суть)??')
        bot.register_next_step_handler(msg, process_title_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_title_step(message):
    try:
        chat_id = message.chat.id
        tickets[message.chat.id].title = message.text
        msg = bot.reply_to(message, 'Опищите проблему подробнее')
        bot.register_next_step_handler(msg, process_problem_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_problem_step(message):
    try:
        chat_id = message.chat.id
        tickets[message.chat.id].desc = message.text
        bot.reply_to(message, str(tickets[message.chat.id].to_json()))
    except Exception as e:
        bot.reply_to(message, 'oooops')


bot.remove_webhook()
bot.polling()
