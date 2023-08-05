from pynecone import Cmd
from .config import Config


class EnvApiCreate(Cmd):

        def __init__(self):
            super().__init__('create')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the API")
            parser.add_argument('url', help="specifies the url of the API")

        def run(self, args):
            api = Config.init().create_api(args.name, args.url)
            if api:
                print('API {0} created'.format(args.name))
            else:
                print('API {0} already exists'.format(args.name))

        def get_help(self):
            return 'create an API'