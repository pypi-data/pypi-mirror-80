from pynecone import Cmd
from .config import Config


class EnvActivate(Cmd):

        def __init__(self):
            super().__init__('activate')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the environment to be set as active")

        def run(self, args):
            env = Config.init().set_active_environment(args.name)
            if env:
                print('environment {0} activated'.format(args.name))
            else:
                print('environment {0} does not exist'.format(args.name))


        def get_help(self):
            return 'activate an environment'