from pynecone import Shell

from .api_auth_show import ApiAuthShow
from .api_auth_set_none import ApiAuthSetNone
from .api_auth_set_basic import ApiAuthSetBasic
from .api_auth_set_cert import ApiAuthSetCert
from .api_auth_set_secret import ApiAuthSetSecret
from .api_auth_set_user import ApiAuthSetUser


class ApiAuth(Shell):

        def __init__(self):
            super().__init__('auth')

        def get_commands(self):
            return [
                    ApiAuthShow(),
                    ApiAuthSetNone(),
                    ApiAuthSetBasic(),
                    ApiAuthSetCert(),
                    ApiAuthSetSecret(),
                    ApiAuthSetUser()
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'configure api authentication'