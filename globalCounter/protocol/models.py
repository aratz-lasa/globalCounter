## name --> op_code
COUNT = 0
RE_COUNT = COUNT + 128

op_code_data_type = {COUNT: str, RE_COUNT: int}

request_response_opcodes = {
    COUNT: RE_COUNT,
}

DATA_ENCODING = "utf-8"

MSG_MAXIMUM_LENGTH = 65_536
