from pynecone import Shell


class Job(Shell):

        def __init__(self):
            super().__init__('job')

        def get_commands(self):
            return [
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'Job shell'