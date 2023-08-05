from pynecone import Cmd
from .config import Config


class ApiAuthSetNone(Cmd):

        def __init__(self):
            super().__init__('none')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the api name")

        def run(self, args):
            res = Config.init().modify_api_auth(args.name,
                                                'NONE')
            if res:
                return res
            else:
                print('Unable to modify authentication parameters for API {0}'.format(args.name))

        def get_help(self):
            return 'disable authentication'