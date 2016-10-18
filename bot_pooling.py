# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import requests
import base64
import telebot
from telebot import types
from ticket import Ticket

import config
from utils import random_str

bot = telebot.TeleBot(config.TOKEN)

tickets = {}


@bot.message_handler(commands=['problem', 'atrier'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
    Добрый день. Как вас зовут?
    """)
    tickets[message.chat.id] = Ticket()
    tickets[message.chat.id].sender = "{0}/{1}@telegram.com".format(message.from_user.id, message.chat.id)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        x = tickets[message.chat.id]
        x.name = message.text
        msg = bot.reply_to(message, 'Назовите ваше заведение?')
        bot.register_next_step_handler(msg, process_place_step)
    except Exception as e:
        bot.reply_to(message, type(e))


def process_place_step(message):
    try:
        x = tickets[message.chat.id]
        x.name += "@{0}".format(message.text)
        msg = bot.reply_to(message, 'Введите ваш номер телефона?')
        bot.register_next_step_handler(msg, process_number_step)
    except Exception as e:
        bot.reply_to(message, type(e))


def process_number_step(message):
    try:
        chat_id = message.chat.id
        try:
            phone = int(message.text)
        except ValueError as e:
            msg = bot.reply_to(message, 'Неправильное введен номер. Пожалуйста, введите только цифры')
            bot.register_next_step_handler(msg, process_number_step)
            return
        tickets[message.chat.id].number = phone
        msg = bot.reply_to(message, 'В чем проблема?(кратко)')
        bot.register_next_step_handler(msg, process_title_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_title_step(message):
    try:
        chat_id = message.chat.id
        tickets[message.chat.id].title = message.text
        msg = bot.reply_to(message, 'Опищите проблему(Подробно)')
        bot.register_next_step_handler(msg, process_problem_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


markup = types.ReplyKeyboardMarkup(row_width=2)
yes = types.KeyboardButton('Да')
no = types.KeyboardButton('Нет')
markup.row(*[yes, no])


def process_problem_step(message):
    try:
        chat_id = message.chat.id
        tickets[message.chat.id].desc = message.text
        msg = bot.reply_to(message, 'Вы хотите прикрепить файлы к заявке?', reply_markup=markup)
        bot.register_next_step_handler(msg, ask_attach_step)
    except Exception as e:
        bot.reply_to(message, type(e))


hide = types.ReplyKeyboardHide(selective=True)


def ask_attach_step(message):
    try:
        text = message.text
        if text == "Да":
            msg = bot.reply_to(message, 'Прикрепите необходимые файлы', reply_markup=hide)
            bot.register_next_step_handler(msg, process_attachments_step)
        else:
            msg = bot.reply_to(message, 'Файлы не прикреплены', reply_markup=hide)
            process_finish_step(message)
    except Exception as e:
        bot.reply_to(message, type(e))


def process_attachments_step(message):
    try:
        text = message.text
        # TODO Сохранение прикрепленных
        msg = bot.reply_to(message, 'Вы хотите прикрепить еще файлы к заявке?', reply_markup=markup)
        bot.register_next_step_handler(msg, ask_attach_step)
        if message.video is not None:
            pass

        if message.photo is not None:
            photo = message.photo[3]
            file_info = bot.get_file(photo.file_id)
            url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path)
            file = requests.get(url)
            b6str = base64.b64encode(file.content)
            tickets[message.chat.id].attachments[file_info.file_path] = "data:image/jpg;base64," + b6str.decode("utf-8")

        if message.voice is not None:
            pass

        if message.document is not None:
            pass

        if message.audio is not None:
            pass

    except Exception as e:
        bot.reply_to(message, type(e))
        process_finish_step(message)


@bot.message_handler(commands=['file'])
def start_file(message):
    try:
        chat_id = message.chat.id
        msg = bot.reply_to(message, 'Вы хотите прикрепить файлы к заявке?', reply_markup=markup)
        bot.register_next_step_handler(msg, ask_attach_step)
    except Exception as e:
        bot.reply_to(message, type(e))


def process_finish_step(message):
    s = tickets[message.chat.id].save()
    print(tickets[message.chat.id].to_json())
    if s:
        msg = bot.reply_to(message, 'Ваша заявка зарегистрирована под номером %s' % s)
    else:
        msg = bot.reply_to(message,
                           'К сожалению произошла ошибка добавления заявки. Пожалуйста, попробуйте еще раз. %s' % s)
    del tickets[message.chat.id]


bot.remove_webhook()
bot.polling()
