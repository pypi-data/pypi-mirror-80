from abc import abstractmethod
from .cmd import Cmd
from .cfg import Cfg


class Consumer(Cmd):

    def add_arguments(self, parser):
        parser.add_argument('topic', help="name of the topic to listen")
        parser.add_argument('script', help="path to the script file")
        parser.add_argument('method', help="name of the handler method in the script file")

    def run(self, args):
        return self.consume(args)

    def get_help(self):
        return 'listen to a topic and execute a specific script method when a message is received'

    @abstractmethod
    def consume(self, args):
        pass

    def get_config(self):
        return Cfg()