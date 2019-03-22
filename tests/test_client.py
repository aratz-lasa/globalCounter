from globalCounter.client import counter_client

from .utils.count_server import global_counter

TEST_PORT = 5555
TEST_IP = "127.0.0.1"


def test_udp_client_count():
    with global_counter(TEST_IP, TEST_PORT):
        topic = "topic"
        for count in range(1, 100):
            assert counter_client.count(topic=topic) == count


def test_udp_client_count_decorator():
    topic = "topic"
    @counter_client.count_deco(topic=topic)
    def get_zero():
        return 0

    with global_counter(TEST_IP, TEST_PORT):
        sum, result = get_zero()
        assert sum == 1
        assert result == 0


def test_tcp_client_count():
    with global_counter(TEST_IP, TEST_PORT, tcp=True):
        topic = "topic"
        for count in range(1, 100):
            assert counter_client.count(topic=topic, tcp=True) == count


def test_tcp_client_count_decorator():
    topic = "topic"
    @counter_client.count_deco(topic=topic, tcp=True)
    def get_zero():
        return 0

    with global_counter(TEST_IP, TEST_PORT, tcp=True):
        sum, result = get_zero()
        assert sum == 1
        assert result == 0
