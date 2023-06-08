import asyncio
import socket
from backend.worker import *
from tools.json_tools import *


class ServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, name, worker):
        self.name = name
        self.worker = worker

    def connection_made(self, transport):
        self.transport = transport
        print(f"{self.name}: connection made")

    def datagram_received(self, data, addr):
        print(f"{self.name}: datagram received {data} from {addr}")
        message = deserialize(data.decode())
        result = self.worker.do_test()
        answer_message = serialize(
            {"message_type": "return_result", "test_result": result, "addr": message["addr"]})
        self.transport.sendto(answer_message.encode(), addr)

    def error_received(self, exc):
        print(f"{self.name}: error received {exc}")

    def connection_lost(self, exc):
        print(f"{self.name}: connection lost")
        asyncio.get_event_loop().stop()


def create_unicast_endpoint(loop, worker):
    endpoint = loop.create_datagram_endpoint(
        lambda: ServerProtocol("Unicast", worker), local_addr=("0.0.0.0", 1234)
    )
    loop.run_until_complete(endpoint)


def create_multicast_endpoint(loop, worker):
    multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    multicast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    multicast_sock.bind(("0.0.0.0", int(os.getenv("MULTICAST_PORT"))))
    multicast_group = os.getenv("MULTICAST_ADDR")
    multicast_sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(multicast_group) + socket.inet_aton("0.0.0.0"),
    )

    endpoint = loop.create_datagram_endpoint(
        lambda: ServerProtocol("Multicast", worker), sock=multicast_sock
    )
    loop.run_until_complete(endpoint)


def start_server():
    loop = asyncio.get_event_loop()
    worker = Worker()

    create_unicast_endpoint(loop, worker)
    create_multicast_endpoint(loop, worker)

    loop.run_forever()
