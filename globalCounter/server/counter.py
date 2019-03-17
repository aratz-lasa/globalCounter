import socket
import struct

UDP_MAX_MSG = 65_536


class Counter:
    def __init__(self, ip="0.0.0.0", port=0):
        self.count = 0
        self.ip = ip
        self.port = port
        self.sock = None

    def run(self):
        self.bind_socket()

        while True:
            data, addr = self.sock.recvfrom(UDP_MAX_MSG)
            self.count += 1
            message = self.get_packed_count(self.count)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message, addr)

    def bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

    def get_packed_count(self, count: int) -> bytes:
        return struct.pack("!Q", count)
