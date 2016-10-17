import os

TOKEN = '285550392:AAGnNRGmWDrxrYlPE9VgNPBe6VV0wxyjs9I'
BOTAN = 'gbWYaN9qPVJUlBDy-TXhpoEt3vMa59WN'
WEBHOOK_HOST = 'xfood.atrier.ru'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

current_dir = os.path.dirname(os.path.abspath(__file__))
WEBHOOK_SSL_CERT = os.path.join(current_dir, 'cert', 'cert.pem')
WEBHOOK_SSL_PRIV = os.path.join(current_dir, 'cert', 'key.pem')

WEBHOOK_URL_BASE = "https://%s" % WEBHOOK_HOST
WEBHOOK_URL_PATH = "/%s/" % TOKEN


api = {
    'ticket': 'http://service.atrier.ru/api/http.php/tickets.json',
    'users': 'http://service.atrier.ru/api/http.php/users.json',
    'key': '99A730889574730FA7247DF813721102'
}