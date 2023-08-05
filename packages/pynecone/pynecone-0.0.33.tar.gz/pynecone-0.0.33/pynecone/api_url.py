from pynecone import Shell

from .api_url_get import ApiUrlGet
from .api_url_set import ApiUrlSet


class ApiUrl(Shell):

        def __init__(self):
            super().__init__('url')

        def get_commands(self):
            return [
                    ApiUrlGet(),
                    ApiUrlSet()
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'manage api url'