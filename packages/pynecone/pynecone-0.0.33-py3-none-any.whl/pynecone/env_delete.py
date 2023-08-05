from pynecone import Cmd
from .config import Config


class EnvDelete(Cmd):

        def __init__(self):
            super().__init__('delete')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the environment to be deleted")

        def run(self, args):
            if Config.init().delete_environment(args.name):
                print('environment {0} deleted'.format(args.name))
            else:
                print('unable to delete environment {0}'.format(args.name))

        def get_help(self):
            return 'delete an environment'