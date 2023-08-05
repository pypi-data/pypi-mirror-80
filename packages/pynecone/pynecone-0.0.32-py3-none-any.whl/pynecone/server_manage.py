from pynecone import Cmd


class Server_Manage(Cmd):

        def __init__(self):
            super().__init__('server_manage')

        def add_arguments(self, parser):
            parser.add_argument('op', choices=['one', 'two'],
                                help="a choice between one and two", default='two', const='two', nargs='?')
            parser.add_argument('--name', help="specifies the name", default="somename")

        def run(self, args):
            pass

        def get_help(self):
            return 'help'