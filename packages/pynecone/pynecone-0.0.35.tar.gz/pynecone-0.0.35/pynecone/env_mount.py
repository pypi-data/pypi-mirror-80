from pynecone import Shell

from .env_mount_create import EnvMountCreate
from .env_mount_delete import EnvMountDelete
from .env_mount_list import EnvMountList


class EnvMount(Shell):

        def __init__(self):
            super().__init__('mount')

        def get_commands(self):
            return [
                    EnvMountCreate(),
                    EnvMountDelete(),
                    EnvMountList()
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'configure mount points'