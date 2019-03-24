import pytest

from globalCounter.client import counter_client
from globalCounter.various.exceptions import CounterTCPConnection, CounterUDPConnection
from .utils.count_server import global_counter

TEST_PORT = 5555
TEST_IP = "127.0.0.1"


def test_udp_client_count():
    with global_counter(TEST_IP, TEST_PORT):
        topic = "test"
        for count in range(1, 100):
            assert counter_client.count(topic=topic) == count

    with pytest.raises(CounterUDPConnection):
        counter_client.count(topic=topic)


def test_tcp_client_count():
    with global_counter(TEST_IP, TEST_PORT, tcp=True):
        topic = "test"
        for count in range(1, 100):
            assert counter_client.count(topic=topic, tcp=True) == count

    with pytest.raises(CounterTCPConnection):
        counter_client.count(topic=topic, tcp=True)


def test_udp_client_count_decorator():
    topic = "test"

    @counter_client.count_deco(topic=topic)
    def get_zero():
        return 0

    with global_counter(TEST_IP, TEST_PORT):
        sum, result = get_zero()
        assert sum == 1
        assert result == 0

    with pytest.raises(CounterUDPConnection):
        get_zero()


def test_tcp_client_count_decorator():
    topic = "test"

    @counter_client.count_deco(topic=topic, tcp=True)
    def get_zero():
        return 0

    with global_counter(TEST_IP, TEST_PORT, tcp=True):
        sum, result = get_zero()
        assert sum == 1
        assert result == 0

    with pytest.raises(CounterTCPConnection):
        get_zero()


def test_udp_client_reset():
    with global_counter(TEST_IP, TEST_PORT):
        topic = "test"
        for count in range(1, 100):
            assert counter_client.count(topic=topic) == count

        counter_client.reset(topic=topic)
        for count in range(1, 100):
            assert counter_client.count(topic=topic) == count

    with pytest.raises(CounterUDPConnection):
        counter_client.reset(topic=topic)


def test_tcp_client_reset():
    with global_counter(TEST_IP, TEST_PORT, tcp=True):
        topic = "test"
        for count in range(1, 100):
            assert counter_client.count(topic=topic, tcp=True) == count

        counter_client.reset(topic=topic, tcp=True)
        for count in range(1, 100):
            assert counter_client.count(topic=topic, tcp=True) == count

    with pytest.raises(CounterTCPConnection):
        counter_client.reset(topic=topic, tcp=True)
