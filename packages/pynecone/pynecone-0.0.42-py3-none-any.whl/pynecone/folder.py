from .proto import ProtoShell, ProtoCmd
from .config import Config

from os import listdir
from os.path import isfile, isdir, join


class Folder(ProtoShell):

    class Copy(ProtoCmd):

        def __init__(self):
            super().__init__('copy',
                             'copy from source_path to target_path')

        def add_arguments(self, parser):
            parser.add_argument('source_path', help="specifies the source_path")
            parser.add_argument('target_path', help="specifies the target_path")

        def run(self, args):
            config = Config.init()
            source_folder = config.get_folder(args.source_path)
            target_folder = config.get_folder(args.target_path)
            source_folder.copy(target_folder)

    class Get(ProtoCmd):

        def __init__(self):
            super().__init__('get',
                             'download folder or file from path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path")
            parser.add_argument('--local_path', help="specifies the local path where to save", default='.')

        def run(self, args):
            config = Config.init()
            folder = config.get_folder(args.path)
            local_path = config.get_folder(args.local_path)
            folder.get(local_path)

    class Put(ProtoCmd):

        def __init__(self):
            super().__init__('put',
                             'upload folder or file to path')

        def add_arguments(self, parser):
            parser.add_argument('local_path', help="specifies the local path to upload")
            parser.add_argument('target_path', help="specifies the target path")


        def run(self, args):
            config = Config.init()
            folder = config.get_folder(args.path)
            local_path = config.get_folder(args.local_path)
            folder.get(local_path)

    class Delete(ProtoCmd):

        def __init__(self):
            super().__init__('delete',
                             'delete path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path to be deleted")

        def run(self, args):
            print(Config.init().get_folder(args.path).delete())

    class List(ProtoCmd):

        def __init__(self):
            super().__init__('list',
                             'list files and folders on path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path to be listed", default=None, const=None, nargs='?')

        def run(self, args):
            if args.path:
                if args.path:
                    folder = Config.init().get_folder(args.path)
                    for c in folder.get_children():
                        print(c.get_name())
                else:
                    for mount in Config.init().list_mount():
                        print(mount['name'])
            else:
                for mount in Config.init().list_mount():
                    print(mount['name'])

    class Checksum(ProtoCmd):

        def __init__(self):
            super().__init__('checksum',
                             'calculate the checksum of the folder at path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path to be deleted")

        def run(self, args):
            print(Config.init().get_folder(args.path).hash())

    def __init__(self):
        super().__init__('folder', [Folder.Copy(), Folder.Get(), Folder.Put(), Folder.Delete(), Folder.List(), Folder.Checksum()], 'folder shell')

    def copy_to(self, target):
        pass

    def get(self, local_path):
        pass
