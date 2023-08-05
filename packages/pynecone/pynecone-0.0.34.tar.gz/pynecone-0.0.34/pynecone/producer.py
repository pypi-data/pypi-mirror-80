from abc import abstractmethod
from .cmd import Cmd
from .cfg import Cfg


class Producer(Cmd):

    def add_arguments(self, parser):
        parser.add_argument('topic', help="topic name")
        parser.add_argument('message', help='message content')
        parser.add_argument('--exchange', help='exchange', default='')

    def run(self, args):
        return self.produce(args)

    def get_help(self):
        return 'publish a message to a topic'

    @abstractmethod
    def produce(self, args):
        pass

    def get_config(self):
        return Cfg()

