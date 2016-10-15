import requests

class Ticket:
    def __init__(self):
        self._name = None
        self._number = None
        self._title = None
        self._desc = None
        self._sender = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sender):
        self._sender = sender

    def to_json(self):
        return {
            "alert": True,
            "autorespond": True,
            "source": "API",
            "name": self.name,
            "email": self.sender,
            "phone": self.number,
            "subject": self.title,
            "ip": "127.0.0.1",
            "message": self.desc,
            "attachments": []
        }

    def save(self):
        pass


if __name__ == "__main__":
    x = Ticket()
    x.name = "Хабиб"
    x.number = "89634131153"
    x.title = "Сериализация"
    x.desc = "Десериалиация"
    x.sender="skeeph05@gmail.com"
    print(x.to_json())
