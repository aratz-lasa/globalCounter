import socket

from globalCounter.protocol.methods import build_message, parse_msg
from globalCounter.protocol.models import *

from .utils.count_server import global_counter

TEST_PORT = 5555
TEST_IP = "127.0.0.1"


def test_udp_server_count():
    with global_counter(TEST_IP, TEST_PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        op_code = COUNT
        topic = "topic"
        sock.sendto(build_message(op_code, topic), (TEST_IP, TEST_PORT))
        msg, addr = sock.recvfrom(MSG_MAXIMUM_LENGTH)
        re_op_code, re_data = parse_msg(msg)

        expected_op_code = request_response_opcodes[op_code]
        assert re_op_code == expected_op_code
        assert type(re_data) == op_code_data_type[expected_op_code]


def test_tcp_server_count():
    with global_counter(TEST_IP, TEST_PORT, tcp=True):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        sock.connect((TEST_IP, TEST_PORT))
        op_code = COUNT
        topic = "topic"
        sock.send(build_message(op_code, topic))
        msg = sock.recv(MSG_MAXIMUM_LENGTH)
        re_op_code, re_data = parse_msg(msg)

        expected_op_code = request_response_opcodes[op_code]
        assert re_op_code == expected_op_code
        assert type(re_data) == op_code_data_type[expected_op_code]

        sock.close()


def test_udp_server_reset_sum():
    with global_counter(TEST_IP, TEST_PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        op_code = RESET_SUM
        topic = "topic"
        sock.sendto(build_message(op_code, topic), (TEST_IP, TEST_PORT))
        msg, addr = sock.recvfrom(MSG_MAXIMUM_LENGTH)
        re_op_code, re_data = parse_msg(msg)

        expected_op_code = request_response_opcodes[op_code]
        assert re_op_code == expected_op_code
        assert type(re_data) == op_code_data_type[expected_op_code]


def test_tcp_server_reset_sum():
    with global_counter(TEST_IP, TEST_PORT, tcp=True):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        sock.connect((TEST_IP, TEST_PORT))
        op_code = RESET_SUM
        topic = "topic"
        sock.send(build_message(op_code, topic))
        msg = sock.recv(MSG_MAXIMUM_LENGTH)
        re_op_code, re_data = parse_msg(msg)

        expected_op_code = request_response_opcodes[op_code]
        assert re_op_code == expected_op_code
        assert type(re_data) == op_code_data_type[expected_op_code]

        sock.close()
