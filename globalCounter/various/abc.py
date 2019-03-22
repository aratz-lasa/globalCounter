from abc import ABCMeta, abstractmethod


class CounterServer(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass
