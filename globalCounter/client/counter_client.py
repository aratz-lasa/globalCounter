import socket
import struct

from ..protocol.methods import build_message, parse_message
from ..protocol.models import *
from ..various.exceptions import MessageDataType

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


def count(topic: str = "default", tcp: bool = False, ip: str = SERVER_IP, port: int = SERVER_PORT, ):
    if not isinstance(topic, str):
        raise MessageDataType(f"Expected {str}, received {type(topic)}")

    msg = build_message(COUNT, topic)
    if tcp:
        return count_tcp(msg, ip, port)
    else:
        return count_udp(msg, ip, port)


def count_udp(msg: bytes, ip: str, port: int) -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(msg, (ip, port))
    re_msg, addr = sock.recvfrom(MSG_MAXIMUM_LENGTH)
    op_code, data = parse_message(re_msg)
    return data


def count_tcp(msg: bytes, ip: str, port: int) -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # UDP
    sock.connect((ip, port))
    sock.send(msg)
    re_msg = sock.recv(MSG_MAXIMUM_LENGTH)
    op_code, data = parse_message(re_msg)
    return data


def count_deco(*deco_args, **deco_kwargs):
    def count_sub_deco(func):
        def count_func(*args, **kwargs):
            func_result = func(*args, **kwargs)
            count_number = count(*deco_args, **deco_kwargs)
            return (
                count_number,
                func_result,
            )
        return count_func

    return count_sub_deco
