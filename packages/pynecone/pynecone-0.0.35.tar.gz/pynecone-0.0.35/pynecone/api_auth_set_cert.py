from pynecone import Cmd
from .config import Config


class ApiAuthSetCert(Cmd):

        def __init__(self):
            super().__init__('cert')

        def add_arguments(self, parser):
            parser.add_argument('name', help="specifies the api name")
            parser.add_argument('client_cert', help="specifies the path to the client certificate file")
            parser.add_argument('client_cert_key', help="specifies the path to the client certificate key file")
            parser.add_argument('ca_bundle', help=" the path to the certificate authority file")

        def run(self, args):
            res = Config.init().modify_api_auth(args.name,
                                                'CLIENT_CERT',
                                                client_cert=args.client_cert,
                                                client_cert_key=args.client_cert_key,
                                                ca_bundle=args.ca_bundle)
            if res:
                return res
            else:
                print('Unable to modify authentication parameters for API {0}'.format(args.name))

        def get_help(self):
            return 'configure client certificate based authentication'