import socket
from typing import Any

from ..protocol.methods import build_message, parse_msg
from ..protocol.models import *
from ..various.exceptions import MessageDataType, CounterUDPConnection, CounterTCPConnection

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


def count(topic: str = "default",
          tcp: bool = False,
          ip: str = SERVER_IP,
          port: int = SERVER_PORT) -> int:
    if not isinstance(topic, op_code_data_type[COUNT]):
        raise MessageDataType(f"Expected {str}, received {type(topic)}")

    msg = build_message(COUNT, topic)
    if tcp:
        return send_recv_tcp_msg(msg, ip, port)
    else:
        return send_recv_udp_msg(msg, ip, port)


def count_deco(*deco_args, **deco_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_result = func(*args, **kwargs)
            count_number = count(*deco_args, **deco_kwargs)
            return (
                count_number,
                func_result,
            )

        return wrapper

    return decorator


def reset(topic: str = "default",
          tcp: bool = False,
          ip: str = SERVER_IP,
          port: int = SERVER_PORT) -> None:
    if not isinstance(topic, op_code_data_type[COUNT]):
        raise MessageDataType(f"Expected {str}, received {type(topic)}")

    msg = build_message(RESET_SUM, topic)
    if tcp:
        return send_recv_tcp_msg(msg, ip, port)
    else:
        return send_recv_udp_msg(msg, ip, port)


def send_recv_udp_msg(msg: bytes, ip: str, port: int) -> Any:
    attempts = 0
    max_attempts = 5
    timeout = 0.1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.settimeout(timeout)
    while attempts < max_attempts:
        sock.sendto(msg, (ip, port))
        try:
            re_msg, addr = sock.recvfrom(MSG_MAXIMUM_LENGTH)
            op_code, data = parse_msg(re_msg)
            return data
        except socket.timeout:
            attempts += 1
    raise CounterUDPConnection("Exceeded connection maximum attempts")


def send_recv_tcp_msg(msg: bytes, ip: str, port: int) -> Any:
    timeout = 0.1

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    sock.settimeout(timeout)
    try:
        sock.connect((ip, port))
        sock.send(msg)
        re_msg = sock.recv(MSG_MAXIMUM_LENGTH)
        op_code, data = parse_msg(re_msg)
        sock.close()
        return data
    except (TimeoutError, ConnectionRefusedError, socket.timeout):
        sock.close()
        raise CounterTCPConnection("Connection timeout")
