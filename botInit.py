import flask
import telebot
import logging
import ssl
import config

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain(config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_PRIV)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config.TOKEN)

app = flask.Flask(__name__)
