from typing import Any

from .models import *
from ..various.exceptions import MessageDataType, MessageOpCode


def get_response(msg, topic_sum_map):
    op_code, data = parse_msg(msg)
    re_data = apply_op(op_code, data, topic_sum_map)
    re_op_code = request_response_opcodes[op_code]
    return build_message(re_op_code, re_data)


def build_message(op_code: int, data: Any) -> bytes:
    try:
        data_type = op_code_data_type[op_code]
    except KeyError:
        raise MessageOpCode(f"Invalid OpCode: {op_code}")
    if not isinstance(data, data_type):
        raise MessageDataType(f"Expected {data_type}, received {type(data)}")

    if data_type is str:
        return bytes([op_code]) + data.encode(DATA_ENCODING)
    elif data_type is int:
        return bytes([op_code, data])
    elif data_type is type(None):
        return bytes([op_code])


def parse_msg(message: bytes) -> (int, str):
    op_code = message[0]
    raw_data = message[1:]
    try:
        data_type = op_code_data_type[op_code]
        if data_type is str:
            data = raw_data.decode(DATA_ENCODING)
        elif data_type is int:
            data = int.from_bytes(raw_data, byteorder="big")
        elif data_type is type(None):
            data = None
    except KeyError:
        raise MessageOpCode(f"Invalid OpCode: {op_code}")
    except TypeError:
        raise MessageDataType(
            f"Could not parse bytes to {data_type}. Data: {raw_data}")

    return op_code, data


def apply_op(op_code: int, data: Any, topic_sum_map: dict):
    if op_code == COUNT:
        return count_and_get_sum(data, topic_sum_map)
    elif op_code == RESET_SUM:
        return reset_topic(data, topic_sum_map)


def count_and_get_sum(topic: str, topic_sum_map: dict) -> int:
    sum = topic_sum_map.get(topic, 0)
    sum += 1
    topic_sum_map[topic] = sum
    return sum


def reset_topic(topic: str, topic_sum_map: dict) -> None:
    topic_sum_map[topic] = 0
