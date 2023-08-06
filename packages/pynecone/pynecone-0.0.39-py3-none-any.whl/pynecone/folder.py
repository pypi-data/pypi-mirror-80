from .proto import ProtoShell, ProtoCmd
from .config import Config

from os import listdir
from os.path import isfile, isdir, join


class Folder(ProtoShell):

    class Get(ProtoCmd):

        def __init__(self):
            super().__init__('get',
                             'get folder or file from path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path", default='.', const='.', nargs='?')

        def run(self, args):
            folder = Config.init().get_folder(args.path)
            print([c.get_name() for c in folder.get_children()])

    class Put(ProtoCmd):

        def __init__(self):
            super().__init__('put',
                             'put folder or file to path',
                             lambda args: Config.init().get_folderfile(path))

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path", default='.', const='.', nargs='?')

    class Delete(ProtoCmd):

        def __init__(self):
            super().__init__('delete',
                             'delete path',
                             lambda args: Config.init().get_folderfile(path))

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path to be deleted", default='.', const='.', nargs='?')

    class List(ProtoCmd):

        def __init__(self):
            super().__init__('list',
                             'list files and folders on path')

        def add_arguments(self, parser):
            parser.add_argument('path', help="specifies the path to be listed", default=None, const=None, nargs='?')

        def run(self, args):
            if args.path:
                fragments = [fragment for fragment in args.path.split('/') if fragment]
                if fragments:
                    mount = fragments[0]
                    path = '/'.join(fragments[1:])
                    print(mount, path)
                else:
                    for mount in Config.init().list_mount():
                        print(mount['name'])
            else:
                for mount in Config.init().list_mount():
                    print(mount['name'])

    def __init__(self):
        super().__init__('folder', [Folder.Get(), Folder.Put(), Folder.Delete(), Folder.List()], 'folder shell')
