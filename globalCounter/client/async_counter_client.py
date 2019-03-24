from trio import socket as async_socket
import trio
import socket
import inspect

from ..protocol.methods import build_message, parse_msg
from ..protocol.models import *
from ..various.exceptions import MessageDataType, CounterUDPConnection, CounterTCPConnection

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


async def count(topic: str = "default", tcp: bool = False, ip: str = SERVER_IP, port: int = SERVER_PORT):
    if not isinstance(topic, op_code_data_type[COUNT]):
        raise MessageDataType(f"Expected {str}, received {type(topic)}")

    msg = build_message(COUNT, topic)
    if tcp:
        return await send_recv_tcp_msg(msg, ip, port)
    else:
        return await send_recv_udp_msg(msg, ip, port)


def count_deco(*deco_args, **deco_kwargs):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if inspect.iscoroutinefunction(func):
                func_result = await func(*args, **kwargs)
            else:
                func_result = func(*args, **kwargs)
            count_number = await count(*deco_args, **deco_kwargs)
            return (
                count_number,
                func_result,
            )

        return wrapper

    return decorator


async def reset(topic: str = "default",
          tcp: bool = False,
          ip: str = SERVER_IP,
          port: int = SERVER_PORT):
    if not isinstance(topic, op_code_data_type[COUNT]):
        raise MessageDataType(f"Expected {str}, received {type(topic)}")

    msg = build_message(RESET_SUM, topic)
    if tcp:
        return await send_recv_tcp_msg(msg, ip, port)
    else:
        return await send_recv_udp_msg(msg, ip, port)


async def send_recv_udp_msg(msg: bytes, ip: str, port: int) -> int:
    attempts = 0
    max_attempts = 5
    timeout = 0.1

    sock = async_socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    while attempts < max_attempts:
        with trio.move_on_after(timeout):
            await sock.sendto(msg, (ip, port))
            re_msg, addr = await sock.recvfrom(MSG_MAXIMUM_LENGTH)
            op_code, data = parse_msg(re_msg)
            return data
        attempts += 1
    raise CounterUDPConnection("Exceeded connection maximum attempts")


async def send_recv_tcp_msg(msg: bytes, ip: str, port: int) -> int:
    timeout = 0.1

    sock = async_socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    try:
        with trio.move_on_after(timeout):
            await sock.connect((ip, port))
            await sock.send(msg)
            re_msg = await sock.recv(MSG_MAXIMUM_LENGTH)
            op_code, data = parse_msg(re_msg)
            sock.close()
            return data
    except ConnectionRefusedError:
        sock.close()
        raise CounterTCPConnection("Connection timeout")
