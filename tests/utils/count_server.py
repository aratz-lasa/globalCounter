from contextlib import contextmanager
from multiprocessing import Process
from time import sleep

from globalCounter.server.counter_server import CounterServer


@contextmanager
def global_counter(ip="127.0.0.1", port=5555):
    counter_server = CounterServer(ip=ip, port=port)
    server_proc = Process(target=counter_server.run)
    server_proc.start()
    sleep(0.1)  # wait to initialize server
    try:
        yield
    finally:
        server_proc.terminate()
