from pynecone import Cmd
from .config import Config


class EnvShow(Cmd):

        def __init__(self):
            super().__init__('show')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the environment to be displayed", nargs='?')

        def run(self, args):
            cfg = Config.init()
            name = args.name if args.name else cfg.get_active_environment()
            print(cfg.get_environment(name, yaml=True))

        def get_help(self):
            return 'show environment values'