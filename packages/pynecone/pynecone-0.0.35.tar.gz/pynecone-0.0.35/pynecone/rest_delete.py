from .rest_cmd import RestCmd
from .auth import Auth, AuthMode
from .config import Config

import requests


class RestDelete(RestCmd):

    def __init__(self):
        super().__init__('delete')
        self.cfg = Config.init()

    def add_arguments(self, parser):
        parser.add_argument('api', help="specifies the api to use")
        parser.add_argument('path', help="specifies the path", default='/', const='/', nargs='?')
        parser.add_argument('--debug', action='store_true', help="enable debugging")

    def run(self, args):
        return self.delete(args.api, args.path, args.debug)

    def get_help(self):
        return 'make a DELETE request to the API'

    def delete(self, api, path, debug=False):

        resp = requests.delete(self.get_endpoint_url(api, path), **self.get_arguments(api))

        if debug:
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.delete(api, path, debug)
            else:
                print('Unauthorized')
        else:
            if not debug:
                self.dump(resp)
            return None