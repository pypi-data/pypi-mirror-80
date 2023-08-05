from pynecone import Cmd
from .config import Config


class ApiAuthSetUser(Cmd):

        def __init__(self):
            super().__init__('user')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the api name")
            parser.add_argument('callback_url', help="specifies the callback url")
            parser.add_argument('auth_url', help="specifies the auth url")

        def run(self, args):
            res = Config.init().modify_api_auth(args.name,
                                                'AUTH_URL',
                                                callback_url=args.callback_url,
                                                auth_url=args.auth_url)
            if res:
                return res
            else:
                print('Unable to modify authentication parameters for API {0}'.format(args.name))

        def get_help(self):
            return 'configure user oauth2 flow'