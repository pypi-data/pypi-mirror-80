from pynecone import Shell

from .api_auth import ApiAuth
from .api_url import ApiUrl


class EnvApiManage(Shell):

        def __init__(self):
            super().__init__('manage')

        def get_commands(self):
            return [
                    ApiAuth(),
                    ApiUrl()
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'manage the api'