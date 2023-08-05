from pynecone import Shell

from .server_create import Server_Create
from .server_list import Server_List
from .server_show import Server_Show
from .server_destroy import Server_Destroy
from .server_manage import Server_Manage


class Server(Shell):

        def __init__(self):
            super().__init__('server')

        def get_commands(self):
            return [
                    Server_Create(),
                    Server_List(),
                    Server_Show(),
                    Server_Destroy(),
                    Server_Manage()
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'Server shell'