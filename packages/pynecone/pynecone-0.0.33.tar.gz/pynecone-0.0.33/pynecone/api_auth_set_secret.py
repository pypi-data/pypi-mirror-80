from pynecone import Cmd
from .config import Config


class ApiAuthSetSecret(Cmd):

        def __init__(self):
            super().__init__('secret')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the api name")
            parser.add_argument('client_key', help="specifies the client key")
            parser.add_argument('client_secret', help="specifies the client secret")
            parser.add_argument('token_url', help="specifies the token url")

        def run(self, args):
            res = Config.init().modify_api_auth(args.name,
                                                'CLIENT_KEY',
                                                client_key=args.client_key,
                                                client_secret=args.client_secret,
                                                token_url=args.token_url)
            if res:
                return res
            else:
                print('Unable to modify authentication parameters for API {0}'.format(args.name))

        def get_help(self):
            return 'configure client key and secret based authentication'