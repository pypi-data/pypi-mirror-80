from pynecone import Shell

from .job_list import Job_List
from .job_delete import Job_Delete
from .job_schedule import Job_Schedule
from .job_update import Job_Update


class Job(Shell):

        def __init__(self):
            super().__init__('job')

        def get_commands(self):
            return [
                    Job_List(),
                    Job_Delete(),
                    Job_Schedule(),
                    Job_Update()
            ]

        def add_arguments(self, parser):
            pass

        def get_help(self):
            return 'Job shell'