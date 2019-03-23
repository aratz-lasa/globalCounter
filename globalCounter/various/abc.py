from abc import ABCMeta, abstractmethod


class CounterServer(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def send_response(self, addr, re_msg):
        pass

    @abstractmethod
    def bind_socket(self):
        pass
