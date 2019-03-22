from globalCounter.protocol.methods import *


def test_build_message():
    op_code = COUNT
    data = "topic"
    message = build_message(op_code, data)
    assert type(message) is bytes
    assert message[0] == op_code
    assert message[1:].decode(DATA_ENCODING) == data

    op_code = RE_COUNT
    data = 1
    message = build_message(op_code, data)
    assert type(message) is bytes
    assert message[0] == op_code
    assert message[1] == data


def test_parse_message():
    op_code = COUNT
    data = "topic"
    test_message = bytes([op_code]) + data.encode(DATA_ENCODING)
    re_op_code, re_data = parse_message(test_message)
    assert type(re_op_code) is int
    assert type(re_data) is str
    assert re_op_code == op_code
    assert re_data == data

    op_code = RE_COUNT
    data = 1
    test_message = bytes([op_code, data])
    re_op_code, re_data = parse_message(test_message)
    assert type(re_op_code) is int
    assert type(re_data) is int
    assert re_op_code == op_code
    assert re_data == data
