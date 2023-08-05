from .rest_cmd import RestCmd
from .auth import Auth, AuthMode
from .config import Config

import json
import requests


class RestPost(RestCmd):

    def __init__(self):
        super().__init__('post')
        self.cfg = Config.init()

    def add_arguments(self, parser):
        parser.add_argument('api', help="specifies the api to use")
        parser.add_argument('path', help="specifies the path", default='/', const='/', nargs='?')
        parser.add_argument('--params', help="list of key:value pairs", nargs='+')
        parser.add_argument('--json', help="json message body")
        parser.add_argument('--debug', action='store_true', help="enable debugging")

    def run(self, args):
        return self.post(args.api,
                        args.path,
                        args.debug,
                        dict([kv.split(':') for kv in args.params]) if args.params else None,
                        json_str=args.json)

    def get_help(self):
        return 'make a POST request on the API'

    def post(self, api, path, debug=False, params=None, json_str=None):
        arguments = self.get_arguments(api)
        arguments['json'] = json.loads(json_str) if json_str else None

        resp = requests.post(self.get_endpoint_url(api, path), data=params, **arguments)

        if debug:
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.post(api, path, debug, params)
            else:
                print('Unauthorized')
        else:
            if not debug:
                self.dump(resp)
            return None
