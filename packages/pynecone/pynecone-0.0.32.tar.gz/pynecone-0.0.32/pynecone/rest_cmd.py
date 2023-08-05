from .cmd import Cmd
from .auth import Auth, AuthMode

from requests_toolbelt.utils import dump

from urllib.parse import urljoin


class RestCmd(Cmd):

    def get_endpoint_url(self, api, path):
        return urljoin(self.get_config().get_api(api)['url'], path)

    def dump(self, response):
        data = dump.dump_all(response)
        print(data.decode('utf-8'))

    def get_arguments(self, api):
        arguments = {'headers': None, 'cookies': None,
            'auth': None, 'timeout': self.get_config().get_timeout(), 'allow_redirects': True, 'proxies': None,
            'hooks': None, 'stream': None, 'verify': None, 'cert': None, 'json': None}

        auth = Auth(self.get_config().get_api(api)['auth'])
        mode = auth.get_mode()

        if mode == AuthMode.CLIENT_KEY or mode == AuthMode.AUTH_URL:
            token = auth.retrieve_token()
            arguments['headers'] = {"Authorization": "Bearer " + token}
        elif mode == AuthMode.CLIENT_CERT:
            arguments['cert'] = (auth.client_cert, auth.client_cert_key)
            if auth.ca_bundle is not None:
                arguments['verify'] = auth.ca_bundle
        elif mode == AuthMode.BASIC:
            arguments['auth'] = auth.get_basic_token()

        return arguments