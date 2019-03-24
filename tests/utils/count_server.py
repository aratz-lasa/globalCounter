from contextlib import contextmanager
from multiprocessing import Process
from time import sleep
import trio

from globalCounter.server.counter_server import UDPCounterServer, TCPCounterServer
from globalCounter.server.async_counter_server import AsyncTCPCounterServer, AsyncUDPCounterServer


@contextmanager
def global_counter(ip="127.0.0.1", port=5555, tcp=False):
    if tcp:
        counter_server = TCPCounterServer(ip=ip, port=port)
    else:
        counter_server = UDPCounterServer(ip=ip, port=port)
    server_proc = Process(target=counter_server.run)
    server_proc.start()
    sleep(0.1)  # wait to initialize server
    try:
        yield
    finally:
        server_proc.terminate()
        server_proc.join()


@contextmanager
def async_global_counter(ip="127.0.0.1", port=5555, tcp=False):
    if tcp:
        counter_server = AsyncTCPCounterServer(ip=ip, port=port)
    else:
        counter_server = AsyncUDPCounterServer(ip=ip, port=port)

    server_proc = Process(target=trio.run, args=(counter_server.run, ))
    server_proc.start()
    sleep(0.1)  # wait to initialize server
    try:
        yield
    finally:
        server_proc.terminate()
        server_proc.join()
