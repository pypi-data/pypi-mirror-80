from .cmd import Cmd
from .config import Config

class ApiUrlGet(Cmd):

        def __init__(self):
            super().__init__('get')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the API")

        def run(self, args):
            print(Config.init().get_api(args.name)['url'])

        def get_help(self):
            return 'get the url of the api'