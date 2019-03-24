import trio
import pytest

from globalCounter.client import async_counter_client
from globalCounter.various.exceptions import CounterTCPConnection, CounterUDPConnection
from .utils.count_server import global_counter

TEST_PORT = 5555
TEST_IP = "127.0.0.1"


def test_udp_client_count():
    async def udp_client_count():
        with global_counter(TEST_IP, TEST_PORT):
            topic = "test"
            for count in range(1, 100):
                sum = await async_counter_client.count(topic=topic)
                assert sum == count

        with pytest.raises(CounterUDPConnection):
            await async_counter_client.count(topic=topic)

    trio.run(udp_client_count)


def test_tcp_client_count():
    async def tcp_client_count():
        with global_counter(TEST_IP, TEST_PORT, tcp=True):
            topic = "test"
            for count in range(1, 100):
                sum = await async_counter_client.count(topic=topic, tcp=True)
                assert sum == count

        with pytest.raises(CounterTCPConnection):
            await async_counter_client.count(topic=topic, tcp=True)

    trio.run(tcp_client_count)


def test_udp_client_count_decorator():

    topic = "test"

    @async_counter_client.count_deco(topic=topic)
    def get_zero():
        return 0

    async def udp_client_count_decorator():
        with global_counter(TEST_IP, TEST_PORT):
            sum, result = await get_zero()
            assert sum == 1
            assert result == 0

        with pytest.raises(CounterUDPConnection):
            await get_zero()

    trio.run(udp_client_count_decorator)


def test_tcp_client_count_decorator():
    topic = "test"

    @async_counter_client.count_deco(topic=topic, tcp=True)
    def get_zero():
        return 0

    async def tcp_client_count_decorator():
        with global_counter(TEST_IP, TEST_PORT, tcp=True):
            sum, result = await get_zero()
            assert sum == 1
            assert result == 0

        with pytest.raises(CounterTCPConnection):
            await get_zero()

    trio.run(tcp_client_count_decorator)


def test_udp_client_reset():
    async def udp_client_reset():
        with global_counter(TEST_IP, TEST_PORT):
            topic = "test"
            for count in range(1, 100):
                sum = await async_counter_client.count(topic=topic)
                assert sum == count

            await async_counter_client.reset(topic=topic)
            for count in range(1, 100):
                sum = await async_counter_client.count(topic=topic)
                assert sum == count

        with pytest.raises(CounterUDPConnection):
            await async_counter_client.reset(topic=topic)

    trio.run(udp_client_reset)


def test_tcp_client_reset():
    async def tcp_client_reset():
        with global_counter(TEST_IP, TEST_PORT, tcp=True):
            topic = "test"
            for count in range(1, 100):
                sum = await async_counter_client.count(topic=topic, tcp=True)
                assert sum == count

            await async_counter_client.reset(topic=topic, tcp=True)
            for count in range(1, 100):
                sum = await async_counter_client.count(topic=topic, tcp=True)
                assert sum == count

        with pytest.raises(CounterTCPConnection):
            await async_counter_client.reset(topic=topic, tcp=True)

    trio.run(tcp_client_reset)
