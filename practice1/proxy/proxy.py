import asyncio
from tools.json_tools import *
import logging
import os

logging.basicConfig(level=logging.INFO)


class ProxyProtocol(asyncio.DatagramProtocol):
    def __init__(self, name):
        self.name = name
        self.backend_port = 1234
        self.multicast_addr = (os.getenv("MULTICAST_ADDR"),
                               int(os.getenv("MULTICAST_PORT")))

    def connection_made(self, transport):
        self.transport = transport
        logging.info(f"{self.name}: connection made")

    def datagram_received(self, data, addr):
        message = deserialize(data.decode("utf-8"))
        logging.info("receive message %s", serialize(message))
        if message is None or not "message_type" in message:
            return

        match message["message_type"]:
            case "get_result":
                message["addr"] = addr
                unicast_message = serialize(message)
                for format in message["formats"]:
                    self.transport.sendto(
                        unicast_message.encode(), (format, self.backend_port))
                    logging.info("send message %s to %s", unicast_message, serialize(
                        (format, self.backend_port)))
            case "get_result_all":
                multicast_message = serialize(
                    {"message_type": "get_result_all", "addr": addr})
                self.transport.sendto(
                    multicast_message.encode(), self.multicast_addr)
                logging.info("send message %s to %s",
                             multicast_message, str(self.multicast_addr))
            case "return_result":
                self.transport.sendto(message["test_result"].encode(
                ), (message["addr"][0], message["addr"][1]))
                logging.info("send message with result to, %s",
                             str(message['addr']))
            case _:
                logging.info("Unknown message_type , %s". str(
                    message['message_type']))


def create_proxy_endpoint(loop):
    endpoint = loop.create_datagram_endpoint(
        lambda: ProxyProtocol("Proxy"), local_addr=('0.0.0.0', 2000))
    loop.run_until_complete(endpoint)


def start_proxy():
    loop = asyncio.get_event_loop()
    create_proxy_endpoint(loop)
    loop.run_forever()
