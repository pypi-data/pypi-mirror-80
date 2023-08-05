from pynecone import Shell

from .mount_local import MountLocal
from .mount_aws import MountAws
from .mount_google import MountGoogle
from .mount_azure import MountAzure


class EnvMountCreate(Shell):

        def __init__(self):
            super().__init__('create')

        def get_commands(self):
            return [
                    MountLocal(),
                    MountAws(),
                    MountGoogle(),
                    MountAzure()
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'mount a new filesystem'