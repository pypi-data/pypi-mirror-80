import os

import dotenv
found_dotenv = dotenv.find_dotenv(usecwd=True)
# print("using .env: ", found_dotenv)
if found_dotenv:
    dotenv.load_dotenv(found_dotenv)

class Cfg:

    def __init__(self,
                 api_base_url=os.getenv('API_BASE_URL'),
                 auth_url=os.getenv('AUTH_URL'),
                 callback_url=os.getenv('CALLBACK_URL', 'http://localhost:8080'),
                 client_id=os.getenv('CLIENT_ID'),
                 client_key=os.getenv('CLIENT_KEY'),
                 client_secret=os.getenv('CLIENT_SECRET'),
                 token_url=os.getenv('TOKEN_URL'),
                 client_cert=os.getenv('CLIENT_CERT'),
                 client_cert_key=os.getenv('CLIENT_CERT_KEY'),
                 ca_bundle=os.getenv('CA_BUNDLE'),
                 basic_username=os.getenv('BASIC_USERNAME'),
                 basic_password=os.getenv('BASIC_PASSWORD'),
                 amqp_client_key=os.getenv('AMQP_CLIENT_KEY'),
                 amqp_client_secret=os.getenv('AMQP_CLIENT_SECRET'),
                 amqp_host=os.getenv('AMQP_HOST'),
                 amqp_port=os.getenv('AMQP_PORT'),
                 amqp_path=os.getenv('AMQP_PATH'),
                 amqp_queue_name=os.getenv('AMQP_QUEUE_NAME'),
                 basic_use_digest=os.getenv('BASIC_USE_DIGEST', False),
                 debug=os.getenv('DEBUG', False),
                 timeout=os.getenv('TIMEOUT', 10)):

        '''
        :param api_base_url:
        :param auth_url:
        :param callback_url:
        :param client_id:
        :param client_key:
        :param client_secret:
        :param token_url:
        :param client_cert:
        :param client_cert_key:
        :param ca_bundle:
        :param basic_username:
        :param basic_password:
        :param amqp_client_key:
        :param amqp_client_secret:
        :param amqp_host:
        :param amqp_port:
        :param amqp_path:
        :param amqp_queue_name:
        :param basic_use_digest:
        :param debug:
        :param timeout:
        '''

        self.api_base_url = api_base_url
        self.auth_url = auth_url
        self.callback_url = callback_url
        self.client_id = client_id
        self.client_key = client_key
        self.client_secret = client_secret
        self.token_url = token_url
        self.basic_username = basic_username
        self.basic_password = basic_password
        self.basic_use_digest = basic_use_digest
        self.amqp_client_key = amqp_client_key
        self.amqp_client_secret = amqp_client_secret
        self.amqp_host = amqp_host
        self.amqp_port = amqp_port
        self.amqp_path = amqp_path
        self.amqp_queue_name = amqp_queue_name
        self.client_cert = client_cert
        self.client_cert_key = client_cert_key
        self.ca_bundle = ca_bundle
        self.debug = debug
        self.timeout = timeout

    def get_client_id(self):
        return self.client_id

    def get_client_key(self):
        return self.client_key

    def get_client_secret(self):
        return self.client_secret

    def get_callback_url(self):
        return self.callback_url

    def get_auth_url(self):
        return self.auth_url

    def get_api_base_url(self):
        return self.api_base_url

    def get_token_url(self):
        return self.token_url

    def get_debug(self):
        return self.debug

    def get_client_cert(self):
        return self.client_cert

    def get_client_cert_key(self):
        return self.client_cert_key

    def get_ca_bundle(self):
        return self.ca_bundle

    def get_timeout(self):
        return self.timeout

    def get_basic_username(self):
        return self.basic_username

    def get_basic_password(self):
        return self.basic_password

    def get_basic_use_digest(self):
        return self.basic_use_digest

    def get_amqp_client_key(self):
        return self.amqp_client_key

    def get_amqp_client_secret(self):
        return self.amqp_client_secret

    def get_amqp_host(self):
        return self.amqp_host

    def get_amqp_port(self):
        return self.amqp_port

    def get_amqp_path(self):
        return self.amqp_path

    def get_amqp_queue_name(self):
        return self.amqp_queue_name
