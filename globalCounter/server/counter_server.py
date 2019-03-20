import socket
import struct

from ..protocol.syntax import *
from ..protocol.methods import *


class CounterServer:
    def __init__(self, ip="0.0.0.0", port=0):
        self.topic_sum_map = {}
        self.ip = ip
        self.port = port
        self.sock = None
        self.is_running = False

    def run(self):
        self.bind_socket()

        while True:
            self.is_running = True
            data, addr = self.sock.recvfrom(MSG_MAXIMUM_LENGTH)
            op_code, payload = parse_message(data)
            sum = self.count_and_get_sum(payload)
            message = self.get_packed_sum(sum)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message, addr)

    def count_and_get_sum(self, payload):
        sum = self.topic_sum_map.get(payload, 0)
        sum += 1
        self.topic_sum_map[payload] = sum
        return sum

    def bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

    def get_packed_sum(self, sum: int) -> bytes:
        return struct.pack(SUM_NUMBER_FORMAT, sum)

    def stop(self):
        self.sock.close()
        self.is_running = False
