from os import getenv
import pika
from multiprocessing import Process
from json import loads, dumps
import logging
# Настройка логирования для библиотеки piko
logging.getLogger('pika').setLevel(logging.WARNING)


def deserialize(data):
    try:
        return loads(data)
    except:
        return None


def Receiver(self_login, exchange_name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(
        exchange=exchange_name, exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    print(f'Вы подключены к чату: {exchange_name}')

    def callback(ch, method, properties, body):
        data = deserialize(body.decode('utf-8'))
        if not "from" in data or not "message" in data or len(data) != 2:
            return
        if data["from"] == self_login:
            return
        print(
            f"Получено сообщение в чате {exchange_name} от {data['from']}: {data['message']}")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


class Messenger:
    def __init__(self, login, session_id):
        self.login = login
        self.session_id = session_id
        self.is_bot = getenv("IS_BOT")
        if self.is_bot is None or self.is_bot != "1":
            self.exchange_name = f'messenger_{session_id}'
            self.receiver = Process(target=Receiver, kwargs={"self_login": login,
                                    "exchange_name": self.exchange_name})
            self.receiver.start()

    def __del__(self):
        if self.is_bot is None or self.is_bot != "1":
            self.receiver.kill()

    def SendMessage(self, message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(
            exchange=self.exchange_name, exchange_type='fanout')

        data = dumps({"from": self.login, "message": message})

        channel.basic_publish(exchange=self.exchange_name,
                              routing_key='', body=data)
        connection.close()
