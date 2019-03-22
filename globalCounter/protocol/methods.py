from typing import Any

from .models import *
from ..various.exceptions import MessageDataType, MessageOpCode


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
    elif data_type is None:
        return bytes([op_code])


def parse_message(message: bytes) -> (int, str):
    op_code = message[0]
    raw_data = message[1:]
    try:
        data_type = op_code_data_type[op_code]
        if data_type is str:
            data = raw_data.decode(DATA_ENCODING)
        elif data_type is int:
            data = int.from_bytes(raw_data, byteorder="big")
        elif data_type is None:
            data = None
    except KeyError:
        raise MessageOpCode(f"Invalid OpCode: {op_code}")
    except TypeError:
        raise MessageDataType(
            f"Could not parse bytes to {data_type}. Data: {raw_data}")

    return op_code, data
