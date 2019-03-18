import socket
import struct

from ..protocol.syntax import *

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


def count(ip=SERVER_IP, port=SERVER_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(COUNT_MSG, (ip, port))
    msg, addr = sock.recvfrom(MSG_MAXIMUM_LENGTH)

    return struct.unpack(COUNT_NUMBER_FORMAT, msg)[0]


def count_func(func):
    def counted_func(*args, **kwargs):
        func_result = func(*args, **kwargs)
        count_number = count()
        return (
            count_number,
            func_result,
        )

    return counted_func
