from globalCounter.protocol.methods import *
from globalCounter.protocol.syntax import *


TEST_OP_CODE = 1
TEST_PAYLOAD = "topic"

def test_build_message():

    message = build_message(TEST_OP_CODE, TEST_PAYLOAD)
    assert type(message) is bytes
    assert message[0] == TEST_OP_CODE
    assert message[1:].decode() == TEST_PAYLOAD


def test_parse_message():
    TEST_MESSAGE = bytes([TEST_OP_CODE]) + TEST_PAYLOAD.encode(PAYLOAD_ENCODING)
    op_code, payload = parse_message(TEST_MESSAGE)
    assert type(op_code) is int
    assert type(payload) is str
    assert op_code == TEST_OP_CODE
    assert payload == TEST_PAYLOAD
