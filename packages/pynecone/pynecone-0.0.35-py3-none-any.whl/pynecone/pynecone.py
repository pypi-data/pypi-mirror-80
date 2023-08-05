from .shell import Shell
from .gen import Gen
from .env import Env
from .task import Task
from .folder import Folder
from .server import Server
from .job import Job
from .repl import Repl
from .rest import Rest

class Pynecone(Shell):

    def __init__(self):
        super().__init__('pynecone')

    def get_commands(self):
        return [Gen(), Env(), Task(), Folder(), Server(), Job(), Repl(), Rest()]

    def add_arguments(self, parser):
        pass

    def get_help(self):
        return 'pynecone shell'