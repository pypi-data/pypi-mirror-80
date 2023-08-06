from abc import ABC, abstractmethod


class MountProvider(ABC):

    @abstractmethod
    def get_folder(self, path):
        pass


class FolderProvider(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_path(self):
        pass

    @abstractmethod
    def is_folder(self):
        pass

    @abstractmethod
    def get_children(self):
        pass

    @abstractmethod
    def get_stat(self):
        pass

    @abstractmethod
    def get_hash(self):
        pass

    @abstractmethod
    def create_folder(self, name):
        pass

    @abstractmethod
    def create_file(self, name, data):
        pass

    @abstractmethod
    def delete(self, name):
        pass


class BrokerProvider(ABC):

    @abstractmethod
    def get_topic(self, name):
        pass


class TopicProvider(ABC):

    @abstractmethod
    def get_consumer(self):
        pass

    @abstractmethod
    def get_producer(self):
        pass


class ConsumerProvider(ABC):

    @abstractmethod
    def consume(self, args):
        pass


class ProducerProvider(ABC):

    @abstractmethod
    def produce(self, message):
        pass


class JobSchedulerProvider(ABC):

    @abstractmethod
    def run(self, job):
        pass


class TaskSchedulerProvider(ABC):

    @abstractmethod
    def run(self, task):
        pass


class TaskProvider(ABC):

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
