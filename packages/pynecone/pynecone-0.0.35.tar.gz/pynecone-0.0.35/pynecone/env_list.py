from pynecone import Cmd
from .config import Config


class EnvList(Cmd):

        def __init__(self):
            super().__init__('list')

        def add_arguments(self, parser):
            pass

        def run(self, args):
            envs = Config.init().list_environments()
            active = Config.init().get_active_environment()

            for env in envs:
                if env['name'] == active:
                    print('-> {0}'.format(env['name']))
                else:
                    print('   {0}'.format(env['name']))

        def get_help(self):
            return 'list available environments'