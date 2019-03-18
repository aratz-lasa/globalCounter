from globalCounter.client import counter_client

from .utils.count_server import global_counter

TEST_PORT = 5555
TEST_IP = "127.0.0.1"
TEST_MSG = b"COUNT"


def test_client_count():
    with global_counter(TEST_IP, TEST_PORT):
        for count in range(1, 100):
            assert counter_client.count() == count


def test_client_count_decorator():
    @counter_client.count_func
    def get_zero():
        return 0

    with global_counter(TEST_IP, TEST_PORT):
        count_number, result = get_zero()
        assert count_number == 1
        assert result == 0
