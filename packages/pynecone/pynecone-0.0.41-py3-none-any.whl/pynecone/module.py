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