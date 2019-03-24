import socket
from multiprocessing import Pool, Queue, Manager, cpu_count

from ..protocol.methods import *
from ..protocol.models import *
from ..various.abc import CounterServer


MAX_WORKERS = cpu_count()


class UDPCounterServer(CounterServer):
    def __init__(self, ip="0.0.0.0", port=0, max_workers=MAX_WORKERS):
        self.ip = ip
        self.port = port
        self.sock = None
        self.is_running = False
        # workers
        self.manager = Manager()
        self.topic_sum_map = self.manager.dict()
        self.pending_requests = Queue()
        self.workers_pool = Pool(processes=max_workers, initializer=self.worker_loop)

    def run(self):
        self.bind_socket()
        self.is_running = True

        try:
            while self.is_running:
                msg, addr = self.sock.recvfrom(MSG_MAXIMUM_LENGTH)
                self.pending_requests.put((msg,addr))
        except Exception as err:
            if self.is_running:
                raise err

    def worker_loop(self):
        while True:
            msg, addr = self.pending_requests.get()
            re_msg = get_response(msg, self.topic_sum_map)
            self.send_response(addr, re_msg)

    def send_response(self, addr, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, addr)

    def bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

    def stop(self):
        self.is_running = False
        self.workers_pool.terminate()
        self.workers_pool.join()
        self.sock.close()


class TCPCounterServer(CounterServer):
    def __init__(self, ip="0.0.0.0", port=0, max_workers=MAX_WORKERS):
        self.ip = ip
        self.port = port
        self.sock = None
        self.is_running = False
        # workers
        self.manager = Manager()
        self.topic_sum_map = self.manager.dict()
        self.pending_requests = Queue()
        self.workers_pool = Pool(processes=max_workers, initializer=self.worker_loop)

    def run(self):
        self.bind_socket()
        self.is_running = True

        try:
            while self.is_running:
                conn, addr = self.sock.accept()
                self.pending_requests.put((conn, addr))
        except Exception as err:
            if self.is_running:
                raise err

    def worker_loop(self):
        while True:
            conn, addr = self.pending_requests.get()
            msg = conn.recv(MSG_MAXIMUM_LENGTH)
            re_msg = get_response(msg, self.topic_sum_map)
            self.send_response(conn, re_msg)

    def send_response(self, conn, message):
        conn.send(message)
        conn.close()

    def bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)

    def stop(self):
        self.is_running = False
        self.sock.close()
