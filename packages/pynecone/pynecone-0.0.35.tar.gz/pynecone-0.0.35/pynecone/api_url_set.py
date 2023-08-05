from .cmd import Cmd
from .config import Config

class ApiUrlSet(Cmd):

        def __init__(self):
            super().__init__('set')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the API")
            parser.add_argument('url', help="specifies the url of the API")

        def run(self, args):
            res = Config.init().modify_api_url(args.name, args.url)
            if res:
                return res
            else:
                print('Unable to modify url parameter for API {0}'.format(args.name))

        def get_help(self):
            return 'change the API url'