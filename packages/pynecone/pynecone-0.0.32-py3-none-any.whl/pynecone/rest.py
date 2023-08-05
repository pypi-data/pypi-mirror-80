from .shell import Shell
from .rest_get import RestGet
from .rest_put import RestPut
from .rest_post import RestPost
from .rest_delete import RestDelete
from .config import Config

class Rest(Shell):

    def get_commands(self):
        return [RestGet(),
                RestPut(),
                RestPost(),
                RestDelete()]

    def add_arguments(self, parser):
        pass

    def __init__(self):
        super().__init__('rest')



    def get_help(self):
        return 'makes standard Rest calls'

    @classmethod
    def api(cls, name=None):
        auth = Config.get_api(name)['auth']
        pass











