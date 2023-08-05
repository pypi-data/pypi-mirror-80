from .rest_cmd import RestCmd
from .auth import Auth, AuthMode
from .config import Config

import requests


class RestPut(RestCmd):

    def __init__(self):
        super().__init__('put')
        self.cfg = Config.init()

    def add_arguments(self, parser):
        parser.add_argument('api', help="specifies the api to use")
        parser.add_argument('path', help="specifies the path", default='/', const='/', nargs='?')
        parser.add_argument('--params', help="list of key:value pairs", nargs='+')
        parser.add_argument('--json', help="json message body")
        parser.add_argument('--debug', action='store_true', help="enable debugging")

    def run(self, args):
        print(self.put( args.api,
                        args.path,
                        args.debug,
                        dict([kv.split(':') for kv in args.params]) if args.params else None,
                        json=args.json))

    def get_help(self):
        return 'make a PUT request to the API'

    def put(self, api, path, debug=False, data=None, json=None):

        arguments = self.get_arguments(api)
        arguments['json'] = json

        resp = requests.put(self.get_endpoint_url(api, path), data=data, **arguments)

        if debug:
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.put(api, path, debug, data, json)
            else:
                print('Unauthorized')
        else:
            print(resp.status_code, resp.text)
            if not debug:
                self.dump(resp)
            return None

    def put_file(self, api, path, file):

        resp = requests.put(self.get_endpoint_url(api, path), files=dict(file=file), **self.get_arguments())

        if self.get_config().get_debug():
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            return resp.status_code
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.put_file(api, path, file)
            else:
                print('Unauthorized')
        else:
            print(resp.status_code, resp.text)
            if not self.get_config().get_debug():
                self.dump(resp)
            return None
