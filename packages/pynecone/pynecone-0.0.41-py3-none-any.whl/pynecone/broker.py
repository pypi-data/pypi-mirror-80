from abc import ABC, abstractmethod


class Broker(ABC):

    @abstractmethod
    def get_consumer(self):
        pass

    @abstractmethod
    def get_producer(self):
        pass