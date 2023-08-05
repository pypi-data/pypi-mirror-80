from pynecone import Cmd
from .config import Config


class EnvCreate(Cmd):

        def __init__(self):
            super().__init__('create')

        def add_arguments(self, parser):
            parser.add_argument('name', help="the name of the new environment")

        def run(self, args):
            res = Config.init().create_environment(args.name)
            if res:
                print('environment {0} created'.format(args.name))
            else:
                print('environment {0} already exists'.format(args.name))


        def get_help(self):
            return 'create a new environment'