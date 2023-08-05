from pynecone import Cmd
from .config import Config

class ApiAuthSetBasic(Cmd):

        def __init__(self):
            super().__init__('basic')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the api name")
            parser.add_argument('basic_username', help="specifies the username")
            parser.add_argument('basic_password', help="specifies the password")
            parser.add_argument('basic_use_digest', help="specifies whether to use digest")

        def run(self, args):
            res = Config.init().modify_api_auth(args.name,
                                                'BASIC',
                                                basic_username=args.basic_username,
                                                basic_password=args.basic_password,
                                                basic_use_digest=args.basic_use_digest)
            if res:
                return res
            else:
                print('Unable to modify authentication parameters for API {0}'.format(args.name))

        def get_help(self):
            return 'configure API to use basic authentication'