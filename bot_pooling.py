# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import sys
import requests
import requests.exceptions
import base64
import telebot
from telebot import types
from ticket import Ticket

import config
from utils import random_str

bot = telebot.TeleBot(config.TOKEN)

tickets = {}


@bot.message_handler(commands=['problem', 'atrier'])
def send_welcome(message: types.Message):
    msg = bot.reply_to(message, """\
    Добрый день. Назовите ваше заведение?
    """)
    tickets[message.chat.id] = Ticket()
    tickets[message.chat.id].sender = "{0}/{1}@telegram.com".format(message.from_user.id, message.chat.id)
    tickets[message.chat.id].name = message.chat.first_name + " " + message.chat.last_name
    bot.register_next_step_handler(msg, process_place_step)


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

        msg = bot.reply_to(message, 'Вы хотите прикрепить еще файлы к заявке?', reply_markup=markup)
        bot.register_next_step_handler(msg, ask_attach_step)
        if message.video is not None:
            video = message.video
            file_info = bot.get_file(video.file_id)
            url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path)
            file = requests.get(url)
            b6str = base64.b64encode(file.content)
            x = {file_info.file_path: "data:video/mp4;base64," + b6str.decode("utf-8")}
            tickets[message.chat.id].attachments.append(x)

        if message.photo is not None:
            photo = message.photo[3]
            file_info = bot.get_file(photo.file_id)
            url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path)
            file = requests.get(url)
            b6str = base64.b64encode(file.content)
            x = {file_info.file_path: "data:image/jpg;base64," + b6str.decode("utf-8")}
            tickets[message.chat.id].attachments.append(x)

        if message.voice is not None:
            voice = message.voice
            file_info = bot.get_file(voice.file_id)
            url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path)
            file = requests.get(url)
            b6str = base64.b64encode(file.content)
            x = {file_info.file_path: "data:" + voice.mime_type + ";base64," + b6str.decode("utf-8")}
            tickets[message.chat.id].attachments.append(x)

        if message.document is not None:
            file_info = bot.get_file(message.document.file_id)
            url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path)
            file = requests.get(url)
            b6str = base64.b64encode(file.content)
            x = {message.document.file_name: "data:" + message.document.mime_type + ";base64," + b6str.decode("utf-8")}
            tickets[message.chat.id].attachments.append(x)

        if message.audio is not None:
            pass

    except Exception as e:
        bot.reply_to(message, type(e))
        process_finish_step(message)


@bot.message_handler(commands=['file'])
def start_file(message):
    try:
        chat_id = message.chat.id
        x = Ticket()
        x.name = "Хабиб"
        x.number = "89634131153"
        x.title = "Сериализация"
        x.desc = "Десериалиация"
        x.sender = "skeeph05@gmail.com"
        tickets[chat_id] = x
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


def main():
    try:
        bot.polling()
    except requests.exceptions.ReadTimeout:
        main()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
