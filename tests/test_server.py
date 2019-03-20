import socket
import struct

from globalCounter.protocol.syntax import *

from .utils.count_server import global_counter

TEST_PORT = 5555
TEST_IP = "127.0.0.1"
TEST_MSG = b"COUNT"


def test_server_count():
    with global_counter(TEST_IP, TEST_PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(TEST_MSG, (TEST_IP, TEST_PORT))
        msg, addr = sock.recvfrom(MSG_MAXIMUM_LENGTH)

        assert struct.unpack(SUM_NUMBER_FORMAT, msg)[0] == 1
