import socket

from globalCounter.protocol.methods import build_message, parse_message
from globalCounter.protocol.models import *

from .utils.count_server import global_counter

TEST_PORT = 5555
TEST_IP = "127.0.0.1"


def test_server_count():
    with global_counter(TEST_IP, TEST_PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        op_code = COUNT
        topic = "topic"
        sock.sendto(build_message(op_code, topic), (TEST_IP, TEST_PORT))
        msg, addr = sock.recvfrom(MSG_MAXIMUM_LENGTH)
        re_op_code, re_data = parse_message(msg)

        expected_op_code = request_response_opcodes[op_code]
        assert re_op_code == expected_op_code
        assert type(re_data) == op_code_data_type[expected_op_code]
