from .proto import ProtoShell, ProtoCmd
from .config import Config


class Broker(ProtoShell):

    class Create(ProtoShell):

        class AMQP(ProtoCmd):

            def __init__(self):
                super().__init__('amqp',
                                 'amqp broker',
                                 lambda args: print(Config.init().create_broker(args.name, {'type': 'amqp', 'bucket': args.bucket})))

            def add_arguments(self, parser):
                # parser.add_argument('name', help="specifies the broker name")
                parser.add_argument('bucket', help="specifies the bucket name")

        def __init__(self):
            super().__init__('create', [Broker.Create.Local(), Broker.Create.Aws()], 'create a broker')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the broker to be created")

    class List(ProtoCmd):

        def __init__(self):
            super().__init__('list',
                             'list brokers',
                             lambda args: print(Config.init().list_broker()))

    class Delete(ProtoCmd):

        def __init__(self):
            super().__init__('delete',
                             'delete a broker',
                             lambda args: print(Config.init().delete_broker(args.name)))

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the broker to be deleted")

    class Get(ProtoCmd):

        def __init__(self):
            super().__init__('get',
                             'get broker',
                             lambda args: print(Config.init().get_broker_cfg(args.name, True)))

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the name of the broker to be retrieved")

    def __init__(self):
        super().__init__('broker', [Broker.Create(), Broker.List(), Broker.Delete(), Broker.Get()], 'broker shell')