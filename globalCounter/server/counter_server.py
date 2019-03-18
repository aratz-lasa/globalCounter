import socket
import struct

from ..protocol.syntax import *


class CounterServer:
    def __init__(self, ip="0.0.0.0", port=0):
        self.count = 0
        self.ip = ip
        self.port = port
        self.sock = None
        self.is_running = False

    def run(self):
        self.bind_socket()

        while True:
            self.is_running = True
            data, addr = self.sock.recvfrom(MSG_MAXIMUM_LENGTH)
            self.count += 1
            message = self.get_packed_count(self.count)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message, addr)

    def bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

    def get_packed_count(self, count: int) -> bytes:
        return struct.pack(COUNT_NUMBER_FORMAT, count)

    def stop(self):
        self.sock.close()
        self.is_running = False
