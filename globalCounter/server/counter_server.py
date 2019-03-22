import socket

from ..protocol.methods import build_message, parse_message
from ..protocol.models import *


class CounterServer:
    def __init__(self, ip="0.0.0.0", port=0):
        self.topic_sum_map = {}
        self.ip = ip
        self.port = port
        self.sock = None
        self.is_running = False
        self.bind_socket()

    def run(self):
        self.is_running = True

        while self.is_running:
            addr, msg = self.receive_msg()
            op_code, payload = msg

            sum = self.count_and_get_sum(payload)
            re_op_code = request_response_opcodes[op_code]
            message = build_message(re_op_code, sum)

            self.send_response(addr, message)

    def send_response(self, addr, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, addr)

    def receive_msg(self):
        data, addr = self.sock.recvfrom(MSG_MAXIMUM_LENGTH)
        op_code, payload = parse_message(data)
        return addr, (op_code, payload)

    def count_and_get_sum(self, topic):
        sum = self.topic_sum_map.get(topic, 0)
        sum += 1
        self.topic_sum_map[topic] = sum
        return sum

    def bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

    def stop(self):
        self.sock.close()
        self.is_running = False
