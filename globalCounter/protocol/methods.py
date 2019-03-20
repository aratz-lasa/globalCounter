from .syntax import *


def build_message(operation_code:int, payload:str) -> bytes:
    return bytes([operation_code]) + payload.encode(PAYLOAD_ENCODING)


def parse_message(message: bytes) -> (int, str):
    return message[0], message[1:].decode(PAYLOAD_ENCODING)
