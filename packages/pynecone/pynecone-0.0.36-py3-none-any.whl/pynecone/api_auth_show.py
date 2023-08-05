from pynecone import Cmd
from .config import Config
import yaml

class ApiAuthShow(Cmd):

        def __init__(self):
            super().__init__('show')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the api name")

        def run(self, args):
            print(yaml.dump(Config.init().get_api(args.name)['auth']))

        def get_help(self):
            return 'show auth information'