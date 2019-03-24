from trio import socket
import trio

from ..protocol.methods import *
from ..protocol.models import *
from ..various.abc import CounterServer


class AsyncUDPCounterServer(CounterServer):
    def __init__(self, ip="0.0.0.0", port=0):
        self.topic_sum_map = {}
        self.ip = ip
        self.port = port
        self.sock = None
        self.is_running = False

    async def run(self) -> None:
        await self.bind_socket()
        self.is_running = True

        try:
            async with trio.open_nursery() as nursery:
                while self.is_running:
                    msg, addr = await self.sock.recvfrom(MSG_MAXIMUM_LENGTH)
                    nursery.start_soon(self.handle_request, msg, addr)
        except Exception as err:
            if self.is_running:
                raise err

    async def handle_request(self, msg: bytes, addr) -> None:
        re_msg = get_response(msg, self.topic_sum_map)
        await self.send_response(re_msg, addr)

    async def send_response(self, msg: bytes, addr) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        await sock.sendto(msg, addr)

    async def bind_socket(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        await self.sock.bind((self.ip, self.port))

    def stop(self) -> None:
        self.is_running = False
        self.sock.close()


class AsyncTCPCounterServer(CounterServer):
    def __init__(self, ip="0.0.0.0", port=0):
        self.topic_sum_map = {}
        self.ip = ip
        self.port = port
        self.sock = None
        self.is_running = False

    async def run(self) -> None:
        await self.bind_socket()
        self.is_running = True

        try:
            async with trio.open_nursery() as nursery:
                while self.is_running:
                    conn, _ = await self.sock.accept()
                    nursery.start_soon(self.handle_request, conn)
        except Exception as err:
            if self.is_running:
                raise err

    async def handle_request(self, conn) -> None:
        msg = await conn.recv(MSG_MAXIMUM_LENGTH)
        re_msg = get_response(msg, self.topic_sum_map)
        await self.send_response(re_msg, conn)

    async def send_response(self, message: bytes, conn) -> None:
        await conn.send(message)
        conn.close()

    async def bind_socket(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        await self.sock.bind((self.ip, self.port))
        self.sock.listen(1)

    def stop(self) -> None:
        self.is_running = False
        self.sock.close()
