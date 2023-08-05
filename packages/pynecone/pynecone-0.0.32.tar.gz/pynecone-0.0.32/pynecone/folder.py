from pynecone import Shell

from .folder_list import Folder_List
from .folder_download import Folder_Download
from .folder_upload import Folder_Upload
from .folder_delete import Folder_Delete
from .folder_create import Folder_Create
from .folder_update import Folder_Update


class Folder(Shell):

        def __init__(self):
            super().__init__('folder')

        def get_commands(self):
            return [
                    Folder_List(),
                    Folder_Download(),
                    Folder_Upload(),
                    Folder_Delete(),
                    Folder_Create(),
                    Folder_Update()
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'Folder shell'