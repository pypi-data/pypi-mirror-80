from pynecone import Cmd
from .config import Config

class EnvApiList(Cmd):

        def __init__(self):
            super().__init__('list')

        def add_arguments(self, parser):
            pass

        def run(self, args):
            print(Config.init().list_api())

        def get_help(self):
            return 'list apis'