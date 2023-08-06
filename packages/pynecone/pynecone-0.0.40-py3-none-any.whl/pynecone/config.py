import yaml
import os

import importlib
import pkgutil
import modules

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


class Config:

    def __init__(self, name, path):
        self.path = path
        self.full_path = os.path.join(path, name)
        self.data = {}
        self.modules = [name for _, name, _ in iter_namespace(modules)]


    def load(self):
        with open(self.full_path) as file:
            self.data = yaml.safe_load(file)

    def save(self):
        with open(self.full_path, 'w') as file:
            yaml.dump(self.data, file)

    def get_blank_environment(self, name):
        return {
            'name': name,
            'apis': [],
            # 'database': {'url': 'sqlite:///{0}'.format(os.path.join(self.path, 'pynecone.db'))},
            # 'server': {'host': '0.0.0.0', 'port': '8080'}
        }

    def create_environment(self, name):
        self.generate()

        found = [env for env in self.data.get('environments') if env['name'] == name]

        if found:
            return None

        env = self.get_blank_environment(name)
        self.data['environments'].append(env)
        self.save()
        return env

    def delete_environment(self, name):
        self.generate()

        found = [env for env in self.data.get('environments') if env['name'] == name]

        if found:
            if found[0]['name'] == self.data['active_environment']:
                print('cannot delete the active environment {0}'.format(name))
                return None
            else:
                self.data['environments'] = [i for i in self.data['environments'] if i['name'] != name]
                self.save()
                return name
        else:
            return None

    def set_active_environment(self, name):
        self.generate()

        found = [env for env in self.data.get('environments') if env['name'] == name]
        if found:
            self.data['active_environment'] = name
            self.save()
            return found
        else:
            return None

    def get_active_environment(self):
        self.generate()

        found = [env for env in self.data.get('environments') if env['name'] == self.data['active_environment']]
        if found:
            return found[0]
        else:
            return None

    def get_active_environment_name(self):
        self.generate()

        return self.data['active_environment']

    def list_environments(self):
        self.generate()

        return self.data['environments']

    def get_environment(self, name, yaml=False):
        self.generate()

        found = [env for env in self.data.get('environments') if env['name'] == name]
        if found:
            if yaml:
                return yaml.dump(found[0])
            else:
                return found[0]
        else:
            return None

    def create_api(self, name, url):
        env = self.get_active_environment()

        apis = env.get('apis')

        if not apis:
            apis = []
            env['apis'] = apis

        if [api for api in apis if api['name'] == name]:
            return None

        api = {'name': name, 'url': url, 'auth': {'method': 'NONE'}}
        apis.append(api)
        self.save()
        return api

    def modify_api_auth(self, name, mode, **kwargs):
        env = self.get_active_environment()

        apis = env.get('apis')

        if not apis:
            return None

        found = [api for api in apis if api['name'] == name]

        if found:
            api = found[0]
        else:
            return None

        if mode == 'BASIC':
            auth = {
                'mode': 'BASIC',
                'basic_username': kwargs['basic_username'],
                'basic_password': kwargs['basic_password'],
                'basic_use_digest': kwargs['basic_use_digest']
            }
        elif mode == 'CLIENT_CERT':
            auth = {
                'mode': 'CLIENT_CERT',
                'client_cert': kwargs['client_cert'],
                'client_cert_key': kwargs['client_cert_key'],
                'ca_bundle': kwargs['ca_bundle']
            }
        elif mode == 'CLIENT_KEY':
            auth = {
                'mode': 'CLIENT_KEY',
                'client_key': kwargs['client_key'],
                'client_secret': kwargs['client_secret'],
                'token_url': kwargs['token_url']
            }
        elif mode == 'AUTH_URL':
            auth = {
                'mode': 'AUTH_URL',
                'callback_url': kwargs['callback_url'],
                'auth_url': kwargs['auth_url']
            }
        else:
            auth = {'mode': 'NONE'}

        api['auth'] = auth
        self.save()
        return auth

    def list_api(self):
        env = self.get_active_environment()
        return [api for api in env['apis']]

    def get_active_api(self):
        return [api for api in self.list_api()][0]

    def get_api(self, name, outputYaml=False):
        api = [api for api in self.list_api() if api['name'] == name]
        if api:
            return yaml.dump(api[0]) if outputYaml else api[0]
        else:
            return None

    def delete_api(self, name):
        env = self.get_active_environment()
        found = [api for api in env['apis'] if api['name'] == name]

        if found:
            env['apis'] = [i for i in env['apis'] if i['name'] != name]
            self.save()
            return name
        else:
            return None

    def create_mount(self, name, mount):
        env = self.get_active_environment()

        mounts = env.get('mounts')

        if not mounts:
            mounts = []
            env['mounts'] = mounts

        if [mount for mount in mounts if mount['name'] == name]:
            return None

        mount = {'name': name, 'mount': mount }
        mounts.append(mount)
        self.save()
        return mount

    def get_mount_cfg(self, name, outputYaml=False):
        mount = [mount for mount in self.list_mount() if mount['name'] == name]
        if mount:
            return yaml.dump(mount[0]) if outputYaml else mount[0]
        else:
            return None


    def get_mount(self, name):
        cfg = self.get_mount_cfg(name)
        if cfg:
            mount_mods = [m.split('_')[1] for m in self.modules if m.startswith('modules.mount_')]
            mount_mod = [m for m in mount_mods if m == cfg['mount']['type']]
            mod_cfg = dict(cfg['mount'])
            mod_cfg['name'] = name
            return getattr(importlib.import_module('modules.mount_{0}'.format(mount_mod[0])), 'Module')(**mod_cfg)
        else:
            return None

    def get_folder(self, path):
        mount_path = '/{0}'.format(path.split('/')[1])
        target_path = '/'.join(path.split('/')[2:])
        return self.get_mount(mount_path).get_folder(target_path)

    def list_mount(self):
        env = self.get_active_environment()
        return [mount for mount in env['mounts']]

    def delete_mount(self, name):
        env = self.get_active_environment()
        found = [mount for mount in env['mounts'] if mount['name'] == name]

        if found:
            env['mounts'] = [i for i in env['mounts'] if i['name'] != name]
            self.save()
            return name
        else:
            return None

    def get_timeout(self):
        return 20

    def modify_api_url(self, name, url):
        env = self.get_active_environment()

        apis = env.get('apis')

        if not apis:
            return None

        found = [api for api in apis if api['name'] == name]

        if found:
            api = found[0]
        else:
            return None

        api['url'] = url

        self.save()
        return api

    def get_active_environment_name(self):
        self.generate()

        return self.data['active_environment']

    def generate(self, force=False):
        if self.data.get('environments') is None or force:
            print('*** generating default config file ***')

            self.data = {
                'environments': [
                        self.get_blank_environment('local')
                ],
                'active_environment': 'local'}

            self.save()

    def get_database_url(self):
        return self.data['database']['url']

    def get_server_host(self):
        return self.data['server']['host']

    def get_server_port(self):
        return self.data['server']['port']

    @classmethod
    def init(cls, name='pynecone.yml', path=os.getcwd()):
        cfg = Config(name, path)

        if not os.path.exists(cfg.full_path):
            cfg.generate()

        cfg.load()
        return cfg
