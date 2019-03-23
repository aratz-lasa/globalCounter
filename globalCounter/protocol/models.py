## name --> op_code
COUNT = 0
RE_COUNT = COUNT + 128
RESET_SUM = 1
RE_RESET_SUM = RESET_SUM + 128

op_code_data_type = {
    COUNT: str,
    RE_COUNT: int,
    RESET_SUM: str,
    RE_RESET_SUM: type(None)
}

request_response_opcodes = {COUNT: RE_COUNT, RESET_SUM: RE_RESET_SUM}

DATA_ENCODING = "utf-8"

MSG_MAXIMUM_LENGTH = 65_536
